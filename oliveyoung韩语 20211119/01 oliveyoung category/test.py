import csv
import requests

with open('oliveyoung category 20211119.csv', mode='r', encoding='utf-8') as f:
    reader = csv.reader(f)
    fieldnames = next(reader)
    # print(fieldnames)
    csv_reader = csv.DictReader(f, fieldnames=fieldnames) # self._fieldnames = fieldnames
    # list of keys for the dict 以list的形式存放键名
    for row in csv_reader:
        d = {}
        for k, v in row.items():
            d[k] = v
        category3 = list(d.values())[5]
        url_category3 = list(d.values())[6] # 选取三级分类网址链接生成列表
        # url_category3 = int(url_category3_raw)
        url_sub = f"&fltDispCatNo=&prdSort=03&pageIdx=1&rowsPerPage=48&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=1&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat{category3}_Small"
        url = url_category3+url_sub

        print(url)
