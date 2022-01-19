# -*- coding: utf-8 -*-

from time import sleep
import time
import random
import requests
import parsel
from tqdm import tqdm
import re
import csv
import pandas as pd

# 读取csv文件
def readcsv():
    # pandas 拉取 listing.csv数据中的产品详情页链接
    df_listing = pd.read_csv(f'data.csv')
    data01 = pd.DataFrame(df_listing)
    # print(data01)
    print(f'\033[32m>>>csv文件，进行去重操作中<<<\033[0m', '读取数据条目共计： ', len(data01), '条')
    data02 = data01.drop_duplicates("표준 영문명")  # 去除重复链接
    # print(data02)
    # print(f'\033[32m>>>数据去重操作已完成<<<\033[0m', '去重操作数据共计： ', len(data02), '条')
    lis1 = data02["표준 성분명"].tolist()
    lis2 = data02["표준 영문명"].tolist()
    # print(lis1,lis2)
    # print(type(lis1))
    return lis1,lis2


a = f'알로에베라잎즙(89.4%),디프로필렌글라이콜,1,2-헥산디올,에탄올,글리세린,트로메타민,카보머,피이지-40하이드로제네이티드캐스터오일,피피지-26-부테스-26,향료,디소듐이디티에이,마치현추출물,베타인,판테놀,정제수,포타슘소르베이트,부틸렌글라이콜,뽕나무뿌리추출물,세이지잎추출물,칸델라브라알로에잎추출물,트레할로스,화이트윌로우껍질추출물,락토바실러스/콩발효추출물,오레가노잎추출물,육계추출물,황금추출물,편백나무잎추출물,로즈마리잎추출물,히비스커스꽃추출물,홍화추출물'
print(type(a))
lis1,lis2 = readcsv()
zipdata = zip(lis1,lis2)
n=0
for k, e in zipdata:
    try:
        n=n+1
        # print(n)
        # print(k,e)
        a = re.sub(k,str(e),a)
    except:
        break
print(a)