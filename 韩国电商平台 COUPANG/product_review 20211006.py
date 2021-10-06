import requests
import parsel
import re

import urllib3.util.proxy

url = 'https://www.coupang.com/vp/product/reviews?productId=133257156&page=3&size=5&sortBy=ORDER_SCORE_ASC&ratings=&q=&viRoleCode=3&ratingSummary=true'
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.99 Safari/537.36'
        }

response = requests.get(url=url, headers=headers)
html_data = response.text

selector = parsel.Selector(html_data)
title = re.findall('<span class="sdp-review__article__list__info__user__name js_reviewUserProfileImage" data-member-id=".*?">(.*?)</span>', selector)[0]
print(title)
print('===================================')

lis = selector.css('body > article > div.sdp-review__article__list__info > div.sdp-review__article__list__info__user > span::text').getall()
print(lis)
print('===================================')
for li in lis:
    title = re.findall('<span class="sdp-review__article__list__info__user__name js_reviewUserProfileImage" data-member-id=".*?">(.*?)</span>', li)[0]
    print(title)