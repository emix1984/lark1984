# import random
# import re
# bi_5 = '■ 제조자 : Otsuka Phamrceuticl Co., Ltd  ■ 판매자 : 한국오츠카제약'
# bi_5_1_raw = re.findall(r"제조.*:(.*)■", bi_5, re.S)[0]
# bi_5_1 = "".join(bi_5_1_raw).strip()
# bi_5_2_raw = re.findall(r"판매.*:(.*)", bi_5, re.S)[0]
# bi_5_2 = "".join(bi_5_2_raw).strip()
# print('=1======', bi_5_1)
# print('=2======', bi_5_2)

import requests
import parsel
import csv
import re
import time

# 配置oliveyoung主页地址，浏览器基础信息
url = f'https://www.oliveyoung.co.kr/store/company/brandStory.do'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.99 Safari/537.36',
    'Connection': 'close'
}

# 发送请求
response = requests.get(url=url, headers=headers)
html_data = response.text

# 解析html代码，获取主要分类名称和编码
selector = parsel.Selector(html_data)
category2_names = selector.xpath('//*[@id="gnbAllMenu"]/ul/li[1]/div/ul/li/a/text()').getall()
category2_codes = selector.xpath('//*[@id="gnbAllMenu"]/ul/li[1]/div/ul/li/a[@data-ref-dispcatno]/@data-ref-dispcatno').getall()

for category2_name,category2_code in zip(category2_names,category2_codes):
    url_category_2 = f'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo={category2_code}&isLoginCnt=1&aShowCnt=0&bShowCnt=0&cShowCnt=0&gateCd=Drawer&trackingCd=Cat{category2_code}_MID'

    # 发送请求
    response_category_2 = requests.get(url=url_category_2, headers=headers)
    html_data_category_2 = response_category_2.text
    # print(html_data_category_2)

    # 解析html代码，获取主要分类名称和编码
    selector_html_data_category_2 = parsel.Selector(html_data_category_2)
    category3_names = selector_html_data_category_2.xpath('//*[@id="Contents"]/ul[1]/li/a/text()').getall()
    category3_codes = selector_html_data_category_2.xpath('//*[@id="Contents"]/ul[1]/li/a[@class]/@class').getall()

    for category3_name, category3_code in zip(category3_names, category3_codes):
        url_category_3 = f'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo={category3_code}&fltDispCatNo=&prdSort=01&pageIdx=1&rowsPerPage=24&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat{category3_code}_Small'

        # 发送请求
        response_category_3 = requests.get(url=url_category_3, headers=headers)
        html_data_category_3 = response_category_3.text
        # print(html_data_category_3)
        selector_html_data_category_3 = parsel.Selector(html_data_category_3)
        number_raw = selector_html_data_category_3.xpath('//*[@id="Contents"]/p/span/text()').getall()[0]
        number = number_raw.strip()
        page_number = int(int(number) / 48) + 1
        print(category2_name, category3_name,category3_code, number,page_number)
