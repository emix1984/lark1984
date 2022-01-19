# 页面地址 http://ftba.nmpa.gov.cn:8181/ftban/fw.jsp
# Request URL: 'http://ftba.nmpa.gov.cn:8181/ftban/itownet/fwAction.do?6SQk6G2z=5m0H4FqYT__etlAFadEmkRXSL0h2yZgGbpEFneg1i5UraPiuam2FUHiSlpVdJom5T3yU.yprvst8hj0p6euZFeGv8JdfEAobmOinfsxD2VDc9qNBbj9G2i_.mR5ZC05QUGkS0EtEpB11lfNIXZ54vi5pH_Ts9k_o0w6wavPzgDWFwZ1emyBAbQY0Qh2G1T5O0EN1WFmIxhzhf9q.r3DjikMh9y18Bq7jmj45dGtOEJPwfk9O9mcPdABR5MMPjJmpapIffFUQicZNeCZfY9tmCkLwjD2CZOBP5Vqntq2ymVQQ&c1SoYK0a=4C0KAQGC8pCjtMIcg1BwTbw8uQu0Yse4afODd0cMYQVIH0PBkHUVWRFtKYb840jMErUafEepHIt_QOSfWlekZJ6mZmFqVvA_YombGF4.Z.xVOpezPWpcUPJv1e1laJ_pm4Qqa4xpECc8cXx5ehh3_9q'
#              http://ftba.nmpa.gov.cn:8181/ftban/itownet/fwAction.do?6SQk6G2z=5q836siy6XEs9c_3KcORKqW8lXrymrJqSQySkp0l0.1sYigMZ1ek_q_9mzix0Hz7tN1qWQES5Tfrol0MKrtOqjvpqCM2Z_Iy4St1mZvIz2JeggRf_RgUD_XB73mFjCx06H0pR72N1m4b6gVcFgrD4FwuTdUe11ocGnI9kKYNolFTsF1Tlri1.si3ZzeKxbXmqbBLN_gfXeYC8SgI.IaMp8HOOuqzaSlW2umn8ZSeci4YKhghmbr4XL47dO_sW6Iv88b3.HX9UTwtiGs1fzX.ZY3Usl1BZzaXmKOH93A8m00A&c1SoYK0a=4.w.WSq_NDo86tgEvvsF71WuyO22t9b787GgkYyZ3XgXfZ7lbs.HlhRk0V.30bxR4zjiirO4Mf.qhjZSr1vwMcXEfnF98Z5z0wukXXygeDLzfcis.Vc97FHMVfxRaXYAs9xV.Rcw3lVOrqiMZBfWnUG
# Request Method: POST
# Host: ftba.nmpa.gov.cn:8181
# Origin: http://ftba.nmpa.gov.cn:8181
# Referer: http://ftba.nmpa.gov.cn:8181/ftban/fw.jsp
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.113 Safari/537.36
# X-Requested-With: XMLHttpRequest
# 参考上面信息获取
# 获取详情页链接方法通过获得json里数据的 newProcessid: "20171225160044sswxf" 构建processid和nid
# 参考详情页链接：http://ftba.nmpa.gov.cn:8181/ftban/itownet/hzp_ba/fw/pz.jsp?processid=201712251607112rbp8&nid=201712251607112rbp8

import json
from time import sleep
import time
import random
import requests
import parsel
from tqdm import tqdm
import re
import csv
import pandas as pd


# 获取htmldata post方法
def response_post(url, params, data):
    # response = requests.post(url=url, headers=headers, params=params, json=data).json()
    response = requests.post(url=url, params=params, json=data)
    print(f'正在解析 >>> {url}')
    # htmldata = response.text
    return response
# 获取htmldata get方法
def response_get(url, headers):
    response = requests.get(url=url, headers=headers)
    # print(f'正在解析 >>> {url}')
    htmldata = response.text
    return htmldata

