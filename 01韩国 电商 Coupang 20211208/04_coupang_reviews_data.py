import pprint

import parsel
import requests

url_dp = f'https://www.coupang.com/vp/product/reviews?productId=246379487&page=3&size=5&sortBy=ORDER_SCORE_ASC&ratings=&q=&viRoleCode=2&ratingSummary=true'
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
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    'refer': 'https://www.coupang.com/vp/products/246379487?itemId=780629226&vendorItemId=79769806875&sourceType=CATEGORY&categoryId=486148&isAddedCart=',
    }
timeout = 5 # 设置超时秒数

# 发送请求
response = requests.get(url=url_dp, headers=headers)
html_data_dp = response.text
pprint.pprint(html_data_dp)
selector_reviews = parsel.Selector(html_data_dp)
# print(selector_reviews)

# sdp-review__article__list__info__user__name
review_1 = selector_reviews.xpath('/html/body/article/div[1]/div[2]/span/text()').getall()
# sdp-review__article__list__info__product-info__reg-date
review_2 = selector_reviews.xpath('/html/body/article/div[1]/div[3]/div[2]/text()').getall()
# sdp-review__article__list__info__product-info__name
review_3 = selector_reviews.xpath('/html/body/article/div[1]/div[4]/text()').getall()
# sdp-review__article__list__review__content js_reviewArticleContent
review_4 = selector_reviews.xpath('/html/body/article[1]/div[3]/div/text()[1]').get()
# review_3 = "".join(review_4)
# class="sdp-review__article__list__survey__row__question"
review_5 = selector_reviews.xpath('/html/body/article[1]/div[4]/div[1]/span[1]/text()').getall()
# print(review_1, review_2, review_3, review_4, review_5)
print(review_4, review_5)