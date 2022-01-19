# 测试连接
# 产品链接 https://www.coupang.com/vp/products/246379487?itemId=780629226&vendorItemId=79769806875&sourceType=CATEGORY&categoryId=486148
# url_dp = f'https://www.coupang.com/vp/product/reviews?productId=246379487&page=3&size=5&sortBy=ORDER_SCORE_ASC&ratings=&q=&viRoleCode=2&ratingSummary=true'
# payload = {
# 'productId': '4880173278',
# 'page': '3',
# 'size': '5',
# 'sortBy': 'ORDER_SCORE_ASC',
# 'ratings': '',
# 'q':'',
# 'viRoleCode': '3',
# 'ratingSummary': 'true',
# }


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
    # print(response)
    html_data = response.text
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


def pasel_coupang_dp_reviews(url_detailpage,csv_writer):
    print(f'正在解析产品详情页链接： {url_detailpage}')
    # 通过网址提取 productId
    productId = re.findall(f'products/(.*?)\?', url_detailpage)[0]
    # print(productId)

    # 排序方式  최고:5; 좋음:4; 보통:3; 별로:2; 나쁨:1;默认：空值
    ratings_review_options =["", "1", "2", "3", "4", "5"]

    for ratings_review_option in ratings_review_options:
        # ratings_review = ""

        # review数量按照review_page_size计算出总页数
        # coupang限制采集买后评论的页数为10页
        page_review_allowed = 10
        for page_review in range(1, page_review_allowed+1):
            url_dp_review = f'https://www.coupang.com/vp/product/reviews?productId={productId}&page={page_review}&size={review_page_size}&sortBy={sortBy_review}&ratings={ratings_review_option}&q=&viRoleCode=2&ratingSummary=true'
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
                'refer': 'https://www.coupang.com/vp/products/246379487?itemId=780629226&vendorItemId=79769806875&sourceType=CATEGORY&categoryId=486148&isAddedCart=',
            }
            # 发送请求
            response = requests.get(url=url_dp_review, headers=headers)
            print(response)
            html_data_dp = response.text
            selector_reviews = parsel.Selector(html_data_dp)

            # 分别按照评级和评论数判断存储
            if ratings_review_option == "":
                review_starname = "모든 별점"
                review_starcount = selector_reviews.xpath(f'/html/body/div[2][@data-total-count]/@data-total-count').get()
            elif ratings_review_option == "5":
                review_starname = "최고"
                review_starcount = selector_reviews.xpath(f'/html/body/div[1]/div[1][@data-count]/@data-count').get()
            elif ratings_review_option == "4":
                review_starname = "좋음"
                review_starcount = selector_reviews.xpath(f'/html/body/div[1]/div[2][@data-count]/@data-count').get()
            elif ratings_review_option == "3":
                review_starname = "보통"
                review_starcount = selector_reviews.xpath(f'/html/body/div[1]/div[3][@data-count]/@data-count').get()
            elif ratings_review_option == "2":
                review_starname = "별로"
                review_starcount = selector_reviews.xpath(f'/html/body/div[1]/div[4][@data-count]/@data-count').get()
            elif ratings_review_option == "1":
                review_starname = "나쁨"
                review_starcount = selector_reviews.xpath(f'/html/body/div[1]/div[5][@data-count]/@data-count').get()
            else:
                continue

            n=0
            # 单页面逐条采集数据
            for n_article in range(1, review_page_size+1):
                n=n+1
                print(f'================正在此采集第 {page_review} 页 第 {n} 条数据====标签: {review_starname}===========\t')
                # sdp-review__article__list__info__user__name
                review_username = selector_reviews.xpath(f'/html/body/article[{n_article}]/div[1]/div[2]/span/text()').get()
                reviewer_userid = selector_reviews.xpath(f'/html/body/article[{n_article}]/div[1]/div[2]/span[@data-member-id]/@data-member-id').get()

                # 判断用户id为空值时跳出循环
                if reviewer_userid is None:
                    print(f"在本页 {url_dp_review} 第 {n_article} 找不到任何数据跳过 '\t'")
                    break
                else:
                    # 用户头像 sdp-review__article__list__info__profile
                    reviewer_userico = selector_reviews.xpath(f'/html/body/article[{n_article}]/div[1]/div[1]/img[@src]/@src').get()
                    # 评论日期 sdp-review__article__list__info__product-info__reg-date
                    review_recorddate = selector_reviews.xpath(f'/html/body/article[{n_article}]/div[1]/div[3]/div[2]/text()').get()
                    # 用户名称 sdp-review__article__list__info__product-info__name
                    review_productname = selector_reviews.xpath(f'/html/body/article[{n_article}]/div[1]/div[4]/text()').get()
                    # 图片附件链接 sdp-review__article__list__attachment__list
                    review_img_lis = selector_reviews.xpath(f'/html/body/article[{n_article}]/div[2]/div/img[@src]/@src').getall()
                    review_img_lis = ", ".join(review_img_lis)
                    # 评论主题 sdp-review__article__list__headline
                    review_headline = selector_reviews.xpath(f'/html/body/article[{n_article}]/div[3]/text()').get()
                    if review_headline is None:
                        review_headline = ""
                    else:
                        review_headline = review_headline.strip()
                    # class="sdp-review__article__list__survey__row__question"
                    review_5_raw = selector_reviews.xpath(f'/html/body/article[{n_article}]/div[4]/div/text()').getall()
                    review_5 = "".join(review_5_raw).strip()
                    # 몇 명에게 되움 됨 sdp-review__article__list__help__count 20220111追加，coupang算法数字越大，review排名越靠前，可参考性越高
                    review_6 = selector_reviews.xpath(f'/html/body/article[{n_article}]/div[6]/div[1]/strong/span/text()').get()
                    # 翻页 页码+1
                    page_review = page_review + 1
                    # print(productId, review_starname, reviewer_userid, review_recorddate, url_dp_review, review_5)

                    # 时间戳
                    rightnow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    # 存储到字典文件
                    dict = {
                        'productId': productId,
                        'review_productname': review_productname,
                        'review_starname': review_starname,
                        'review_starcount': review_starcount,
                        'review_userid': reviewer_userid,
                        'review_username': review_username,
                        'review_user头像': reviewer_userico,
                        'review_date': review_recorddate,
                        'review_title': review_headline,
                        'review_评论图': review_img_lis,
                        'review_contents': review_5,
                        'review_helpcont': review_6,
                        '当前评论页面': url_dp_review,
                        '产品详情页网址': url_detailpage,
                        '当前时间': rightnow,
                    }
                    csv_writer.writerow(dict)
                    print(f'\033[31m时间：\033[0m', rightnow, f'\033[00;42m>>>写入数据：\033[0m', 'productId：', productId, '用户名称：', review_username, '主题：', review_headline, '\t')

####################################################################################
###开始运行代码

csv_writer = makecsvfile()
urls_detailpage = readcsv_coupang_detailpage_data()

# 构造产品链接参数
# productId = "246379487"

# 单页产品数量
review_page_size = 100
# 评论排序规格 best评论顺序：ORDER_SCORE_ASC 最近时间顺序：DATE_DESC
sortBy_review = "ORDER_SCORE_ASC"
# 项目计时用
# time_start = time.time()
# max_worker 是进程/线程数, 默认为 CPU 核心数
with ThreadPoolExecutor(max_workers=2000) as pool:
    futures = [pool.submit(pasel_coupang_dp_reviews, url_detailpage,csv_writer)
               for url_detailpage in urls_detailpage ]

    for future in futures:
        print('线程是否有错误程结果：', future.result())
    for future in as_completed(futures):
        print('线程结果：', future.result())
