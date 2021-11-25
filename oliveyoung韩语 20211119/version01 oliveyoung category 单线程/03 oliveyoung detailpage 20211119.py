from time import sleep
import time
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions # 配置chromedriver无界面方式
from selenium.webdriver.chrome.service import Service # 升级后webdriver配置chromedriver.exe为服务
from selenium.webdriver.common.by import By # python3.6 升级到 3.8后定位元素的方式变动
import re
import csv


# 创建csv文件和表头
f = open('../03 oliveyoung detailpage/03_oliveyoung_detailpage_data.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
        '产品编码',
        '产品名称',
        '产品缩略图',
        '销售价',
        '市场价',
        '评论数',
        'Q&A',
        '促销1세일',
        '促销2오늘드림',
        '促销3증정',
        '促销41+1',
        '促销5쿠폰',
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

# 项目计时用
time_1 = time.time()

# 拉取listing.csv数据中的产品详情页链接
with open('02_oliveyoung_listing.csv', mode='r', encoding='utf-8') as f_listing:
    reader = csv.reader(f_listing)
    fieldnames_listing = next(reader)
    # print(fieldnames_listing)
    csv_reader = csv.DictReader(f_listing, fieldnames=fieldnames_listing)  # self._fieldnames = fieldnames
    # list of keys for the dict 以list的形式存放键名
    for row in csv_reader:
        d_listing = {}
        for k, v in row.items():
            d_listing[k] = v
        urls_detailpage = list(d_listing.values())[5]
        print(urls_detailpage)

        # 配置浏览器基本信息
        url_dp = urls_detailpage
        headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.99 Safari/537.36'
            }
        opt = ChromeOptions()
        opt.headless = True
        s = Service(r"D:\lark1984\selenium\chromedriver.exe")
        driver_dp = Chrome(service=s, options=opt)

        sleep(0.5) # 等待页面加载0.5秒
        driver_dp.get(url_dp)

        sleep(3) # 等待页面加载3秒
        driver_dp.find_element(By.XPATH, '//*[@id="buyInfo"]/a').click() # 点击详情页下方标签页
        html_data_dp = driver_dp.page_source
        # print(html_data)

        # detail page - product info
        # 产品名称
        product_code = re.findall(f'goodsNo=(.*?)&', url_dp, re.S)[0]
        dp_name = driver_dp.find_element(By.XPATH, '//*[@id="Contents"]/div[2]/div[2]/div/p[2]').text
        dp_img = driver_dp.find_element(By.XPATH, '//*[@id="mainImg"]').get_attribute('src')

        # 开始判断是否存在 price-1 标签, <strike></strike>是唯一一个price-1标签用到的html标签
        if "strike" in html_data_dp:
                dp_price1 = driver_dp.find_element(By.XPATH, '//*[@class="price-1"]/strike').text
                dp_price2 = driver_dp.find_element(By.XPATH, '//*[@class="price-2"]/strong').text
        else:
                dp_price2 = driver_dp.find_element(By.XPATH, '//*[@class="price-2"]/strong').text
                dp_price1 = driver_dp.find_element(By.XPATH, '//*[@class="price-2"]/strong').text
        # print(dp_price1,dp_price2)

        # detail page - promotion
        # <span class="icon_flag sale">세일</span>
        # <span class="icon_flag delivery">오늘드림</span>
        # <span class="icon_flag gift">증정</span>
        # <span class="icon_flag plus">1+1</span>
        # <span class="icon_flag coupon">쿠폰</span>

        # sale세일
        if "icon_flag sale" in html_data_dp:
                dp_promo1 = "세일"
        else:
                dp_promo1 = ""

        # 오늘드림
        if "icon_flag delivery" in html_data_dp:
                dp_promo2 = "오늘드림"
        else:
                dp_promo2 = ""

        # 증정
        if "icon_flag gift" in html_data_dp:
                dp_promo3 = "증정"
        else:
                dp_promo3 = ""

        # 1+1
        if "icon_flag plus" in html_data_dp:
                dp_promo4 = "1+1"
        else:
                dp_promo4 = ""

        # 쿠폰
        if "icon_flag coupon" in html_data_dp:
                dp_promo5 = "쿠폰"
        else:
                dp_promo5 = ""

        brand_name = driver_dp.find_element(By.XPATH, '//*[@id="moveBrandShop_like"]/em').text.replace(' 브랜드관', "")
        brand_logo_raw = driver_dp.find_element(By.XPATH, '//*[@id="moveBrandShop_like"]/span').get_attribute('style')
        brand_logo = re.findall(r'\"(.*?)\"', brand_logo_raw)[0]
        brand_id = driver_dp.find_element(By.XPATH, '//*[@id="brnd_wish"]').get_attribute('data-ref-onlbrndcd')

        # 상품설명 prd_detail_tab>id=productInfo
        detailpage_img = "" # 后续待处理

        # 구매정보 prd_detail_tab>id=buyInfo
        bi_1 = driver_dp.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[1]/dd').text
        # volume/weight
        bi_2 = driver_dp.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[2]/dd').text
        # ideal for
        bi_3 = driver_dp.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[3]/dd').text
        # expiration date
        bi_4 = driver_dp.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[4]/dd').text
        # how to use
        bi_5 = driver_dp.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[5]/dd').text
        # manufacturer/distributor
        bi_6 = driver_dp.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[6]/dd').text
        # country of manufacture
        bi_7 = driver_dp.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[7]/dd').text
        # ingredients
        bi_8 = driver_dp.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[8]/dd').text
        # MFDS Evaluation of functional cosmetics
        bi_9 = driver_dp.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[9]/dd').text
        # cautions for use
        bi_10 = driver_dp.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[10]/dd').text
        # quality assurance standard
        bi_11 = driver_dp.find_element(By.XPATH, '//*[@id="artcInfo"]/dl[11]/dd').text
        # customer service

        # 리뷰 prd_detail_tab>id=reviewInfo
        ri_1_raw = driver_dp.find_element(By.XPATH, '//*[@id="reviewInfo"]/a/span').text
        ri_1 = re.findall(f'\((.*?)\)', ri_1_raw)[0]

        # Q&A  prd_detail_tab>id=qnaInfo
        qi_1_raw = driver_dp.find_element(By.XPATH, '//*[@id="qnaInfo"]/a/span').text
        qi_1 = re.findall(f'\((.*?)\)', qi_1_raw)[0]

        #时间戳
        rightnow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 存储到字典文件
        dict = {
                '产品编码' : product_code,
                '产品名称' : dp_name,
                '产品缩略图' : dp_img,
                '销售价' : dp_price2,
                '市场价' : dp_price1,
                '评论数' : ri_1,
                'Q&A' : qi_1,
                '促销1세일' : dp_promo1,
                '促销2오늘드림' : dp_promo2,
                '促销3증정' : dp_promo3,
                '促销41+1' : dp_promo4,
                '促销5쿠폰' : dp_promo5,
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
                '当前网址': url_dp,
                '当前时间': rightnow,
                }
        print(dp_name, dp_price2, dp_promo1, brand_name, bi_1, bi_4)
        csv_writer.writerow(dict)
        print(f'==========下载完成==========', dp_name, product_code,f'时间：', rightnow)
        driver_dp.close()
        driver_dp.quit()
    print(f'===采集完成===累计耗时：', time.time() - time_1, rightnow)