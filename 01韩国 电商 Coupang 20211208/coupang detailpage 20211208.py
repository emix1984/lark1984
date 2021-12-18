import pprint
from time import sleep
import requests
import parsel
import json
import csv
import re
import time
import concurrent.futures

def get_response(html_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44',
    }
    response = requests.get(html_url, headers=headers)
    html_data_url = response.text
    return html_data_url

def get_selector(html_url):
    html_data_url = get_response(html_url)
    selector = parsel.Selector(html_data_url)
    return selector

url_detailpage = f'https://www.coupang.com/vp/products/344529480?itemId=148293960&vendorItemId=3335127002&pickType=COU_PICK&q=%EB%A1%9C%EC%85%98&itemsCount=36&searchId=b5738182b86f48b9a249acf9e1f240a3&rank=1&isAddedCart='
selector_detailpage = get_selector(url_detailpage)

# 产品名
prod_buy_header_title = selector_detailpage.xpath('//*[@id="contents"]/div[1]/div/div[3]/div[3]/h2/text()').get()
# 产品评论数
reviews_count = selector_detailpage.xpath('//*[@id="prod-review-nav-link"]/span[2]/text()').get()
# 折扣sale
discount_rate = selector_detailpage.xpath('//*[@id="contents"]/div[1]/div/div[3]/div[5]/div[1]/div/div[1]/span[1]/text()').get().strip()
# 市场价
origin_price = selector_detailpage.xpath('//*[@id="contents"]/div[1]/div/div[3]/div[5]/div[1]/div/div[1]/span[2]/text()').get()
# 销售价
prod_sale_price = selector_detailpage.xpath('//*[@id="contents"]/div[1]/div/div[3]/div[5]/div[1]/div/div[2]/span[1]/strong/text()').get()
# 每毫升克容量单价
unit_price = selector_detailpage.xpath('//*[@id="contents"]/div[1]/div/div[3]/div[5]/div[1]/div/div[2]/span[2]/text()').get()
## prod-description
# prod-description-attribute
prod_attr_item = selector_detailpage.xpath('//*[@class="prod-description"]/ul/li/text()').get()
# print(prod_attr_item)
print(prod_buy_header_title, reviews_count,discount_rate,origin_price,prod_sale_price,unit_price,)

## 通过构建下面的产品属性链接解决采集属性标签的问题
## https://www.coupang.com/vp/products/344529480/items/148293960/vendoritems/3335127002
## tab-titles
# product-item__table
prod_attr_info = selector_detailpage.xpath('//*[@id="btfTab"]/ul[2]/li[4]/div/table/tbody/tr/td/text()').get()
print('product-item__table')
print(prod_attr_info)

## 产品销售者信息 product-item__table product-seller
product_seller = selector_detailpage.xpath('//*[@id="itemBrief"]/div/table/tbody/tr[3]/td[1]/text()').get()
print('产品销售者信息 product-item__table product-seller')
print(product_seller)

## 产品review_tab请求链接
## https://www.coupang.com/vp/product/reviews?productId=344529480&page=1&size=5&sortBy=ORDER_SCORE_ASC&ratings=&q=&viRoleCode=3&ratingSummary=true

## 销售公司信息
## 与产品属性的tab在同一个json里
## https://www.coupang.com/vp/products/5735830650/items/9639246678/vendoritems/76923492094
## 从产品详情页地址可以得到productId, itemId, vendoritems.
url_detailpage_itemBrief = 'https://www.coupang.com/vp/products/5735830650/items/9639246678/vendoritems/76923492094'
response_itemBrief = get_response(url_detailpage_itemBrief)
detailpage_itemBrief_json_data = json.loads(response_itemBrief)
# pprint.pprint(detailpage_itemBrief_json_data)
# 용량 중량
# weight = detailpage_itemBrief_json_data['essentials'][0]['description']
# 제품 주요 사양
# weight = detailpage_itemBrief_json_data['essentials'][1]['description']
# 사용기한 또는 개봉 후 사용기간
# weight = detailpage_itemBrief_json_data['essentials'][2]['description']
# 사용방법
# weight = detailpage_itemBrief_json_data['essentials'][3]['description']
# 화장품제조업자 및 화장품책임판매업자
# weight = detailpage_itemBrief_json_data['essentials'][4]['description']
# 제조국
# weight5 = detailpage_itemBrief_json_data['essentials'][5]['description']
# 성분
# weight6 = detailpage_itemBrief_json_data['essentials'][6]['description']
# 기능성 화장품
# weight7 = detailpage_itemBrief_json_data['essentials'][7]['description']
# 주의사항
# weight8 = detailpage_itemBrief_json_data['essentials'][8]['description']
# 품질보증기준
# weight = detailpage_itemBrief_json_data['essentials'][9]['description']
# 소비자상담관련 전화번호
# weight = detailpage_itemBrief_json_data['essentials'][10]['description']

## returnPolicyVo 退换政策销售者公司信息
# 사업자번호
bizNum = detailpage_itemBrief_json_data['returnPolicyVo']['sellerDetailInfo']['bizNum']
# 통신판매업 신고번호
ecommReportNum = detailpage_itemBrief_json_data['returnPolicyVo']['sellerDetailInfo']['ecommReportNum']
# 사업장 소재지
repAddress = detailpage_itemBrief_json_data['returnPolicyVo']['sellerDetailInfo']['repAddress']
# e-mail
repEmail = detailpage_itemBrief_json_data['returnPolicyVo']['sellerDetailInfo']['repEmail']
# 联系人姓名
repPersonName = detailpage_itemBrief_json_data['returnPolicyVo']['sellerDetailInfo']['repPersonName']
# 연락처
repPhoneNum = detailpage_itemBrief_json_data['returnPolicyVo']['sellerDetailInfo']['repPhoneNum']
# 상호/대표자
sellerWithRepPersonName = detailpage_itemBrief_json_data['returnPolicyVo']['sellerDetailInfo']['sellerWithRepPersonName']
# 商号
vendorName = detailpage_itemBrief_json_data['returnPolicyVo']['sellerDetailInfo']['vendorName']
print(bizNum,ecommReportNum,repAddress,repEmail, repPersonName,repPhoneNum, sellerWithRepPersonName, vendorName)

pprint.pprint(detailpage_itemBrief_json_data)