url = f'http://ftba.nmpa.gov.cn:8181/ftban/itownet/fwAction.do?6SQk6G2z=5q836siy6XEs9c_3KcORKqW8lXrymrJqSQySkp0l0.1sYigMZ1ek_q_9mzix0Hz7tN1qWQES5Tfrol0MKrtOqjvpqCM2Z_Iy4St1mZvIz2JeggRf_RgUD_XB73mFjCx06H0pR72N1m4b6gVcFgrD4FwuTdUe11ocGnI9kKYNolFTsF1Tlri1.si3ZzeKxbXmqbBLN_gfXeYC8SgI.IaMp8HOOuqzaSlW2umn8ZSeci4YKhghmbr4XL47dO_sW6Iv88b3.HX9UTwtiGs1fzX.ZY3Usl1BZzaXmKOH93A8m00A&c1SoYK0a=4.w.WSq_NDo86tgEvvsF71WuyO22t9b787GgkYyZ3XgXfZ7lbs.HlhRk0V.30bxR4zjiirO4Mf.qhjZSr1vwMcXEfnF98Z5z0wukXXygeDLzfcis.Vc97FHMVfxRaXYAs9xV.Rcw3lVOrqiMZBfWnUG'
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,ko-KR;q=0.8,ko;q=0.7',
    'Connection': 'keep-alive',
    'Content-Length': '56',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'JSESSIONID=A5B11290FC76EA6032F7C1736A951453; enable_neCYtZEjo8Gm=true; neCYtZEjo8GmS=53aM_ffneSZhAu6grsFM97onBL0dv47aeICv8NV.6kKfT8jarmIvaRqe.iY2eLqVVb0ywsqwMJTwqYCXShiWnuA; acw_tc=b65cfd2116419052483765967e58f4aad9bae3d89c3f280bc0a72ba4f7bd67; JSESSIONID=628308E4052F532E89D5FDCB9057CEF9; neCYtZEjo8GmT=53wTZICowIolqqqm511ysVG5jl74Z6mdNJQ5UOKQNWkSjOCxeF8DwClfTmVbLKmqDkILY6cyoGyWEcn.j18hExiAI5RNqpBWg.L6dM8GKGv.CikwQCxacDpSXNGUUbHbw8ExMshm.tFhAH9sxhPN2w6mxE5wUihn9mcA6KAC.xWlw95Ow8jFd5dBKUXGNGr2zIPnbt4Ls9FymYH2CbASW2DEi3AjRhOJ9jnHsNL.38awIH24yoiL0tU0GSDhkxHJHa',
    'Host': 'ftba.nmpa.gov.cn:8181',
    'Origin': 'http://ftba.nmpa.gov.cn:8181',
    'Referer': 'http://ftba.nmpa.gov.cn:8181/ftban/fw.jsp',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.137 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
params = {
    '6SQk6G2z': '5q836siy6XEs9c_3KcORKqW8lXrymrJqSQySkp0l0.1sYigMZ1ek_q_9mzix0Hz7tN1qWQES5Tfrol0MKrtOqjvpqCM2Z_Iy4St1mZvIz2JeggRf_RgUD_XB73mFjCx06H0pR72N1m4b6gVcFgrD4FwuTdUe11ocGnI9kKYNolFTsF1Tlri1.si3ZzeKxbXmqbBLN_gfXeYC8SgI.IaMp8HOOuqzaSlW2umn8ZSeci4YKhghmbr4XL47dO_sW6Iv88b3.HX9UTwtiGs1fzX.ZY3Usl1BZzaXmKOH93A8m00A',
    'c1SoYK0a': '4.w.WSq_NDo86tgEvvsF71WuyO22t9b787GgkYyZ3XgXfZ7lbs.HlhRk0V.30bxR4zjiirO4Mf.qhjZSr1vwMcXEfnF98Z5z0wukXXygeDLzfcis.Vc97FHMVfxRaXYAs9xV.Rcw3lVOrqiMZBfWnUG',
}
data = {
    'on': 'true',
    'productName': '',
    'conditionType': '1',
    'applyname': '',
    'applysn': '',
}
response = response_post(url, params, data)

print(response)