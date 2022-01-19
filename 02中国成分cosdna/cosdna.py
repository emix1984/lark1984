from time import sleep
import time
import random
import requests
import parsel
from tqdm import tqdm
import re
import csv
import pandas as pd

# 创建csv
def makecsvfile():
    # 创建csv文件和表头
    f = open(f'cosdna.csv', mode='a', encoding='utf-8', newline='')
    print(f'\033[32m>>>创建csv文件完毕！！！<<<\033[0m')
    csv_writer = csv.DictWriter(f, fieldnames=[
        '成分英文名称',
        '成分详情页面链接',
        '成分中文名',
        '概略特性',
        '粉刺',
        '刺激',
        '安心度',
        '成分官方英文名称',
        '成分相关英文名称',
        '产品中文名称',
        '分子量',
        'Cas No',
        '说明内容',
        '参考资料',
        '当前时间',
    ])
    csv_writer.writeheader()
    print(f'\033[32m>>> csv文件<表头>写入完毕 <<<\033[0m')
    return csv_writer

# 保存数据到csv文件
def savetocsv(csv_writer,ingredients_1,ingredients_1url,ingredients_2,ingredients_3,ingredients_4,ingredients_5,ingredients_6,dp_1,dp_2,dp_3,dp_4,dp_5,dp_6,dp_7):
    #时间戳
    rightnow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # print(rightnow)
    # 存储到字典文件
    dict = {
        '成分英文名称': ingredients_1,
        '成分详情页面链接': ingredients_1url,
        '成分中文名': ingredients_2,
        '概略特性': ingredients_3,
        '粉刺': ingredients_4,
        '刺激': ingredients_5,
        '安心度': ingredients_6,
        '成分官方英文名称': dp_1,
        '成分相关英文名称': dp_2,
        '产品中文名称': dp_3,
        '分子量': dp_4,
        'Cas No': dp_5,
        '说明内容': dp_6,
        '参考资料': dp_7,
        '当前时间': rightnow,
        }
    csv_writer.writerow(dict)
    print(f'\033[31m时间：\033[0m', rightnow, f'\033[00;42m>>>写入数据：\033[0m', '成分中文名称：', ingredients_2, '成分英文名称：', ingredients_1,'\t')
    return None

# 读取csv文件
def readcsv():
    # pandas 拉取 listing.csv数据中的产品详情页链接
    df_listing = pd.read_csv(f'기사용원료.csv')
    data01 = pd.DataFrame(df_listing)
    # print(data01)
    print(f'\033[32m>>>读取listing.csv文件，进行去重操作中<<<\033[0m', '读取数据条目共计： ', len(data01), '条')
    data02 = data01.drop_duplicates("INCI")  # 去除重复链接
    # print(data02)
    print(f'\033[32m>>>数据去重操作已完成<<<\033[0m', '去重操作数据共计： ', len(data02), '条')
    lis = data02["INCI"].tolist()
    # print(urls)
    # print(type(urls))
    return lis

# 获取htmldata post方法
def response_post(url, Payload, headers):
    response = requests.post(url=url,headers=headers,data=Payload)
    htmldata = response.text
    return htmldata
# 获取htmldata get方法
def response_get(url, headers):
    response = requests.get(url=url,headers=headers)
    # print(f'正在解析 >>> {url}')
    htmldata = response.text
    return htmldata

# 判断是否是空值后，再清理多余的回车符，换行符号，空白
def cleantext(text):
    if text is None:
        # print(text, type(text), '空值')
        text = ""
    else:
        symbols = ["\n", "\t", " "]
        for symbol in symbols:
            text = text.replace(symbol, "").strip()
        return text

