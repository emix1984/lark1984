# 【Python爬虫】从零爬取某知名招聘网站招聘数据，看你离月薪过万差哪些
# https://www.youtube.com/watch?v=AakmTK-cnmE&t=1028s

# 导入模块
import requests
import re
import json
import pprint
import time
import csv

f = open('51job_data.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
    '职位名字',
        '公司',
        '薪资',
        '地区',
        '经验',
        '详情链接',
])
csv_writer.writeheader()

for page in range(1, 5):
    print(f'正在爬取第{page}页数据内容')
    time.sleep(1.5)

# 配置url,headers
    url = f'https://search.51job.com/list/360000%252c010000,000000,0000,32,9,99,PHP,2,{page}.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38'
    }

    response = requests.get(url=url, headers=headers)
    html_data = re.findall('window.__SEARCH_RESULT__ = (.*?)</script>', response.text)[0]
    # 正则表达式匹配出来的数据是列表 [] list
    # 在正则表达式最后加入[0]获取到字符串数字
    # print(html_data)

    json_data = json.loads(html_data)['engine_jds']
    # pprint.pprint(json_data)

    for index in json_data:
        title = index['job_title']
        company_name = index['company_name']
        money = index['providesalary_text']
        workarea_text = index['attribute_text'][0]
        exp = index['attribute_text'][1]
        href = index['job_href']
        dict = {
            '职位名字' : title,
            '公司' : company_name,
            '薪资' : money,
            '地区' : workarea_text,
            '经验' : exp,
            '详情链接' : href,
            }
        print(title, company_name, money, workarea_text, exp, href)
    csv_writer.writerow(dict)

