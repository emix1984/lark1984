# _*_ coding: utf-8 _*_
"""
Time:     2022/1/24 18:03
Author:   LIU YING(天蝎座数据)
Version:  V 0.1
File:     台湾屈臣氏 all-brands urls 20220124.py
Describe: Write during the internship at Hikvison, Github link: https://github.com/Deeachain/GraphEmbeddings
"""

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
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import math

################################
# 定义模块
# 获取源码数据

def get_responseget(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.137 Safari/537.36',
        'referer': 'https://www.watsons.com.tw/',
    }
    Parameters = {
        'fields': 'FULL',
        'lang': 'zh_TW',
        'curr': 'TWD',
    }
    response = requests.get(url=url, headers=headers, params=Parameters)
    # print(response,response.apparent_encoding)
    response.encoding = response.apparent_encoding
    html_data = response.text
    return html_data

# 文件名称用时间戳
timeforfile = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
timeforfile_lis = re.findall(r"\d+\.?\d*",timeforfile)
timeforfile_str = "".join(timeforfile_lis)

# 创建csv文件和表头
f = open(f'watsons_allbrand_{timeforfile_str}.csv', mode='a', encoding='utf-8', newline='')
print(f'\033[32m>>> 创建数据库完毕 <<<\033[0m')
csv_writer = csv.DictWriter(f, fieldnames=[
    '关键词',
    '关键词网址',
    '采集当前时间',
])
csv_writer.writeheader()

# url = 'https://www.watsons.com.tw/b/brandlist'
url = 'https://api.watsons.com.tw/api/v2/wtctw/brands?fields=FULL&lang=zh_TW&curr=TWD'
html_data = get_responseget(url)
json_data = json.loads(html_data)
items = json_data['brands']

for item in tqdm(items):
    # print(item)
    brand = item['name']
    brandUrl = item['brandUrl']
    brandUrl = 'https://www.watsons.com.tw'+brandUrl
    # abrand = item['abrand']

    # 写入时间
    rightnow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 存储到字典文件
    dict = {
        '关键词': brand,
        '关键词网址': brandUrl,
        '采集当前时间': rightnow,
    }
    csv_writer.writerow(dict)
    print(brand,brandUrl,rightnow)
