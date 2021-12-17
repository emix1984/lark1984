# 采集oliveyoung韩文<뷰티>类目下，
# 二级分类编码，并且拼合二级分类的网站地址
# 三级分类编码，并且拼合三级分类网站地址
# 获得三级分类地址里产品总数以及总页数
# _*_ coding:utf8 _*_
# @author：liuying
# date：2021-11-19
# version 02

import requests
import parsel
import csv
import re
import time

# 创建csv文件和表头
f = open('01_oliveyoung_category.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
            '一级分类名称',
            '一级分类编码',
            '二级分类名称',
            '二级分类编码',
            '三级分类名称',
            '三级分类编码',
            '三级分类链接',
            '产品数量',
            '48产品页数',
            '采集时间',
])
csv_writer.writeheader()

# 项目计时用
time_1 = time.time()

# 配置oliveyoung主页地址，浏览器基础信息
url = f'https://www.oliveyoung.co.kr/store/main/main.do?oy=0'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.113 Safari/537.36',
    'Connection': 'close'
}
# 发送请求
response = requests.get(url=url, headers=headers)
html_data = response.text

# 解析html代码，获取主要分类名称和编码
selector = parsel.Selector(html_data)
category1_names = selector.xpath('//*[@id="gnbAllMenu"]/ul/li[1]/div/p/a/text()').getall()
category1_codes = selector.xpath('//*[@id="gnbAllMenu"]/ul/li[1]/div/p/a[@data-ref-dispcatno]/@data-ref-dispcatno').getall()
# print(category1_names, category1_codes)

# 获取二级分类名称和编码
for category1_name, category1_code in zip(category1_names, category1_codes):
    print(category1_name, category1_code)
    category1_url = f"https://www.oliveyoung.co.kr/store/display/getCategoryShop.do?dispCatNo={category1_code}&gateCd=Drawer"
    print(category1_url)
    # 发送一级级分类地址请求，解析html代码，获得三级分类名称和编码
    response_category1 = requests.get(url=category1_url, headers=headers)
    html_data_category1 = response_category1.text

    # 解析html代码，获取主要分类名称和编码
    selector_category1 = parsel.Selector(html_data_category1)
    category2_names = selector_category1.xpath('//*[@id="Contents"]/div/div[1]/ul/li/a/span/text()').getall()
    category2_codes = selector_category1.xpath('//*[@id="Contents"]/div/div[1]/ul/li/a[@class]/@class').getall()
    # print(category2_names, category2_codes)

    for category2_name,category2_code in zip(category2_names,category2_codes):
        # 拼合二级分类网页网址，打开网址并获得三级分类名称和编码
        # print(category1_name, category1_code, category2_name, category2_code) # 打印显示一级分类和二级分类的名称和code组合
        category2_url = f"https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo={category2_code}&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat{category2_code}_MID"
        # print(category2_url)

        # 发送二级分类地址请求，解析html代码，获得三级分类名称和编码
        response_category2 = requests.get(url=category2_url, headers=headers)
        html_data_category2 = response_category2.text
        selector_category2 = parsel.Selector(html_data_category2)
        category3_names = selector_category2.xpath('//*[@id="Contents"]/ul[1]/li/a/text()').getall()
        category3_codes = selector_category2.xpath('//*[@id="Contents"]/ul[1]/li/a[@class]/@class').getall()

        # 拼合三级分类的地址，获得分类下的产品数量以及按照每页48个产品的展示下有多少页
        for category3_name, category3_code in zip(category3_names, category3_codes):
            category3_url = f'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo={category3_code}&fltDispCatNo=&prdSort=01&pageIdx=1&rowsPerPage=24&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat{category3_code}_Small'
            response_category3 = requests.get(url=category3_url, headers=headers)
            html_data_category3 = response_category3.text
            number_raw = re.findall('<span>(.*?)</span>', html_data_category3, re.S)[11]
            number = number_raw.strip()
            page_number = int(int(number)/48) + 1
            # print(number, page_number)

            # 时间戳
            rightnow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # 建立字典存储到文件
            dict = {
                '一级分类名称': category1_name,
                '一级分类编码': category1_code,
                '二级分类名称': category2_name,
                '二级分类编码': category2_code,
                '三级分类名称': category3_name,
                '三级分类编码': category3_code,
                '三级分类链接': category3_url,
                '产品数量': number,
                '48产品页数': page_number,
                '采集时间': rightnow,
                    }
            print(rightnow, '....正在采集：', category1_name, category2_name, category3_name)
            csv_writer.writerow(dict)
    print(f'★★★采集完成★★★ 累计耗时：，{time.time() - time_1}')