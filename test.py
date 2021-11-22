import requests
import parsel


# 1 找数据对应的链接地址
url = 'https://www.oliveyoung.co.kr/pc-static-root/js/goods/goods.js?dumm=202111180002'

#伪装，代表浏览器身份，python的基本数据容器（列表，元组，字典，集合）
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.214 Safari/537.36'}

#2 发送指定地址请求（python）utf-8
response = requests.get(url=url, headers=headers)

html_data = response.text

print(html_data)