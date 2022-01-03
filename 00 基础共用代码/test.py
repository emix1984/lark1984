# 多线程池测试 20211221
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import parsel
import time

time_start = time.time()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.113 Safari/537.36',
    'Connection': 'close'
}

def getselector(url):
    response = requests.get(url=url, headers=headers)
    print(response)
    html_data = response.text
    # print(len(html_data))
    selector = parsel.Selector(html_data)
    return selector

def getdata(selector):
    titles = selector.xpath('//*[@id="post_list"]/article/section/div/a/text()').getall()
    names = selector.xpath('//*[@id="post_list"]/article/section/footer/a[1]/span/text()').getall()
    zipdata = zip(titles,names)
    # print('kaishi', titles, names)
    return zipdata

def run(url):
    selector = getselector(url)
    zipdata = getdata(selector)
    for title, name in zipdata:
        print('kaishi', name, title)

if __name__ == '__main__':
    urls = []
    for page in range(1,101):
        url1 = f'https://www.cnblogs.com/#p{page}'
        urls.append(url1)

    with ThreadPoolExecutor() as pool:
        futures = [pool.submit(run, url)
                   for url in urls]
        for future in futures:
            print('标记线程', future.result())
        for future in as_completed(futures):
            print(future.result())
    print('jieshu', time.time()-time_start)

