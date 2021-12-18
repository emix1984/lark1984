# 【Python爬虫】最适合于python小白的爬虫案例教程-多线程采集表情包网站
# https://www.youtube.com/watch?v=SZ_v0_u3yq0&list=PL9OlirjBavPE9JJ5lq0yeK1ol8v-lJiU-&index=4&t=27s
# 表情包页面地址 https://www.fabiaoqing.com/biaoqing/lists/page

import requests
import re
import time
import concurrent.futures

def get_response(html_url):
    response = requests.get(html_url)
    return response

def get_img_url_info(response):
    images = re.findall('<img class="ui image lazy" data-original="(.*?)"', response.text)
    titles = re.findall('<a href=".*?" title="(.*?)">', response.text)
    zip_data = zip(titles, images)
    return zip_data

def save(title, name, img_url):
    img_content = get_response(img_url).content
    with open('img\\' + title + '.' +name, mode='wb') as f:
        f.write(img_content)
        print('正在保存：', title)

def change_title(title):
    new_title = re.sub(r'[\\\/\:*?"<>|]', '_', title)
    return new_title

def run(html_url):
    response = get_response(html_url)
    zip_data = get_img_url_info(response)
    for title, img_url in zip_data:
        new_title = change_title(title)
        img_name = img_url[-3:]
        if len(new_title) > 50:
            new_title = new_title[:10]
        # save(new_title, img_name, img_url)

# time_1 = time.time()
# for page in range(1,11):
#     run(f'https://www.fabiaoqing.com/biaoqing/lists/page/{page}.html')
# print(f'总耗时，{time.time() - time_1}')

if __name__ == '__main__':
    time_1 = time.time()
    # concurrent.futures模块提供了两种executor的子类，ThreadPoolExecutor各自独立操作一个线程和 ProcessPoolExecutor一个进程池
    exe = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    # exe = concurrent.futures.ProcessPoolExecutor(max_workers=10)
    for page in range(1, 51):
        url = f'https://www.fabiaoqing.com/biaoqing/lists/page/{page}.html'
        print(url)
        exe.submit(run, url)
        exe.su
    exe.shutdown()
    print(f'总耗时:{time.time()-time_1}')