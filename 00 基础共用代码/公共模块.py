from selenium.webdriver import Chrome, ChromeOptions # 配置chromedriver无界面方式
from selenium.webdriver.chrome.service import Service # 升级后webdriver配置chromedriver.exe为服务
from selenium.webdriver.common.by import By # python3.6 升级到 3.8后定位元素的方式变动
import pprint
import parsel
import requests
import pandas as pd
import requests
import parsel
import json
import csv
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import math

################################
# 定义模块
# 获取源码数据
def get_responseget(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
        'referer': url
    }
    response = requests.get(url='https://www.coupang.com/vp/products/review-details', headers=headers,)
    # print(response,response.apparent_encoding)
    response.encoding = response.apparent_encoding
    html_data = response.text
    return html_data

def get_selenium(url):
    # 配置浏览器基本信息
    headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.99 Safari/537.36'
        }
    opt = ChromeOptions()
    opt.headless = True
    s = Service(r"D:\lark1984\selenium\chromedriver.exe")
    driver_dp = Chrome(service=s, options=opt)

    sleep(3) # 等待页面加载3秒
    driver_dp.get(url=url, headers=headers)
    html_data = driver_dp.page_source # 转换页面源代码
    # print(html_data)
    return html_data

# 创建csv文件和表头
def makecsvfile():
    f = open('04_oliveyoung_detailpage_reviewsdata_test1.csv', mode='a', encoding='utf-8', newline='')
    print(f'\033[32m>>>创建csv文件完毕！！！<<<\033[0m')
    csv_writer = csv.DictWriter(f, fieldnames=[
                                            'productId',
                                            'review_productname',
                                            'review_starname',
                                            'review_starcount',
                                            'review_userid',
                                            'review_username',
                                            'review_user头像',
                                            'review_date',
                                            'review_title',
                                            'review_评论图',
                                            'review_contents',
                                            'review_helpcont',
                                            '当前评论页面',
                                            '产品详情页网址',
                                            '当前时间',
                                            ])
    csv_writer.writeheader()
    print(f'\033[32m>>> csv文件<表头>写入完毕 <<<\033[0m')
    return csv_writer

# 读取数据
def readcsv_coupang_detailpage_data():
    # pandas 拉取 listing.csv数据中的产品详情页链接
    df_listing = pd.read_csv('03_coupang_detailpage_data.csv')
    data01 = pd.DataFrame(df_listing)
    print(f'\033[32m>>>读取listing.csv文件完毕<<<\033[0m', '读取数据条目共计： ', len(data01), '条')
    urls_detailpage = data01["当前网址"]
    # print(urls_detailpage)
    # print('================')
    return urls_detailpage