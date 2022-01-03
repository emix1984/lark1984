import pprint
import re
import requests
import parsel
import json
from pandas.core.frame import DataFrame

# 获取网址源码数据json
def responsetxt_coupang(productid,itemsid,vendoritemsid):
        url_detailpage_itemBrief = f'https://www.coupang.com/vp/products/{productid}/items/{itemsid}/vendoritems/{vendoritemsid}'
        headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44',
        }
        response_detailpage_itemBrief = requests.get(url=url_detailpage_itemBrief, headers=headers)
        response_itemBrief = response_detailpage_itemBrief.text
        return response_itemBrief

# 判断是否存在产品信息属性的模块
def product_essential_info(response_itemBrief,title):
    # print(type(response_itemBrief),response_itemBrief)
    detailpage_itemBrief_json_data = json.loads(response_itemBrief)
    lis_essentials = detailpage_itemBrief_json_data['essentials']
    for bi in lis_essentials:
        # print(bi.values())
        if title not in bi['title']:
            b1 = "kongzhi"
            continue
        else:
            b1 = bi['description']
            # print(b1)
            # print(bi['description'])
            break
    # print('最终结果返回值',b1)
    return b1


productid = '5735830650'
itemsid = '9639246678'
vendoritemsid = '76923492094'

response_itemBrief = responsetxt_coupang(productid,itemsid,vendoritemsid)

title1 = "용량(중량)"
b1=product_essential_info(response_itemBrief,title1)
print('====용량(중량)1====')
print(b1)


title2 = "용량(중량)"
b2=product_essential_info(response_itemBrief,title2)
print('====용량(중량)====')
print(b2)


# 사용할 때 주의사항
title3 = "사용할 때 주의사항"
b3=product_essential_info(response_itemBrief,title3)
print('====사용할 때 주의사====')
print(b3)
print(b1, b2, b3)