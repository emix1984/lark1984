from time import sleep
import time
import random
import requests
import parsel
import re
import csv
import pandas as pd

n = 0 # 计数初始化
# 项目计时用
time_start = time.time()
# 设置随机间歇时间
# time_sleep = random.random()*6

# 创建csv文件和表头
f = open('03_oliveyoung_detailpage_data99.csv', mode='a', encoding='utf-8', newline='')
print(f'\033[32m>>>创建csv文件完毕！！！<<<\033[0m')
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
        '化妆品制造企业',
        '化妆品销售企业',
        '制造国家',
        '成分',
        '功能性化妆品',
        '使用注意事项',
        '品质保证基准',
        '售后服务电话',
        '医药外用品品名&型号',
        '认证许可',
        '进口产品KC认证有无',
        '颜色',
        '材质',
        '使用年龄',
        '同一型号产品上市日期',
        '电压功耗',
        '产品主要构成',
        '当前网址',
        '当前时间',
])
# csv_writer.writeheader()
# print(f'\033[32m>>> csv文件<表头>写入完毕 <<<\033[0m')

# pandas 拉取 listing.csv数据中的产品详情页链接
df_listing = pd.read_csv('02_oliveyoung_listing04.csv')
data01 = pd.DataFrame(df_listing)
print(f'\033[32m>>>读取listing.csv文件，进行去重操作中<<<\033[0m', '读取数据条目共计： ', len(data01), '条')
data02 = data01.drop_duplicates("产品链接") # 去除重复链接
print(f'\033[32m>>>数据去重操作已完成<<<\033[0m', '去重操作数据共计： ', len(data02), '条')
urls_detailpage = data02["产品链接"]

