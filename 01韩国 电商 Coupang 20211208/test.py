#
import requests
import parsel
import json

url_detailpage_itemBrief = 'https://www.coupang.com/vp/product/reviews?productId=344529480&page=1&size=5&sortBy=ORDER_SCORE_ASC&ratings=&q=&viRoleCode=3&ratingSummary=true'
headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.113 Safari/537.36',
        }
body = {
        'productId': "344529480",
        'page': "1",
        'size': '5',
        'sortBy': 'ORDER_SCORE_ASC',
        'ratings': '',
        'q':'',
        'viRoleCode': '3',
        'ratingSummary': 'true',
        }

response_detailpage_itemBrief = requests.post(url=url_detailpage_itemBrief, headers=headers, json=body)
response_itemBrief = response_detailpage_itemBrief.text
print(response_itemBrief)
# detailpage_itemBrief_json_data = json.loads(response_itemBrief)
# print(detailpage_itemBrief_json_data)
#
# if "제품 주요 사양" not in response_itemBrief:
#     print('not')
#     bi_2 = ""
# else:
#     bi_2 = detailpage_itemBrief_json_data['essentials'][1]['description']
#     print('exist', bi_2)