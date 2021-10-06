import requests
import parsel
import pprint

import urllib3.util.proxy

url = 'https://www.coupang.com/vp/product/reviews?productId=133257156&page=3&size=5&sortBy=ORDER_SCORE_ASC&ratings=&q=&viRoleCode=3&ratingSummary=true'
headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.99 Safari/537.36'
        }

response = requests.get(url=url, headers=headers)
html_data = response.text

selector = parsel.Selector(html_data)
# lis = selector.css('body > article').getall()
lis = selector.css('body > article > div.sdp-review__article__list__info').getall()

for li in lis:
    user5 = li.css('div > div.sdp-review__article__list__info__user > span::text').get()
    print(user5)