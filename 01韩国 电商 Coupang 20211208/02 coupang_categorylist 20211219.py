import pprint
from time import sleep
import requests
import parsel
import json
import csv
import re
import time
import concurrent.futures

url_homepage = f'https://www.coupang.com/'
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44',
    }
response_homepage = requests.get(url=url_homepage, headers=headers)
html_data_homepage = response_homepage.text
selector_hompage = parsel.Selector(html_data_homepage)

# 美妆
category1_name = selector_hompage.xpath('//*[@id="gnbAnalytics"]/ul[1]/li[2]/a/text()').get()
# 全部主分类
# category_main = selector_hompage.xpath('//*[@id="gnbAnalytics"]/ul[1]/li/a/text()').getall()

category2_names = selector_hompage.xpath('//*[@id="gnbAnalytics"]/ul[1]/li[2]/div/div/ul/li/a/text()').getall()
category2_codes = selector_hompage.xpath('//*[@id="gnbAnalytics"]/ul[1]/li[2]/div/div/ul/li/a[@href]/@href').getall()
zipdata_category2 = zip(category2_names, category2_codes)

for category2_name, category2_code_raw in zipdata_category2:
    category2_code = category2_code_raw.replace("/np/categories/", "")
    # print(category2_code)
    url_category2 = f'https://www.coupang.com/np/categories/'+category2_code
    print(category2_code, '二级主页地址： ', url_category2)
    response_category2 = requests.get(url=url_category2, headers=headers)
    html_data_category2 = response_category2.text
    # print(html_data_category2)
    selector_category2 = parsel.Selector(html_data_category2)

    category3_names = selector_category2.xpath(f'//*[@id="searchCategoryComponent"]/ul/li[1]/ul/li/label/text()').getall()
    category3_codes = selector_category2.xpath(f'//*[@id="searchCategoryComponent"]/ul/li[1]/ul/li[@data-linkcode]/@data-linkcode').getall()
    zipdata_category3 = zip(category3_names, category3_codes)

    for category3_name, category3_code in zipdata_category3:
        # print('三级类目', category3_name, category3_code)
        url_category3 = f'https://www.coupang.com/np/categories/' + category3_code
        response_category3 = requests.get(url=url_category3, headers=headers)
        html_data_category3 = response_category3.text
        # print(html_data_category2)
        selector_category3 = parsel.Selector(html_data_category3)

        category4_names = selector_category3.xpath(f'//*[@data-linkcode="{category3_code}"]/ul/li/label/text()').getall()
        category4_codes = selector_category3.xpath(f'//*[@data-linkcode="{category3_code}"]/ul/li[@data-linkcode]/@data-linkcode').getall()
        zipdata_category4 = zip(category4_names,category4_codes)

        for category4_name, category4_code in zipdata_category4:
            print('四级类目', category4_name, category4_code)
            url_category4 = f'https://www.coupang.com/np/categories/' + category4_code
            response_category4 = requests.get(url=url_category4, headers=headers)
            html_data_category4 = response_category4.text
            # print(html_data_category2)
            selector_category4 = parsel.Selector(html_data_category4)

            category5_names = selector_category4.xpath(f'//*[@data-linkcode="{category4_code}"]/ul/li/label/text()').getall()
            print(len(category5_names))
            if len(category5_names) == 0:
                print('没有五级分类')
            category5_codes = selector_category4.xpath(f'//*[@data-linkcode="{category4_code}"]/ul/li[@data-linkcode]/@data-linkcode').getall()
            zipdata_category5 = zip(category5_names, category5_codes)

            for category5_name, category5_code in zipdata_category5:
                print('五级类目', category5_name, category5_code)
                print(category1_name,category2_name,category2_code, category3_name, category3_code,category4_name,category4_code, category5_name, category5_code)

                for page_number in range(1, 10):
                    url_category5_productlist = f'https://www.coupang.com/np/categories/{category5_code}?listSize=60&brand=&offerCondition=&filterType=&isPriceRange=false&minPrice=&maxPrice=&page={page_number}&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=saleCountDesc&filter=&component={category5_code}&rating=0'
                    print(f'============正在采集第{page_number}页产品列表================', url_category5_productlist)
                    response_category5_productlist = requests.get(url=url_category5_productlist, headers=headers)
                    html_data_category5_productlist = response_category5_productlist.text
                    selector_category5_productlist = parsel.Selector(html_data_category5_productlist)

                    # product_names = selector_category5_productlist.xpath('//*[@id="productList"]/li/a/dl/dd/div[2]/text()').getall()
                    product_names = selector_category5_productlist.xpath('//*[@id="productList"]/li/a[@href]/@href').getall()
                    for product_name in product_names:
                        print(product_name)

    # print(category3_names)
# print(category_main,category_2, category_2_code)