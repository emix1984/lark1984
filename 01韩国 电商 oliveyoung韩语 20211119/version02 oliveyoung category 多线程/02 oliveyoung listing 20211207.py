# 第二步解决问题
# 1 解决三级分类链接下的产品数量采集
# 2 解决页面生成逻辑
# 3 采集产品详情页链接
# 下面是示例链接，按照符号& 进行换行处理
# dispCatNo=类别编码；&prdSort=01默认01是按照人气排序方式；pageIdx=1页码第一页；trackingCd=Cat1000001000100080001_Small这是追踪用记得要和分类编码组合使用
# https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=1000001000100080001
# &fltDispCatNo=
# &prdSort=01
# &pageIdx=1
# &rowsPerPage=24
# &searchTypeSort=btn_thumb
# &plusButtonFlag=N
# &isLoginCnt=0
# &aShowCnt=
# &bShowCnt=
# &cShowCnt=
# &trackingCd=Cat1000001000100080001_Small

from time import sleep
import requests
import parsel
import csv
import re
import time
import concurrent.futures

def get_response(html_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.99 Safari/537.36',
        'Connection': 'close'
    }
    response = requests.get(html_url, headers=headers)
    html_data_url = response.text
    return html_data_url

def get_selector(html_url):
    html_data_url = get_response(html_url)
    selector = parsel.Selector(html_data_url)
    return selector
def open_csv_data():
    # 创建csv文件和表头
    f = open('02_oliveyoung_listing.csv', mode='a', encoding='utf-8', newline='')
    csv_writer = csv.DictWriter(f, fieldnames=[
    '三级类目名称',
    '三级类目编码',
    '三级类目产品数',
    '页码',
    '产品编码',
    '产品链接',
    '采集时间',
    ])
    csv_writer.writeheader()

    # 项目计时用
    time_1 = time.time()

    # 时间戳
    rightnow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def parse_data(category2_names, category2_codes):
    for category2_name, category2_code in zip(category2_names,category2_codes):
        url_category_2 = f'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo={category2_code}&isLoginCnt=1&aShowCnt=0&bShowCnt=0&cShowCnt=0&gateCd=Drawer&trackingCd=Cat{category2_code}_MID'

        # 发送请求
        selector_html_data_category_2 = get_selector(url_category_2)

        category3_names = selector_html_data_category_2.xpath('//*[@id="Contents"]/ul[1]/li/a/text()').getall()
        category3_codes = selector_html_data_category_2.xpath('//*[@id="Contents"]/ul[1]/li/a[@class]/@class').getall()

        for category3_name, category3_code in zip(category3_names, category3_codes):
            url_category_3 = f'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo={category3_code}&fltDispCatNo=&prdSort=01&pageIdx=1&rowsPerPage=24&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat{category3_code}_Small'

            # 发送请求
            selector_html_data_category_3 = get_selector(url_category_3)
            # print(html_data_category_3)
            number_raw = selector_html_data_category_3.xpath('//*[@id="Contents"]/p/span/text()').getall()[0]
            number = number_raw.strip()
            page_number = int(int(number) / 48) + 1
            # print(category2_name, category3_name, category3_code, number, page_number)

            for page in range(1, page_number+1): # 因为range函数计算的是区间，开始的数字是1，所以计算出来的页码+1
                print(f'==================正在爬取', category2_name, category3_name, f'第{page}页内容=======================')
                prdSort = "3" # 产品列表按照01人气排序；02最新登录排序；03按照销量排序；04按照最低价格排序；05按照最高价格排序
                rowsPerPage = "48" # 每页显示产品数 24, 36, 48
                url = f'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo={category3_code}&fltDispCatNo=&prdSort={prdSort}&pageIdx={page}&rowsPerPage={rowsPerPage}&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=1&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat{category3_code}_Small'
                # sleep(3)  # 等待页面加载3秒
                html_data = get_response(url)
                # print(html_data)

                urls = re.findall('<div class="prd_info "><a href="(.*?)"', html_data)

                # 采集到的三级分类category，和category3进行比对是否存在错，确认用
                category_raw = re.findall('<p class="cate_info_tx">(.*?) .*?', html_data, re.S)[0]
                category = category_raw.strip()

                # 采集到的三级分类下产品数量
                number_raw = re.findall('<span>(.*?)</span>', html_data, re.S)[11]
                number = number_raw.strip()

                for d_url in urls:
                    prd_name_number = re.findall(r'goodsNo=(.*?)&', d_url)[0]
                    print(category, page_number, number, prd_name_number)

                    # 建立字典存储到文件
                    dict = {
                        '三级类目名称': category3_name,
                        '三级类目编码': category3_code,
                        '三级类目产品数': number,
                        '页码': page_number,
                        '产品编码': prd_name_number,
                        '产品链接': d_url,
                        '采集时间': rightnow,
                    }
                    print(rightnow, '....正在采集：', category2_name, category3_name, page, "/", page_number)
                    csv_writer.writerow(dict)
            print(f'===采集完成===累计耗时：', time.time() - time_1, rightnow)

#
def run():
    # 配置oliveyoung主页地址，浏览器基础信息
    url_start = f'https://www.oliveyoung.co.kr/store/company/brandStory.do'
    selector_start = get_selector(url_start)
    # 解析html代码，获取主要分类名称和编码
    category2_names = selector_start.xpath('//*[@id="gnbAllMenu"]/ul/li[1]/div/ul/li/a/text()').getall()
    category2_codes = selector_start.xpath(
        '//*[@id="gnbAllMenu"]/ul/li[1]/div/ul/li/a[@data-ref-dispcatno]/@data-ref-dispcatno').getall()
    parse_data(category2_names, category2_codes)

#
# # time_1 = time.time()
# # for page in range(1,11):
# #     run(f'https://www.fabiaoqing.com/biaoqing/lists/page/{page}.html')
# # print(f'总耗时，{time.time() - time_1}')
#
# if __name__ == '__main__':
#     time_1 = time.time()
#     # concurrent.futures模块提供了两种executor的子类，ThreadPoolExecutor各自独立操作一个线程和 ProcessPoolExecutor一个进程池
#     exe = concurrent.futures.ThreadPoolExecutor(max_workers=10)
#     # exe = concurrent.futures.ProcessPoolExecutor(max_workers=10)
#     for page in range(1, 11):
#         url = f'https://www.fabiaoqing.com/biaoqing/lists/page/{page}.html'
#         exe.submit(run, url)
#     exe.shutdown()
#     print(f'总耗时:{time.time()-time_1}')