# 采集oliveyoung韩文<뷰티>类目下，
# 二级分类编码，并且拼合二级分类的网站地址
# 三级分类编码，并且拼合三级分类网站地址
# 获得三级分类地址里产品总数以及总页数

import requests
import parsel
import csv
import re
import time

# 项目计时用
time_1 = time.time()

# 配置oliveyoung主页地址，浏览器基础信息
url = f'https://www.oliveyoung.co.kr/store/main/main.do?oy=0'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.99 Safari/537.36'
}
# 发送请求
response = requests.get(url=url, headers=headers)
html_data = response.text

# 解析html代码，获取主要分类名称和编码
selector = parsel.Selector(html_data)
category1_names = selector.xpath('//*[@id="gnbAllMenu"]/ul/li[1]/div/p/a/text()').getall()
category1_codes = selector.xpath('//*[@id="gnbAllMenu"]/ul/li[1]/div/p/a[@data-ref-dispcatno]/@data-ref-dispcatno').getall()

# 获取二级分类名称和编码
for category1_name, category1_code in zip(category1_names, category1_codes):
    category2_names = selector.xpath('//*[@id="gnbAllMenu"]/ul/li[1]/div/ul/li/a/text()').getall()
    category2_codes = selector.xpath('//*[@id="gnbAllMenu"]/ul/li[1]/div/ul/li/a[@data-ref-dispcatno]/@data-ref-dispcatno').getall()
    # 拼合二级分类网页网址，打开网址并获得三级分类名称和编码
    for category2_name, category2_code in zip(category2_names, category2_codes):
        # print(category1_name, category1_code, category2_name, category2_code) # 打印显示一级分类和二级分类的名称和code组合
        oliveyoung_homepage_url = "https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo="
        category2_url = oliveyoung_homepage_url+category2_code
        # print(category2_url)

        # 发送二级分类地址请求，解析html代码，获得三级分类名称和编码
        response_category2 = requests.get(url=category2_url, headers=headers)
        html_data_category2 = response_category2.text
        selector_category2 = parsel.Selector(html_data_category2)
        category3_names = selector_category2.xpath('//*[@id="Contents"]/ul[1]/li/a/text()').getall()
        category3_codes = selector_category2.xpath('//*[@id="Contents"]/ul[1]/li/a[@class]/@class').getall()

        # 拼合三级分类的地址，获得分类下的产品数量以及按照每页48个产品的展示下有多少页
        for category3_name, category3_code in zip(category3_names,category3_codes):
            category3_url = oliveyoung_homepage_url+category3_code
            response_category3 = requests.get(url=category3_url, headers=headers)
            html_data_category3 = response_category3.text
            number_raw = re.findall('<span>(.*?)</span>', html_data_category3, re.S)[11]
            number = number_raw.strip()
            page_number = int(int(number)/48) + 1
            print(number, page_number)
            # 时间戳
            rightnow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            print(rightnow, '正在采集：', category1_name, category2_name, category3_name)
            with open('oliveyoung category 20211119.csv', mode='a', encoding='utf-8', newline="") as f:
                csv_write = csv.writer(f)
                csv_write.writerow([category1_name, category1_code, category2_name, category2_code, category3_name, category3_code, category3_url, number, page_number, rightnow])
                print(f'总耗时，{time.time() - time_1}')