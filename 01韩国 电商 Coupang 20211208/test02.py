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
def get_responsetext(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
        'referer': url
    }
    response = requests.get(url='https://www.coupang.com/vp/products/review-details', headers=headers,)
    print(response)
    html_data = response.text
    return html_data

# 读取数据
def readcsv_coupang_detailpage_data():
    # pandas 拉取 listing.csv数据中的产品详情页链接
    df_listing = pd.read_csv('03_coupang_detailpage_data.csv')
    data01 = pd.DataFrame(df_listing)
    print(f'\033[32m>>>读取listing.csv文件，进行去重操作中<<<\033[0m', '读取数据条目共计： ', len(data01), '条')
    data02 = data01.drop_duplicates("当前网址")  # 去除重复链接
    print(f'\033[32m>>>数据去重操作已完成<<<\033[0m', '去重操作数据共计： ', len(data02), '条')
    productId = data02["productId"]
    reviews_count = data02["评论数"]
    urls_detailpage = data02["当前网址"]
    print(urls_detailpage)
    return productId, reviews_count, urls_detailpage

productId, reviews_count, urls_detailpage = readcsv_coupang_detailpage_data()
# 获取评论星级评论数量
for url_detailpage in urls_detailpage:
    html_data = get_responsetext(url_detailpage)
    print('==================')
    print(html_data)

    selectors_review_details = parsel.Selector(html_data)
    # print(selectors_review_details)
    star1 = selectors_review_details.xpath('//*[@class="sdp-review__article__order__star__all__current__count js_reviewArticleCurrentStarCount1"]/text()').extract()
    star2 = selectors_review_details.xpath('//*[@class="sdp-review__article__order__star__all__current__count js_reviewArticleCurrentStarCount2"]/text()').extract()
    star3 = selectors_review_details.xpath('//*[@class="sdp-review__article__order__star__all__current__count js_reviewArticleCurrentStarCount3"]/text()').extract()
    star4 = selectors_review_details.xpath('//*[@class="sdp-review__article__order__star__all__current__count js_reviewArticleCurrentStarCount4"]/text()').extract()
    star5 = selectors_review_details.xpath('//*[@class="sdp-review__article__order__star__all__current__count js_reviewArticleCurrentStarCount5"]/div/text()').extract()
    print('star1:', star1,'star2:', star2,'star3:', star3,'star4:', star4,'star5:', star5)