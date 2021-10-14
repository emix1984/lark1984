# youtube Python采集某直播平台美女照片，实现人脸检测，打造颜值排行榜！
# https://www.youtube.com/watch?v=BA2_51GWr8k&t=2436s
# 斗鱼颜值页面 https://www.douyu.com/g_yz

import requests
import jsonpath
from urllib.request import urlretrieve

url = 'https://www.douyu.com/gapi/rknc/directory/yzRec/1'

response = requests.get(url).json()

images = jsonpath.jsonpath(response, '$..rs16')
names = jsonpath.jsonpath(response, '$..nn')

for image, name in zip(images,names):
    filepath = r'img/'+name+'.jpg'
    urlretrieve(image, filepath)
    print(name, image)
