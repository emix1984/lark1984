import requests
import parsel
import json

url_detailpage_itemBrief = 'https://www.coupang.com/vp/products/5735830650/items/9639246678/vendoritems/76923492094'
headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44',
        }
response_detailpage_itemBrief = requests.get(url=url_detailpage_itemBrief, headers=headers)
response_itemBrief = response_detailpage_itemBrief.text
detailpage_itemBrief_json_data = json.loads(response_itemBrief)
# print(detailpage_itemBrief_json_data)

if "제품 주요 사양" not in response_itemBrief:
    print('not')
    bi_2 = ""
else:
    bi_2 = detailpage_itemBrief_json_data['essentials'][1]['description']
    print('exist', bi_2)