for url_dp in urls_detailpage:
    n = n + 1 # 计数
    headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.114 Safari/537.36'
        }
    timeout = 5 # 设置超时秒数
    # 发送请求
    response = requests.get(url=url_dp, headers=headers, timeout=timeout)
    html_data_dp = response.text
    selector_dp = parsel.Selector(html_data_dp)
    # sleep(time_sleep) # 等待页面加载3秒
    # print(html_data_dp)

    if "상품을 찾을 수 없습니다" in html_data_dp:
        print(f'>>>\033[00;41m第{n}条数据页面内商品不存在或已下架！\033[0m', url_dp)
        product_code = "",
        dp_name = "상품을 찾을 수 없습니다",
        dp_img = "",
        dp_price2 = "",
        dp_price1 = "",
        ri_1 = "",
        qi_1 = "",
        dp_promo1 = "",
        dp_promo2 = "",
        dp_promo3 = "",
        dp_promo4 = "",
        dp_promo5 = "",
        brand_name = "",
        brand_id = "",
        brand_logo = "",
        detailpage_img = "",
        bi_1 = "",
        bi_2 = "",
        bi_3 = "",
        bi_4 = "",
        bi_5 = "",
        bi_6 = "",
        bi_7 = "",
        bi_8 = "",
        bi_9 = "",
        bi_10 = "",
        bi_11 = "",
        bi_12 = "",
        bi_13 = "",
        bi_14 = "",
        bi_15 = "",
        bi_16 = "",
        bi_17 = "",
        bi_18 = "",
        bi_19 = "",
        bi_20 = "",
    else:
        print(f'\033[00;42m>>>正在采集第{n}条数据\033[0m 地址：', url_dp)
        # sleep(time_sleep) # 等待页面加载1秒

        # detail page - product info
        # 产品名称
        product_code = re.findall(f'goodsNo=(.*?)&', url_dp, re.S)[0]
        dp_name = selector_dp.xpath('//*[@id="Contents"]/div[2]/div[2]/div/p[2]/text()').extract()[0]
        dp_img = selector_dp.xpath('//*[@id="mainImg"]/@src').extract()[0]
        # print(product_code, dp_name, dp_img)

        # 开始判断是否存在 price-1 标签, <strike></strike>是唯一一个price-1标签用到的html标签
        if "strike" in html_data_dp:
                dp_price1 = selector_dp.xpath('//*[@class="price-1"]/strike/text()').extract()[0]
                dp_price2 = selector_dp.xpath('//*[@class="price-2"]/strong/text()').extract()[0]
        else:
                dp_price2 = selector_dp.xpath('//*[@class="price-2"]/strong/text()').extract()[0]
                dp_price1 = selector_dp.xpath('//*[@class="price-2"]/strong/text()').extract()[0]
        # print(dp_price1, dp_price2)

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

        # 品牌馆相关信息 class=brand_like
        brand_name_raw = selector_dp.xpath('//*[@id="moveBrandShop_like"]/em/text()').extract()[0]
        brand_name = brand_name_raw.replace(' 브랜드관', "")
        brand_logo_raw = selector_dp.xpath('//*[@id="moveBrandShop_like"]/span/@style').extract()[0]
        brand_logo = re.findall(r'\'(.*?)\'', brand_logo_raw)[0]
        brand_id = selector_dp.xpath('//*[@id="brnd_wish"]/@data-ref-onlbrndcd').extract()[0]
        # print(brand_name, brand_id, brand_logo)

        # 상품설명 prd_detail_tab>id=productInfo
        detailpage_img = "" # 后续待处理

        # 标签页2产品详细信息 구매정보 prd_detail_tab>id=buyInfo
        # 构建产品信息post请求
        url_getGoodsArtcAjax = 'https://www.oliveyoung.co.kr/store/goods/getGoodsArtcAjax.do'
        preload = {
            'goodsNo': f'{product_code}',
            'itemNo': '001',
            'pkgGoodsYn': 'N',
        }
        response_dp_tab = requests.post(url_getGoodsArtcAjax, data=preload, headers=headers, timeout=timeout)
        html_data_dp_tab_raw = response_dp_tab.text
        # bi_1 = html_data.replace(" ", "").replace("\t", "").strip()
        html_data_dp_tab = html_data_dp_tab_raw.replace("\n", "").replace("\t", "")
        # print(html_data_dp_tab)
        selector_dp_tab = parsel.Selector(html_data_dp_tab)
        lis_dp_tab = selector_dp_tab.xpath('//*[@class="detail_info_list"]/dt/text()').extract()

        # 打开tab之后判断产品是<化妆品화장품>，还是医药外用品<의약외품>,2021.11.30改成属性项目是否存在，存在就采集相关属性，不存在就留空
        # 需要增加判断 空值 链接 https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000141302&dispCatNo=1000001000100100002&trackingCd=Cat1000001000100100002_Small&curation&egcode&rccode&egrankcode

        # 용량 또는 중량 volume/weight
        if "용량 또는 중량" in lis_dp_tab:
            bi_1 = re.findall(f'<dt>용량 또는 중량</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        elif "크기, 무게" in lis_dp_tab:
            # 크기, 무게 / 크기, 중량 / 용량 또는 중량 volume/weight
            bi_1 = re.findall(f'<dt>크기, 무게</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        elif "크기, 중량" in lis_dp_tab:
            # 크기, 중량 / 용량 또는 중량 volume/weight
            bi_1 = re.findall(f'<dt>크기, 중량</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        else:
            bi_1 = ""

        # 제품 주요 사양 ideal for
        if "제품 주요 사양" in lis_dp_tab:
            bi_2 = re.findall(f'<dt>제품 주요 사양</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        else:
            bi_2 = ""
        # 사용기간(개봉 후 사용기간) expiration date
        if "사용기간(개봉 후 사용기간)" in lis_dp_tab:
            bi_3 = re.findall(f'<dt>사용기간\(개봉 후 사용기간\)</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        else:
            bi_3 = ""

        # 사용방법 how to use
        if "제품의 사용목적 및 사용방법" in lis_dp_tab:
            bi_4 = re.findall(f'<dt>제품의 사용목적 및 사용방법</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        elif "사용방법" in lis_dp_tab:
            bi_4 = re.findall(f'<dt>사용방법</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        else:
            bi_4 = ""

        # 화장품제조업자 및 화장품책임판매업자 manufacturer/distributor
        if "화장품제조업자 및 화장품책임판매업자" in lis_dp_tab:
            bi_5 = re.findall(f'<dt>화장품제조업자 및 화장품책임판매업자</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
            if "/" in bi_5:
                # 通过判断区分화장품제조업자和화장품책임판매업자
                # 제조사
                bi_5_1_raw = re.findall(r"(.*)/", bi_5, re.S)[0]
                if ":" in bi_5_1_raw:
                    bi_5_1_raw_raw = re.findall(r":(.*)", bi_5_1_raw, re.S)[0]
                    bi_5_1 = "".join(bi_5_1_raw_raw).strip()
                else:
                    bi_5_1 = "".join(bi_5_1_raw).strip()
                # 판매업자
                bi_5_2_raw = re.findall(r"/(.*)", bi_5, re.S)[0]
                if ":" in bi_5_2_raw:
                    bi_5_2_raw_raw = re.findall(r":(.*)", bi_5_2_raw, re.S)[0]
                    bi_5_2 = "".join(bi_5_2_raw_raw).strip()
                else:
                    bi_5_2 = "".join(bi_5_2_raw).strip()
            elif ":" in bi_5:
                if "제조" in bi_5:
                    bi_5_1_raw = re.findall(r"제조.*:(.*)", bi_5, re.S)[0]
                    bi_5_1 = "".join(bi_5_1_raw).strip()
                else:
                    bi_5_1 = ""

                if "제조판매업자ㅣ" in bi_5:
                    bi_5_2_raw = re.findall(r"판매.*ㅣ(.*)", bi_5, re.S)[0]
                    bi_5_2 = "".join(bi_5_2_raw).strip()
                elif "제조판매업자 (주)" in bi_5:
                    bi_5_2_raw = re.findall(r"제조판매업자 \(주\)(.*)", bi_5, re.S)[0]
                    bi_5_2 = "".join(bi_5_2_raw).strip()
                elif "판매" in bi_5:
                    bi_5_2_raw = re.findall(r"판매.*:(.*)", bi_5, re.S)[0]
                    bi_5_2 = "".join(bi_5_2_raw).strip()
                else:
                    bi_5_2 = ""
            else:
                bi_5_1 = bi_5_2 = bi_5
        elif "제조자" in lis_dp_tab:
            # 제조자 / 화장품제조업자 및 화장품책임판매업자 manufacturer/distributor
            bi_5 = re.findall(f'<dt>제조자</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
            if "/" in bi_5:
                # 通过判断区分화장품제조업자和화장품책임판매업자
                # 제조사
                bi_5_1_raw = re.findall(r"(.*)/", bi_5, re.S)[0]
                if ":" in bi_5_1_raw:
                    bi_5_1_raw_raw = re.findall(r":(.*)", bi_5_1_raw, re.S)[0]
                    bi_5_1 = "".join(bi_5_1_raw_raw).strip()
                else:
                    bi_5_1 = "".join(bi_5_1_raw).strip()
                # 판매업자
                bi_5_2_raw = re.findall(r"/(.*)", bi_5, re.S)[0]
                if ":" in bi_5_2_raw:
                    bi_5_2_raw_raw = re.findall(r":(.*)", bi_5_2_raw, re.S)[0]
                    bi_5_2 = "".join(bi_5_2_raw_raw).strip()
                else:
                    bi_5_2 = "".join(bi_5_2_raw).strip()
            else:
                bi_5_1 = bi_5_2 = bi_5
        else:
            bi_5 = ""
            bi_5_1 = ""
            bi_5_2 = ""

        # 제조국 country of manufacture
        if "제조국" in lis_dp_tab:
            bi_6 = re.findall(f'<dt>제조국</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        else:
            bi_6 = ""

        # 화장품법에 따라 기재해야 하는 모든 성분 ingredients
        if "화장품법에 따라 기재해야 하는 모든 성분" in lis_dp_tab:
            bi_7 = re.findall(f'<dt>화장품법에 따라 기재해야 하는 모든 성분</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        else:
            bi_7 = ""

        # 기능성 화장품 식품의약품안전처 심사필 여부 MFDS Evaluation of functional cosmetics
        if "기능성 화장품 식품의약품안전처 심사필 여부" in lis_dp_tab:
            bi_8 = re.findall(f'<dt>기능성 화장품 식품의약품안전처 심사필 여부</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        else:
            bi_8 = ""

        # 사용시 주의사항 cautions for use
        if "사용시 주의사항" in lis_dp_tab:
            bi_9 = re.findall(f'<dt>사용시 주의사항</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        elif "취급방법 및 주의사항" in lis_dp_tab:
            # 취급방법 및 주의사항 / 사용시 주의사항 cautions for use
            bi_9 = re.findall(f'<dt>취급방법 및 주의사항</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        else:
            bi_9 = ""

        # 품질보증기준 quality assurance standard
        if "품질보증기준" in lis_dp_tab:
            bi_10 = re.findall(f'<dt>품질보증기준</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        else:
            bi_10 = ""

        # 소비자상담 전화번호 customer service
        if "소비자상담 전화번호" in lis_dp_tab:
            bi_11 = re.findall(f'<dt>소비자상담 전화번호</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        elif "A/S 책임자 / 전화번호" in lis_dp_tab:
            # A/S 책임자 / 전화번호 / 소비자상담 전화번호 customer service
            bi_11 = re.findall(f'<dt>A/S 책임자 / 전화번호</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        else:
            bi_11 = ""

        # 以下bi_12开始，非化妆品类产品追加属性变数
        # 품명 및 모델명
        if "품명 및 모델명" in lis_dp_tab:
            bi_12 = re.findall(f'<dt>품명 및 모델명</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        else:
            bi_12 = ""

        # 인증·허가
        if "인증·허가" in lis_dp_tab:
            bi_13 = re.findall(f'<dt>인증·허가</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        else:
            bi_13 = ""

        # KC 인증 필 유무
        if "KC 인증 필 유무" in lis_dp_tab:
            bi_14 = re.findall(f'<dt>KC 인증 필 유무</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        else:
            bi_14 = ""

        # 색상
        if "색상" in lis_dp_tab:
            bi_15 = re.findall(f'<dt>색상</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        else:
            bi_15 = ""

        # 재질
        if "재질" in lis_dp_tab:
            bi_16 = re.findall(f'<dt>재질</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        else:
            bi_16 = ""

        # 사용연령(체중범위)
        if "사용연령(체중범위)" in lis_dp_tab:
            bi_17 = re.findall(f'<dt>사용연령\(체중범위\)</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        else:
            bi_17 = ""

        # 동일 모델 출시년월
        if "동일 모델 출시년월" in lis_dp_tab:
            bi_18 = re.findall(f'<dt>동일 모델 출시년월</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        else:
            bi_18 = ""

        # 정격전압, 소비전력
        if "정격전압, 소비전력" in lis_dp_tab:
            bi_19 = re.findall(f'<dt>정격전압, 소비전력</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        else:
            bi_19 = ""

        # 주요 사양 剃须刀产品主要构成
        if "제품 주요 사양" in lis_dp_tab:
            bi_20 = re.findall(f'<dt>제품 주요 사양</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        elif "주요 사양" in lis_dp_tab:
            bi_20 = re.findall(f'<dt>주요 사양</dt><dd>(.*?)</dd>', html_data_dp_tab)[0]
        else:
            bi_20 = ""


        # 리뷰 prd_detail_tab>id=reviewInfo
        ri_1_raw = selector_dp.xpath('//*[@id="reviewInfo"]/a/span/text()').extract()[0]
        ri_1 = re.findall(f'\((.*?)\)', ri_1_raw)[0]

        # Q&A  prd_detail_tab>id=qnaInfo
        qi_1_raw = selector_dp.xpath('//*[@id="qnaInfo"]/a/span/text()').extract()[0]
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
            '化妆品制造企业': bi_5_1,
            '化妆品销售企业': bi_5_2,
            '制造国家': bi_6,
            '成分': bi_7,
            '功能性化妆品': bi_8,
            '使用注意事项': bi_9,
            '品质保证基准': bi_10,
            '售后服务电话': bi_11,
            '医药外用品品名&型号': bi_12,
            '认证许可': bi_13,
            '进口产品KC认证有无': bi_14,
            '颜色': bi_15,
            '材质': bi_16,
            '使用年龄': bi_17,
            '同一型号产品上市日期': bi_18,
            '电压功耗': bi_19,
            '产品主要构成': bi_20,
            '当前网址': url_dp,
            '当前时间': rightnow,
            }
    # print(dp_name, dp_price2, dp_promo1, brand_name, bi_1, bi_4)
    csv_writer.writerow(dict)
    print(f'\033[00;41m>>>数据写入完成：\033[0m', product_code, dp_name, f'\033[31m时间：\033[0m', rightnow)
time_end = time.time()
print(f'\033[31m===采集完成===累计耗时：\033[0m', time_end - time_start, rightnow)