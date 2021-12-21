#
# import requests
# import  parsel
# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.113 Safari/537.36',
#     'Connection': 'close'
# }
# url = 'https://www.oliveyoung.co.kr/store/display/getCategoryShop.do?dispCatNo=10000010001&gateCd=Drawer'
# response = requests.get(url=url, headers=headers)
# html_data = response.text
# selector = parsel.Selector(html_data)
# category2_names = selector.xpath('//*[@id="Contents"]/div/div[1]/ul/li/a/span/text()').getall()
# category2_codes = selector.xpath('//*[@id="Contents"]/div/div[1]/ul/li/a[@class]/@class').getall()
#
# print(category2_names,category2_codes)
#
# for category2_name, category2_code in zip(category2_names,category2_codes):
#     print(category2_name,category2_code)

lis = [""]
print('lis', lis)
for li in lis:
    print('li', li)