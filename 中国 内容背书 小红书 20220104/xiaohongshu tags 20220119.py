# _*_ coding: utf-8 _*_
"""
Time:     20220105
Author:   LIUYING(lark1984)
Version:  V 0.1
File:     xiaohongshu.py
Describe: Github link: https://github.com/emix1984/lark1984
"""

import requests
import parsel
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

# 模块定义
def get_selector(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    }
    response = requests.get(url=url, headers=headers)
    # print(response,response.apparent_encoding)
    # response.encoding = response.apparent_encoding
    html_data = response.text
    # print(html_data)
    selector = parsel.Selector(html_data)
    return selector

def parsel_data(keyword, url, tag1, url_tag1):
    print(f'"\033[32m>>>>>>>正在解析链接\033[0m {tag1}, {url_tag1} \n')
    selector_tag1 = get_selector(url_tag1)
    tags2 = selector_tag1.xpath('//*[@id="app"]/div/div[2]/div[2]/a/text()').getall()
    urls_tags2 = selector_tag1.xpath('//*[@id="app"]/div/div[2]/div[2]/a[@href]/@href').getall()
    zipdata_tags2 = zip(tags2, urls_tags2)

    # note-title
    note_1s = selector_tag1.xpath('//*[@id="app"]/div/div[4]/div/div/div/h3/text()').getall()
    # note-cover cube-image normal-image
    # note_2s = selector_tag1.xpath('//*[@id="app"]/div/div[4]/div[1]/div[4]/a/div/img[@src]/@src').get()
    # links
    note_2s = selector_tag1.xpath('//*[@id="app"]/div/div[4]/div/div/a[@href]/@href').getall()
    # note-author-nickname
    note_3s = selector_tag1.xpath('//*[@id="app"]/div/div[4]/div/div/div[2]/div/a/text()').getall()
    # note-likes-icon
    note_4s = selector_tag1.xpath('//*[@id="app"]/div/div[4]/div/div/div[2]/span/text()').getall()
    # note-author-links
    note_5s = selector_tag1.xpath('//*[@id="app"]/div/div[4]/div/div/div[2]/div/a[@href]/@href').getall()
    # note-author-img
    note_6s = selector_tag1.xpath('//*[@id="app"]/div/div[4]/div/div/div[2]/div/div/div[1]/img[@src]/@src').getall()

    zipdata1 = zip(note_1s, note_2s, note_3s, note_4s, note_5s, note_6s)

    for note_1, note_2, note_3, note_4, note_5, note_6 in zipdata1:
        note_2 = 'https://www.xiaohongshu.com' + note_2
        note_4 = note_4.strip()
        note_5 = 'https://www.xiaohongshu.com' + note_5
        print(f'>>>正在保存数据=', keyword, url, tag1, url_tag1, note_1, note_2, note_3, note_4, note_5, note_6)
        with open('./datawarehouse/tags_data.csv', mode='a', encoding='utf-8', newline="") as f:
            csv_write = csv.writer(f)
            csv_write.writerow([keyword, url, tag1, url_tag1, note_1, note_2, note_3, note_4,note_5, note_6])
    return zipdata_tags2

def run(tag1, url_tag1):
    tag1 = tag1.strip()
    url_tag1 = 'https://www.xiaohongshu.com' + url_tag1
    zipdata_tags2 = parsel_data(keyword, url, tag1, url_tag1)
    for tag2, url_tag2 in zipdata_tags2:
        tag2 = tag2.strip()
        url_tag2 = 'https://www.xiaohongshu.com' + url_tag2
        zipdata_tags3 = parsel_data(tag1, url_tag1, tag2, url_tag2)
        for tag3, url_tag3 in zipdata_tags3:
            tag3 = tag3.strip()
            url_tag3 = 'https://www.xiaohongshu.com' + url_tag3
            parsel_data(tag2, url_tag2, tag3, url_tag3)
            # zipdata_tags4 = parsel_data(tag2, url_tag2, tag3, url_tag3)

# #####################正式运行##########################################
keyword = input('输入关键词： ')
# keyword = 'abib'
url = f'https://www.xiaohongshu.com/mobile/tags/0?name={keyword}'

selector = get_selector(url)
tags1 = selector.xpath('//*[@id="app"]/div/div[2]/div[2]/a/text()').getall()
urls_tags1 = selector.xpath('//*[@id="app"]/div/div[2]/div[2]/a[@href]/@href').getall()
zipdata_tags1 = zip(tags1, urls_tags1)

# 乱序多线程
with ThreadPoolExecutor() as pool:
    futures = [pool.submit(run, tag1, url_tag1) for tag1, url_tag1 in zipdata_tags1]
    # futures = [pool.submit(run, tag1, url_tag1) for tag1, url_tag1 in zipdata_tags1]
    for future in futures:
        print('线程是否有错误程结果：', future.result())
    for future in as_completed(futures):
        print('线程结果：', future.result())