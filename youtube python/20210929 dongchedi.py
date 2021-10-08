
import requests
import parsel
import csv

csv_dcd = open('dcd.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_dcd)
csv_writer.writerow(['品牌', '车龄', '里程', '城市', '认证', '售价', '原价'])

for page in range(1,2):
    print(f'------------正在采集第{page}页------------')
    url = f'https://www.dongchedi.com/usedcar/x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x?sh_city_name=%E5%8C%97%E4%BA%AC&page={page}'
    html_data = requests.get(url).text

    selector = parsel.Selector(html_data)
    lis = selector.css('#__next > div > div.new-main.new > div > div > div.wrap > ul > li')
    print(lis)
    print('====================')
    for li in lis:
        title = li.css('li > a > dl > dt > p::text').get()
        info_list = li.css('dl > dd:nth-child(2)::text').getall()
        car_age = ''.join(info_list).split('|')[0]
        mileage = ''.join(info_list).split('|')[1]
        city = ''.join(info_list).split('|')[2]
        # print(city)
        dd_list = li.css('dl dd')
        if len(dd_list) == 4:
            dd_auth = dd_list.css('dd:nth_child(3) span::text').get()
            price = dd_list.css('dd:nth_child(4)::text').get()
            original_price = dd_list.css('dd:nth_child(5)::text').get()
        elif len(dd_list) == 3:
            dd_auth = '无认证'
            price = dd_list.css('dd:nth_child(3)::text').get()
            original_price = dd_list.css('dd:nth_child(4)::text').get()
            print(title, car_age, mileage, city, dd_auth, price, original_price)
            csv_writer.writerow([title, car_age, mileage, city, dd_auth, price, original_price])
csv_dcd.close()