import pprint
import parsel
import requests
import math

# 构造headers
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
        'refer': 'https://www.coupang.com/vp/products/246379487?itemId=780629226&vendorItemId=79769806875&sourceType=CATEGORY&categoryId=486148&isAddedCart=',
        }

# 构造产品链接参数
productId = "246379487"
reviews_count =3040
# 单页产品数量
review_page_size = 100
# 评论排序规格 best评论顺序：ORDER_SCORE_ASC 最近时间顺序：DATE_DESC
sortBy_review = "ORDER_SCORE_ASC"

# 排序方式  최고:5; 좋음:4; 보통:3; 별로:2; 나쁨:1;默认：空值
ratings_review = ""

# review数量按照review_page_size计算出总页数
page_review = 0

for page_review in range(1, page_review+1):
    page_review=page_review+1
    url_dp = f'https://www.coupang.com/vp/product/reviews?productId={productId}&page={page_review}&size={review_page_size}&sortBy={sortBy_review}&ratings={ratings_review}&q=&viRoleCode=2&ratingSummary=true'
    # 测试连接
    # 产品链接 https://www.coupang.com/vp/products/246379487?itemId=780629226&vendorItemId=79769806875&sourceType=CATEGORY&categoryId=486148
    # url_dp = f'https://www.coupang.com/vp/product/reviews?productId=246379487&page=3&size=5&sortBy=ORDER_SCORE_ASC&ratings={ratings_review}&q=&viRoleCode=2&ratingSummary=true'
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

    timeout = 5 # 设置超时秒数

    # 发送请求
    response = requests.get(url=url_dp, headers=headers)
    print(response)
    html_data_dp = response.text
    # pprint.pprint(html_data_dp)
    selector_reviews = parsel.Selector(html_data_dp)
    # print(selector_reviews)
    n=0
    for n_article in range(1, review_page_size+1):
        n=n+1
        print(f'================正在此采集第{page_review}页=第{n}条数据===============')
        # sdp-review__article__list__info__user__name
        review_1 = selector_reviews.xpath(f'/html/body/article[{n_article}]/div[1]/div[2]/span/text()').get()
        reviewer_id = selector_reviews.xpath(f'/html/body/article[1]/div[1]/div[2]/span[@data-member-id]/@data-member-id').get()
        # sdp-review__article__list__info__product-info__reg-date
        review_2 = selector_reviews.xpath(f'/html/body/article[{n_article}]/div[1]/div[3]/div[2]/text()').get()
        # sdp-review__article__list__info__product-info__name
        review_3 = selector_reviews.xpath(f'/html/body/article[{n_article}]/div[1]/div[4]/text()').get()
        # sdp-review__article__list__attachment__list
        review_img_lis = selector_reviews.xpath(f'/html/body/article[{n_article}]/div[2]/div/img[@src]/@src').getall()
        review_img_lis = ", ".join(review_img_lis)
        # sdp-review__article__list__headline
        # review_4 = selector_reviews.xpath(f'/html/body/article[{n_article}]/div[3]/text()').get().strip()
        review_4 = selector_reviews.xpath(f'/html/body/article[{n_article}]/div[3]/text()').get()
        if review_4 is None:
            print(type(review_4), 'review4空')
            review_4 = ""
        else:
            review_4 = review_4.strip()
            print(type(review_4), "review4非空")
        print(review_4,len(review_4))
        # review_3 = "".join(review_4)
        # class="sdp-review__article__list__survey__row__question"
        review_5_raw = selector_reviews.xpath(f'/html/body/article[{n_article}]/div[4]/div/text()').getall()
        review_5 = "".join(review_5_raw).strip()
        # print(review_1, review_2, review_3, review_4, review_5)

        # print(review_img_lis)
        print("======1===========")
        print(review_1)
        # print(reviewer_id)
        # print("======2===========")
        # print(review_2)
        # print("======3===========")
        print(review_3)
        # print("======4===========")
        # print(review_4)
        # print("======5===========")
        # print(review_5)