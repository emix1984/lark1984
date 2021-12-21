# ThreadPoolExecutor的使用方法

from concurrent.futures import ThreadPoolExecutor, as_completed
# 用法1： map函数，很简单，注意map的结果和入参是顺序对应的，严格的按照顺序执行线程
with ThreadPoolExecutor() as pool:
    results = pool.map(craw, urls)

    for result in results:
        print(result)

# 用法2：future模式更强大，注意线程池中的线程完成一个线程后系统不按照顺序分配新任务，属于乱序，如果使用as_complete顺序是不固定的
with ThreadPoolExecutor() as pool:
    futures = [pool.submit(craw, url)
               for url in urls ]
    for future in futures:
        print(future.result())
    for future in as_completed(futures):
        print(future.result())