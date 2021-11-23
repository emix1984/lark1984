# 第二步解决问题
# 1 解决三级分类链接下的产品数量采集
# 2 解决页面生成逻辑
# 3 采集产品详情页链接
# 下面是示例链接，按照符号& 进行换行处理，dispCatNo=类别编码；&prdSort=01默认01是按照人气排序方式；pageIdx=1页码第一页；trackingCd=Cat1000001000100080001_Small这是追踪用记得要和分类编码组合使用
# https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=1000001000100080001
# &fltDispCatNo=
# &prdSort=01
# &pageIdx=1
# &rowsPerPage=24
# &searchTypeSort=btn_thumb
# &plusButtonFlag=N
# &isLoginCnt=0
# &aShowCnt=
# &bShowCnt=
# &cShowCnt=
# &trackingCd=Cat1000001000100080001_Small

import requests
import csv
import re
import time

# 创建csv文件和表头
f = open('oliveyoung_listing.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
'三级类目名称',
'三级类目名称1',
'三级类目编码',
'三级类目产品数',
'页码',
'产品编码',
'产品链接',
'采集时间',
])
csv_writer.writeheader()

# 项目计时用
time_1 = time.time()

# 时间戳
rightnow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# 提取三级分类地址链接和页面数量
with open('oliveyoung category 20211119.csv', mode='r', encoding='utf-8') as f:
    reader = csv.reader(f)
    fieldnames = next(reader)
    # print(fieldnames)
    csv_reader = csv.DictReader(f, fieldnames=fieldnames)  # self._fieldnames = fieldnames
    # list of keys for the dict 以list的形式存放键名
    for row in csv_reader:
        d = {}
        for k, v in row.items():
            d[k] = v
        category1 = list(d.values())[0]
        category2 = list(d.values())[2]
        category3 = list(d.values())[4]
        category3_code = list(d.values())[5]
        # url_category3 = list(d.values())[6]  # 提取三级分类网址链接生成列表
        pageno_raw = list(d.values())[8] # 选取三级分类网址下总页面数
        pageno = int(pageno_raw) # 将三级分类网址下总页面数从文字类型转换为数值型
        print(category1,category2,category3,pageno)

        for page in range(1, pageno):
            print(page)
            print(f'==================正在爬取',category1,category2, category3, f'第{page}页内容=======================')
            rowsPerPage = 48 # 每页显示产品数 24, 36, 48

            url = f'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo={category3_code}&fltDispCatNo=&prdSort=03&pageIdx={page}&rowsPerPage={rowsPerPage}&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=1&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat{category3_code}_Small'
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
            # pageno = int(int(number)/4)+1

            for d_url in urls:
                prd_name_mumber = re.findall(r'goodsNo=(.*?)&', d_url)[0]
                # d_response = requests.get(url=d_url, headers=headers)
                # d_html_data = d_response.text

                # prd_name = re.findall(r'<p class="prd_name">(.*?)</p>', d_html_data)
                # price_1 = re.findall('<strike>(.*?)</strike>', d_html_data)
                # price_2 = re.findall('<strong>(.*?)</strong>', d_html_data)[2]
                # color = re.findall('<dd>(.*?)</dd>', d_html_data)

                print(category, pageno, number, prd_name_mumber)

                # 建立字典存储到文件
                dict = {
                    '三级类目名称': category,
                    '三级类目名称1': category3,
                    '三级类目编码': category3_code,
                    '三级类目产品数': number,
                    '页码': page,
                    '产品编码': prd_name_mumber,
                    '产品链接': d_url,
                    '采集时间': rightnow,
                }
                print(rightnow, '....正在采集：', category1, category2, category3)
                csv_writer.writerow(dict)
print(f'===采集完成===累计耗时：', time.time() - time_1, rightnow)