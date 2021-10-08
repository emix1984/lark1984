import requests
import parsel
import csv

url = f'https://travel.qunar.com/p-cs302391-shouer'
response = requests.get(url)
html_data = response.text

selector = parsel.Selector(html_data)
url_list = selector.css('#js_replace_box > ul > li > h3 > a::attr(href)').getall()
for detail_url in url_list:
    response_1 = requests.get(detail_url).text
    selector_1 = parsel.Selector(response_1)
    title = selector_1.css('#booktitle::text').get()
    contents = selector_1.css('#ele-1120580-2 > div.bottom > div.e_img_schedule > div > div > p.first::text').get()
    print(title, contents)