import requests
import re
import os

filename = 'img\\'

if not os.path.exists(filename):
    os.mkdir(filename)

def changer_title(name):
    new_name = re.sub(r'[\/\\\:\*\?\"\<\>\|]', '_', name)
    return new_name
# for page in range(1, 11)
# url = f'https://m.bcoderss.com/tag/%e7%be%8e%e5%a5%b3/page/{page}/'
url = 'https://m.bcoderss.com/tag/%e7%be%8e%e5%a5%b3/page/3/'
headers = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44'
}
response = requests.post(url=url, headers=headers)
href = re.findall('<li><a target="_blank" href="(.*?)"',response.text)[1:]
for index in href:
    response_1 = requests.get(url=index, headers=headers)
    title = re.findall('<title>(.*?)</title>', response_1.text)[0]
    title = changer_title(title)
    img_url = re.findall('<img alt=".*?" title=".*?" src="(.*?)">', response_1.text)[0]
    img_content = requests.get(url=img_url, headers=headers).content
    requests.get(url=img_url, headers=headers)
    with open(filename + title + '.jpg', mode='wb') as f:
        f.write(img_content)
    print("正在采集"+title, img_url)
