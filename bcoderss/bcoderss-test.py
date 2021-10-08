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
print(href)