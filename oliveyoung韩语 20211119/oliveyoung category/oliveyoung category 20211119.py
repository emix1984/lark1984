# 采集oliveyoung韩文<뷰티>类目下，二级分类编码，并且拼合二级分类的网站地址
import requests
import parsel
import csv
import re

for page in range (1,2):
    # print(f'==================正在爬取{page}页内容=======================')

    url = f'https://www.oliveyoung.co.kr/store/main/main.do?oy=0'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.99 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    html_data = response.text

    selector = parsel.Selector(html_data)
    category1_names = selector.xpath('//*[@id="gnbAllMenu"]/ul/li[1]/div/p/a/text()').getall()
    category1_codes = selector.xpath('//*[@id="gnbAllMenu"]/ul/li[1]/div/p/a[@data-ref-dispcatno]/@data-ref-dispcatno').getall()

    for category1_name, category1_code in zip(category1_names, category1_codes):
        category2_names = selector.xpath('//*[@id="gnbAllMenu"]/ul/li[1]/div/ul/li/a/text()').getall()
        category2_codes = selector.xpath('//*[@id="gnbAllMenu"]/ul/li[1]/div/ul/li/a[@data-ref-dispcatno]/@data-ref-dispcatno').getall()
        for category2_name, category2_code in zip(category2_names, category2_codes):
            # print(category1_name, category1_code, category2_name, category2_code) # 打印显示一级分类和二级分类的名称和code组合
            oliveyoung_homepage_url = "https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo="
            category2_url = oliveyoung_homepage_url+category2_code
            print(category2_url)

            response_category2 = requests.get(url=category2_url, headers=headers)
            html_data_category2 = response_category2.text
            selector_category2 = parsel.Selector(html_data_category2)

            category3_names = selector_category2.xpath('//*[@id="Contents"]/ul[1]/li/a/text()').getall()
            category3_codes = selector_category2.xpath('//*[@id="Contents"]/ul[1]/li/a[@class]/@class').getall()
            for category3_name, category3_code in zip(category3_names,category3_codes):
                category3_url = oliveyoung_homepage_url+category3_code
                print(category1_name, category1_code, category2_name, category2_code, category3_name, category3_code, category3_url)
                with open('oliveyoung category 20211119.csv', mode='a', encoding='utf-8', newline="") as f:
                    csv_write = csv.writer(f)
                    csv_write.writerow([category1_name, category1_code, category2_name, category2_code, category3_name, category3_code, category3_url])