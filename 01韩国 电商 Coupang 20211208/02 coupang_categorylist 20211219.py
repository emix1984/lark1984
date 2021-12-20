import pprint
from time import sleep
import requests
import parsel
import json
import csv
import re
import time
import concurrent.futures


# 创建csv文件和表头
f = open('02_coupang_listing02.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
'一级类目名称',
'二级类目名称',
'二级类目编码',
'三级类目名称',
'三级类目编码',
'四级类目名称',
'四级类目编码',
'五级类目名称',
'五级类目编码',
'存在五级类目',
'页码',
'序号',
'产品名称',
'产品链接',
'采集时间',
])
csv_writer.writeheader()

# 项目计时用
time_1 = time.time()

# 时间戳
rightnow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# 序号
order_number = 0

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
    # print(category2_code, '二级主页地址： ', url_category2)
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
            # print('四级类目', category4_name, category4_code)
            url_category4 = f'https://www.coupang.com/np/categories/' + category4_code
            response_category4 = requests.get(url=url_category4, headers=headers)
            html_data_category4 = response_category4.text
            # print(html_data_category2)
            selector_category4 = parsel.Selector(html_data_category4)

            category5_names = selector_category4.xpath(f'//*[@data-linkcode="{category4_code}"]/ul/li/label/text()').getall()
            # print(len(category5_names))
            if len(category5_names) == 0:
                category5_exist = 'none'
                category5_names = category4_names
                category5_codes = category4_codes
                # print('没有五级分类')
            else:
                category5_exist = 'yes'
                category5_codes = selector_category4.xpath(f'//*[@data-linkcode="{category4_code}"]/ul/li[@data-linkcode]/@data-linkcode').getall()

            zipdata_category5 = zip(category5_names, category5_codes)

            for category5_name, category5_code in zipdata_category5:
                # print('五级类目', category5_name, category5_code)
                print('category1：', category1_name, 'category2：', category2_name, category2_code, 'category3：', category3_name, category3_code,'category4：', category4_name,category4_code, 'category5：',category5_name, category5_code)

                for page_number in range(1, 10):
                    url_category5_productlist = f'https://www.coupang.com/np/categories/{category5_code}?listSize=60&brand=&offerCondition=&filterType=&isPriceRange=false&minPrice=&maxPrice=&page={page_number}&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=saleCountDesc&filter=&component={category5_code}&rating=0'
                    print(f'============正在采集第{page_number}页产品列表================')
                    response_category5_productlist = requests.get(url=url_category5_productlist, headers=headers)
                    html_data_category5_productlist = response_category5_productlist.text
                    selector_category5_productlist = parsel.Selector(html_data_category5_productlist)

                    product_names = selector_category5_productlist.xpath('//*[@id="productList"]/li/a/dl/dd/div[2]/text()').getall()
                    detailpage_urls = selector_category5_productlist.xpath('//*[@id="productList"]/li/a[@href]/@href').getall()
                    zipdata_listing = zip(product_names, detailpage_urls)

                    for product_name_raw, detailpage_url_raw in zipdata_listing:
                        order_number = order_number+1
                        product_name = product_name_raw.strip()
                        detailpage_url = f'https://www.coupang.com'+detailpage_url_raw
                        print( f'\033[31m正在采集第{order_number}条数据\033[0m', product_name, detailpage_url)
                        # 建立字典存储到文件
                        dict = {
                            '一级类目名称': category1_name,
                            '二级类目名称': category2_name,
                            '二级类目编码': category2_code,
                            '三级类目名称': category3_name,
                            '三级类目编码': category3_code,
                            '四级类目名称': category4_name,
                            '四级类目编码': category4_code,
                            '五级类目名称': category5_name,
                            '五级类目编码': category5_code,
                            '存在五级类目': category5_exist,
                            '页码': page_number,
                            '序号': order_number,
                            '产品名称': product_name,
                            '产品链接': detailpage_url,
                            '采集时间': rightnow,
                        }
                        print(rightnow, '>>>\033[00;42m数据写入完毕：\033[0m')
                        csv_writer.writerow(dict)
print(f'===采集完成===累计耗时：', time.time() - time_1, rightnow)