# 解析数据模块
def parse_1data(selector, i):
    # 成分英文名称
    ingredients_1 = selector.xpath(f'//*[@class="chem-list"]/tr[{i}]/td[1]/a/div[1]/span[1]/text()').get()
    ingredients_1 = cleantext(ingredients_1)
    # 成分详情页面链接
    ingredients_1url = selector.xpath(f'//*[@class="chem-list"]/tr[{i}]/td[1]/a[@href]/@href').get()
    ingredients_1url = "http://www.cosdna.com" + ingredients_1url
    # 成分中文名
    ingredients_2 = selector.xpath(f'//*[@class="chem-list"]/tr[{i}]/td[1]/a/div[2]/text()').get()
    ingredients_2 = cleantext(ingredients_2)
    # 概略特性
    ingredients_3 = selector.xpath(f'//*[@class="chem-list"]/tr[{i}]/td[2]/text()').get()
    ingredients_3 = cleantext(ingredients_3)
    # 粉刺
    ingredients_4 = selector.xpath(f'//*[@class="chem-list"]/tr[{i}]/td[3]/a/text()').get()
    ingredients_4 = cleantext(ingredients_4)
    # 刺激
    ingredients_5 = selector.xpath(f'//*[@class="chem-list"]/tr[{i}]/td[4]/a/text()').get()
    ingredients_5 = cleantext(ingredients_5)
    # 安心度
    ingredients_6 = selector.xpath(f'//*[@class="chem-list"]/tr[{i}]/td[5]/a/div//text()').getall()
    ingredients_6 = ''.join(ingredients_6).strip()
    ingredients_6 = cleantext(ingredients_6)
    # print(ingredients_1,ingredients_1url,ingredients_2,ingredients_3,ingredients_4,ingredients_5,ingredients_6)
    return(ingredients_1,ingredients_1url,ingredients_2,ingredients_3,ingredients_4,ingredients_5,ingredients_6)

def parse_2data(ingredients_1url,headers):
    htmldata_dp = response_get(ingredients_1url,headers)
    # print(htmldata_dp)
    selector_dp = parsel.Selector(htmldata_dp)

    # 成分官方英文名称
    dp_1 = selector_dp.xpath('//*[@class="h4 text-vampire"]/text()').get()
    dp_1 = cleantext(dp_1)
    # 成分相关英文名称
    dp_2 = selector_dp.xpath('//*[@class="mb-2"]/text()').get()
    dp_2 = cleantext(dp_2)
    # 产品中文名称
    dp_3 = selector_dp.xpath('//*[@class="pb-3 mb-3 border-bottom"]/text()').get()
    dp_3 = cleantext(dp_3)
    # 分子量
    dp_4 = selector_dp.xpath('//*[@class="d-flex justify-content-between mb-3"]/div/span[1]/text()').get()
    dp_4 = cleantext(dp_4)
    # Cas No
    dp_5 = selector_dp.xpath('//*[@class="d-flex justify-content-between mb-3"]/div/span[3]/text()').get()
    dp_5 = cleantext(dp_5)
    # 说明内容
    dp_6 = selector_dp.xpath('//*[@class="linkb1 ls-2 lh-1"]/text()').get()
    dp_6 = cleantext(dp_6)
    # 参考资料
    dp_7 = selector_dp.xpath('//*[@class="text-muted mt-3"]/text()').get()
    dp_7 = cleantext(dp_7)
    print(dp_1,dp_2,dp_3,dp_4,dp_5,dp_6,dp_7)
    return dp_1,dp_2,dp_3,dp_4,dp_5,dp_6,dp_7

    # print(f'===================={i}====结束===============================')
    # break

# PART03 封装RUN #################
def run(keyword):
    csv_writer = makecsvfile()
    # 构建请求头数据
    url = 'http://www.cosdna.com/chs/ingredients.php'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.113 Safari/537.36'
    }
    Payload = {
        'q': f'{keyword}',
    }

    htmldata = response_post(url, Payload, headers)
    selector = parsel.Selector(htmldata)

    # 判断当前页面有多少条数据
    ingredients_0s = selector.xpath(f'//*[@class="chem-list"]/tr/td[1]/a/div[1]/span[1]/text()').getall()
    # print(len(ingredients_0s))
    n = len(ingredients_0s)
    for i in tqdm(range(1, n + 1)):
        ingredients_1,ingredients_1url,ingredients_2,ingredients_3,ingredients_4,ingredients_5,ingredients_6 = parse_1data(selector, i)
        dp_1,dp_2,dp_3,dp_4,dp_5,dp_6,dp_7 = parse_2data(ingredients_1url,headers)
        savetocsv(csv_writer,ingredients_1, ingredients_1url, ingredients_2, ingredients_3, ingredients_4, ingredients_5,
                  ingredients_6, dp_1, dp_2, dp_3, dp_4, dp_5, dp_6, dp_7)
######################################
keywords = readcsv()
for keyword in keywords:
    # keyword = f'水,甘油,丙二醇,山梨（糖）醇,DMDM 乙内酰脲,苯氧乙醇,丙烯酸（酯）类/C10-30 烷醇丙烯酸酯交联聚合物,三乙醇胺,甲基异噻唑啉酮,3-o-乙基抗坏血酸,透明质酸钠'
    run(keyword)
