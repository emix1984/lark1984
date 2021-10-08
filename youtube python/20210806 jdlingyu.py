import requests
#数据请求模块
import parsel
import os
import random

#1 找数据对应的链接地址
url = 'https://www.ababbb.com/ymm'

#伪装，代表浏览器身份，python的基本数据容器（列表，元组，字典，集合）
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.214 Safari/537.36'}

#2 发送指定地址请求（python）utf-8
response = requests.get(url=url, headers=headers)

html_data = response.text
# text 提取对象里边的文本
#print(html_data)
# 在通过在终端中搜索数据，如果能够找到，证明我们找到的数据已经请求下来

#3 数据提取（提取有用额，需要的）
selector = parsel.Selector(html_data)
#print(selector)

lis = selector.xpath('//*[@id="post-list"]/ul/li')
for li in lis:
    title = li.xpath('.//h2/a/text()').get() #需要对比一下完整地址是//*[@id="post-list"]/ul/li//h2/a/@href
    pic_url = li.xpath('.//h2/a/@href').get()
    print(title, pic_url)

    if not os.path.exists('img\\' + title): #判断img文件夹下没有相册的文件夹
        os.mkdir('img\\' + title) #创建文件夹
    response_pic = requests.get(url=pic_url, headers=headers).text

    selector_pic = parsel.Selector(response_pic)
    pic_url_list = selector_pic.xpath('//*[@id="primary-home"]/article/div[2]/p[2]/img/@src').getall()
    print(pic_url_list)

    for pic_url in pic_url_list:
        pic_data = requests.get(url=pic_url, headers=headers).content
        #准备文件
        file_name = pic_url.split('/')[-1]
        with open(f'img\\{title}\\' + file_name, mode='wb') as f:
            f.write(pic_data)
            print('下载完成:', file_name)
