# 采集韩国猎头网站SARAMIN的相关关键词工作岗位数据
import csv
import requests
import parsel

f = open('saramin_data.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
    '岗位名称',
    '省级',
    '市级',
])
csv_writer.writeheader()

for page in range(1, 2):
    print(f'------------正在采集第{page}页------------')
    url = f'https://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=auto&searchword=PHP+AJAX&recruitPage={page}&recruitSort=relation&recruitPageCount=40&inner_com_type=&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9%2C10&show_applied=&quick_apply=&except_read=&mainSearch=n'
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38'
        }
    response = requests.get(url=url, headers=headers)
    html_data = response.text
    # print(html_data)

    selector = parsel.Selector(html_data)
    lis = selector.css('#recruit_info_list > div.content > div')
    # print(lis)
    # print(type(lis))

    for li in lis:
        job_tit = li.css('div.area_job > h2.job_tit > a::attr(href)').get()
        area1 = li.css('div.area_job > div.job_condition > span:nth-child(1) > a:nth-child(1)::text').get()
        area2 = li.css('div.area_job > div.job_condition > span:nth-child(1) > a:nth-child(2)::text').get()
        print(job_tit, area1, area2)
        dict = {
            '岗位名称' : job_tit,
            '省级' : area1,
            '市级' : area2,
        }
        csv_writer.writerow(dict)
f.close()