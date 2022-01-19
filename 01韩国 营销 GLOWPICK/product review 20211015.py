import json
from time import sleep
import time
import random
import requests
import parsel
from tqdm import tqdm
import re
import csv
import pandas as pd
from selenium.webdriver import Chrome, ChromeOptions # 配置chromedriver无界面方式
from selenium.webdriver.chrome.service import Service # 升级后webdriver配置chromedriver.exe为服务
from selenium.webdriver.common.by import By # python3.6 升级到 3.8后定位元素的方式变动

################################
# 定义模块
# 获取源码数据
def response_get(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2NDE5Njc2NTksImV4cCI6MTY0MjA1NDA1OX0.iGYk - q7egiHDGY7pO2PdQ2RYDyOYy4KZjp1Lw0xKTUg',
        'origin': 'https://www.glowpick.com',
        'referer': 'https://www.glowpick.com/',
    }
    params = {
        'type': 'product_id',
        'value': '151498',
    }
    response = requests.get(url=url, headers=headers,params=params)
    print(response, response.apparent_encoding)
    response.encoding = response.apparent_encoding
    html_data = response.text
    return html_data

def get_selenium(url):
    # 配置浏览器基本信息
    headers = {
            ':authority': '20vxjueund.execute-api.ap-northeast-2.amazonaws.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.99 Safari/537.36'
        }
    opt = ChromeOptions()
    opt.headless = True
    s = Service(r"D:\lark1984\selenium\chromedriver.exe")
    driver_dp = Chrome(service=s, options=opt)

    sleep(3) # 等待页面加载3秒
    driver_dp.get(url=url)
    html_data = driver_dp.page_source # 转换页面源代码
    # print(html_data)
    return html_data


################################

# url = 'https://www.glowpick.com/products/151498'
url = 'https://20vxjueund.execute-api.ap-northeast-2.amazonaws.com/production/system/dynamic-link/short?type=product_id&value=151498'


response = response_get(url)
print(response)