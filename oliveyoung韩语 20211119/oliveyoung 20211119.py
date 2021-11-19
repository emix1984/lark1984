import requests
import csv
import re

for page in range (1,2):
    print(f'==================正在爬取{page}页内容=======================')

    url = f'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=1000001000200060003&fltDispCatNo=&prdSort=03&pageIdx={page}&rowsPerPage=48&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat1000001000200060003_Small'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.99 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    html_data = response.text
    # print(html_data)

    urls = re.findall('<div class="prd_info "><a href="(.*?)"', html_data)
    category_raw = re.findall('<p class="cate_info_tx">(.*?)<span>.*?', html_data, re.S)[0]
    category = category_raw.strip()
    number_raw = re.findall('<span>(.*?)</span>', html_data, re.S)[11]
    number = number_raw.strip()

    for d_url in urls:
        prd_name_mumber = re.findall(r'goodsNo=(.*?)&', d_url)[0]
        d_response = requests.get(url=d_url, headers=headers)
        d_html_data = d_response.text

        prd_name = re.findall(r'<p class="prd_name">(.*?)</p>', d_html_data)
        price_1 = re.findall('<strike>(.*?)</strike>', d_html_data)
        price_2 = re.findall('<strong>(.*?)</strong>', d_html_data)[2]
        color = re.findall('<dd>(.*?)</dd>', d_html_data)
        print(d_url, category, number, prd_name_mumber)
        with open('oliveyoung 20211119.csv', mode='a', encoding='utf-8', newline="") as f:
            csv_write = csv.writer(f)
            csv_write.writerow([d_url, category, number])