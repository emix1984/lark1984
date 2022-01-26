# 榜单主页链接
# https://red-heart.xiaohongshu.com/ranks/home


import json
import pprint
from time import sleep
import requests
import parsel
import csv
import re
import time
from tqdm import tqdm
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
url = f'https://red-heart.xiaohongshu.com/api/award/index?version=202007'
# url = f'https://red-heart.xiaohongshu.com/ranks/home'
response = requests.get(url)
json_data = json.loads(response.text)
pprint.pprint(json_data)
collections_ids = json_data['data']
print('=====')
print('collections_ids ', type(collections_ids),collections_ids)
# collections_names = json_data['data']['collections_name']
# print('=====')
# print('collections_names ', type(collections_names))
# zipdata = zip(collections_ids,collections_names)
# for collections_id, collections_name in zipdata:
#     print('=====')
#     print(collections_name, collections_id)