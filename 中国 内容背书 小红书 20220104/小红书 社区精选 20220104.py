import json
import pprint
from time import sleep
import requests
import parsel
import csv
import re
import time
import concurrent.futures


url = f'https://www.xiaohongshu.com/explore'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.113 Safari/537.36',
    'referer': 'https://www.xiaohongshu.com/explore',
}
def get_responsetext(url,headers):
    response = requests.get(url=url, headers=headers)
    htmldata = response.text
    return htmldata

def get_selector(url, headers):
    htmldata = get_responsetext(url, headers)
    # pprint.pprint(htmldata)
    # print('====打印结束===')
    selector = parsel.Selector(htmldata)
    return selector

selector_explore = get_selector(url, headers)
# 提取数据
titles = selector_explore.xpath('//*[@id="app"]/div/div[2]/div[1]/div/div/div/div/div/a/text()').getall()
title_links = selector_explore.xpath('//*[@id="app"]/div/div[2]/div[1]/div/div/div/div/div[1]/a[@href]/@href').getall()
# title_link = 'https://www.xiaohongshu.com' + title_link_raw
user_names = selector_explore.xpath('//*[@id="app"]/div/div[2]/div[1]/div/div/div/div/div[2]/div[1]/span/text()').getall()
user_imgs = selector_explore.xpath('//*[@id="app"]/div/div[2]/div[1]/div/div/div/div/div[2]/div[1]/div/img[@src]/@src').getall()
title_imgs = selector_explore.xpath('//*[@id="app"]/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/img[@src]/@src').getall()
title_likes = selector_explore.xpath('//*[@id="app"]/div/div[2]/div[1]/div/div/div/div/div[2]/div[2]/span/text()').getall()
zipdata = zip(titles,title_links,user_names,user_imgs,title_imgs,title_likes)

for title,title_link,user_name,user_img,title_img,title_like in zipdata:
    title_link = 'https://www.xiaohongshu.com' + title_link
    # print(title,title_link,user_name,user_img,title_img,title_like)
    print(title_link)
    # 遇到小红书加密数据 20220104 等待需要解决

    json_discovery = get_responsetext(title_link, headers)
    # selector_discovery = json.loads(json_discovery)
    pprint.pprint(json_discovery)
    # note_raw = selector_explore.xpath('//*[@class="left-card"]/main/div/p/text()').get()
    note_raw = selector_explore.xpath('//*[@id="app"]/div/div[2]/div[1]/div[6]/div[1]/div[1]/p/text()').get()
    # note = "".join(note_raw)
    print(note_raw)
    break