# 【Python爬虫】最适合于python小白的爬虫案例教程-多线程采集表情包网站
# https://www.youtube.com/watch?v=SZ_v0_u3yq0&list=PL9OlirjBavPE9JJ5lq0yeK1ol8v-lJiU-&index=4&t=27s
# 表情包页面地址 https://www.fabiaoqing.com/biaoqing/lists/page

import requests
import re

for page in range(1,3)

    url  = f'https://www.fabiaoqing.com/biaoqing/lists/page/{page}.html'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.72 Safari/537.36'
    }

    response =  requests.get(url=url, headers=headers)
    html_data = response.text

    images = re.findall('<img class="ui image lazy" data-original="(.*?)"', html_data)
    titles = re.findall('<a href=".*?" title="(.*?)">', html_data)

    for img_url, title in zip(images, titles):
        new_title = re.sub(r'[\\\/\:*?"<>|]', '_', title)
        if len(new_title) >50:
            new_title = new_title[:10]
        response_2 = requests.get(img_url)
        suffix = img_url.split('.')[-1]
        img_data = response_2.content

        with open (f'img/{new_title}.{suffix}', mode='wb') as f:
            f.write(img_data)
        print(f'{new_title},保存成功！！！')