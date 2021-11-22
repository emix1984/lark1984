import re
from time import sleep
import time
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions # 配置chromedriver无界面方式
from selenium.webdriver.chrome.service import Service # 升级后webdriver配置chromedriver.exe为服务
from selenium.webdriver.common.by import By # python3.6 升级到 3.8后定位元素的方式变动
import csv

# 创建csv文件和表头
f = open('oliveyoung detailpage data.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
        '产品名称',
        '销售价',
        '市场价',
        '促销1세일',
        '促销2쿠폰',
        '促销3증정',
        '促销4오늘드림',
        '品牌',
        '品牌id',
        '品牌logo图片url',
        '详情页图',
        '容量重量',
        '适合肌肤类型',
        '流通期限',
        '使用方法',
        '化妆品制造企业&销售企业',
        '制造国家',
        '成分',
        '功能性化妆品',
        '使用注意事项',
        '品质保证基准',
        '售后服务电话',
        '当前网址',
        '当前时间',
])
csv_writer.writeheader()

# 配置浏览器基本信息
url = 'https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000158896&dispCatNo=1000001000200060003&trackingCd='
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.99 Safari/537.36'
    }
opt = ChromeOptions()
opt.headless = True
s = Service(r"D:\lark1984\selenium\chromedriver.exe")
driver = Chrome(service=s, options=opt)

# sleep(0.5)
driver.get(url)

# sleep(3) #等待页面加载
driver.find_element(By.XPATH, '//*[@id="buyInfo"]/a').click() #登录

# category


# detail page - product info
dp_name = driver.find_element(By.XPATH, '//*[@id="Contents"]/div[2]/div[2]/div/p[2]').text
dp_price1 = driver.find_element(By.XPATH, '//*[@class="price-1"]/strike').text
dp_price2 = driver.find_element(By.XPATH, '//*[@class="price-2"]/strong').text

# detail page - promotion
dp_promo1 = driver.find_element(By.XPATH, '//*[@id="Contents"]/div[2]/div[2]/div/p[3]/span[1]').text
# sale 세일
dp_promo2 = driver.find_element(By.XPATH, '//*[@id="Contents"]/div[2]/div[2]/div/p[3]/span[1]').text
# 쿠폰
dp_promo3 = driver.find_element(By.XPATH, '//*[@id="Contents"]/div[2]/div[2]/div/p[3]/span[1]').text
# 증정
dp_promo4 = driver.find_element(By.XPATH, '//*[@id="Contents"]/div[2]/div[2]/div/p[3]/span[1]').text
# 오늘드림

brand_name = driver.find_element(By.XPATH, '//*[@id="moveBrandShop_like"]/em').text.replace(' 브랜드관', "")
brand_logo_raw = driver.find_element(By.XPATH, '//*[@id="moveBrandShop_like"]/span').get_attribute('style')
brand_logo = re.findall(r'\"(.*?)\"', brand_logo_raw)[0]
brand_id = driver.find_element(By.XPATH, '//*[@id="brnd_wish"]').get_attribute('data-ref-onlbrndcd')

# 상품설명 prd_detail_tab>id=productInfo
detailpage_img = driver.find_element(By.XPATH, '//*[@id="Contents"]/div[7]/div[1]/div[1]/img[1]').get_attribute('src')

# 구매정보 prd_detail_tab>id=buyInfo
bi_1 = driver.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[1]/dd').text
# volume/weight
bi_2 = driver.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[2]/dd').text
# ideal for
bi_3 = driver.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[3]/dd').text
# expiration date
bi_4 = driver.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[4]/dd').text
# how to use
bi_5 = driver.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[5]/dd').text
# manufacturner/distributor
bi_6 = driver.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[6]/dd').text
# country of manufacture
bi_7 = driver.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[7]/dd').text
# ingredients
bi_8 = driver.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[8]/dd').text
# MFDS Evaluation of functional cosmetics
bi_9 = driver.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[9]/dd').text
# cautions for use
bi_10 = driver.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[10]/dd').text
# quality assurance standard
bi_11 = driver.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[11]/dd').text
# customer servcie

#时间戳
rightnow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# 存储到文件
dict = {
    '产品名称' : dp_name,
    '销售价' : dp_price2,
    '市场价' : dp_price1,
    '促销1세일' : dp_promo1,
    '促销2쿠폰' : dp_promo2,
    '促销3증정' : dp_promo3,
    '促销4오늘드림' : dp_promo4,
    '品牌' : brand_name,
    '品牌id' : brand_id,
    '品牌logo图片url' : brand_logo,
    '详情页图': detailpage_img,
    '容量重量': bi_1,
    '适合肌肤类型': bi_2,
    '流通期限': bi_3,
    '使用方法': bi_4,
    '化妆品制造企业&销售企业': bi_5,
    '制造国家': bi_6,
    '成分': bi_7,
    '功能性化妆品': bi_8,
    '使用注意事项': bi_9,
    '品质保证基准': bi_10,
    '售后服务电话': bi_11,
    '当前网址': url,
    '当前时间': rightnow,
        }
print(dp_name, dp_price2, dp_promo1, brand_name, bi_1, bi_4)
csv_writer.writerow(dict)
print('下载完成:', dp_name,url)

driver.close()
driver.quit()