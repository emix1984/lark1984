import pprint
from time import sleep
import pandas as pd
import requests
import parsel
import json
import csv
import re
import time

# 创建csv文件和表头
f = open(f'03_coupang_detailpage_data.csv', mode='a', encoding='utf-8', newline='')
print(f'\033[32m>>>创建csv文件完毕！！！<<<\033[0m')
csv_writer = csv.DictWriter(f, fieldnames=[
    'productId',
    'itemId',
    'vendoritems',
    '产品名称',
    '产品缩略图',
    '销售价',
    '折扣',
    '市场价',
    '每毫升单价',
    '评论数',
    '品牌',
    '品牌链接',
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
    '流通公司名称',
    '流通公司营业执照号码',
    '流通公司通信销售申告号码',
    '流通公司地址',
    '流通公司邮箱',
    '流通公司联系人',
    '流通公司联系电话',
    '流通公司&法人姓名',
    '当前网址',
    '当前时间',
])
csv_writer.writeheader()
print(f'\033[32m>>> csv文件<表头>写入完毕 <<<\033[0m')

# 计数初始化
n = 0

# 项目计时用
time_start = time.time()
# 设置随机间歇时间
# time_sleep = random.random()*6

# pandas 拉取 listing.csv数据中的产品详情页链接
df_listing = pd.read_csv('02_coupang_listing.csv')
data01 = pd.DataFrame(df_listing)
print(f'\033[32m>>>读取listing.csv文件，进行去重操作中<<<\033[0m', '读取数据条目共计： ', len(data01), '条')
data02 = data01.drop_duplicates("产品链接")  # 去除重复链接
print(f'\033[32m>>>数据去重操作已完成<<<\033[0m', '去重操作数据共计： ', len(data02), '条')
urls_detailpage = data02["产品链接"]

for url_detailpage in urls_detailpage:
    # 计数
    n = n+1
    print(f'>>>正在采集第\033[32m{n}\033[0m条数据', url_detailpage)
    # url_detailpage = 'https://www.coupang.com/vp/products/246379487?itemId=780629226&vendorItemId=79769806875&sourceType=CATEGORY&categoryId=486148'

    productId = re.findall(f'products/(.*?)\?', url_detailpage)[0]
    itemId = re.findall(f'itemId=(.*?)&', url_detailpage)[0]
    vendoritems = re.findall(f'vendorItemId=(.*?)&', url_detailpage)[0]

    headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44',
        }
    response = requests.get(url=url_detailpage, headers=headers)
    html_data_url = response.text
    if "상품을 찾을 수 없습니다"not in html_data_url:

        selector_detailpage = parsel.Selector(html_data_url)

        # 类目
        category1_name = selector_detailpage.xpath('//*[@id="breadcrumb"]/li[2]/a[@title]/@title').get()
        category2_name = selector_detailpage.xpath('//*[@id="breadcrumb"]/li[3]/a[@title]/@title').get()
        category3_name = selector_detailpage.xpath('//*[@id="breadcrumb"]/li[4]/a[@title]/@title').get()

        # brand name
        brand_name = selector_detailpage.xpath('//*[@id="contents"]/div[1]/div/div[3]/a/text()').get()
        # 品牌链接
        brand_url = selector_detailpage.xpath('//*[@id="contents"]/div[1]/div/div[3]/a[@href]/@href').get()

        # 产品名
        prod_buy_header_title = selector_detailpage.xpath('//*[@id="contents"]/div[1]/div/div[3]/div[3]/h2/text()').get()
        # 产品缩略图
        dp_img_raw = selector_detailpage.xpath('//*[@id="repImageContainer"]/img[@src]/@src').get()
        dp_img = "https:"+dp_img_raw

        # 产品评论数
        reviews_count = selector_detailpage.xpath('//*[@id="prod-review-nav-link"]/span[2]/text()').get()
        # 折扣sale
        discount_rate = selector_detailpage.xpath('//*[@id="contents"]/div[1]/div/div[3]/div[5]/div[1]/div/div[1]/span[1]/text()').get().strip()
        # 市场价
        origin_price = selector_detailpage.xpath('//*[@id="contents"]/div[1]/div/div[3]/div[5]/div[1]/div/div[1]/span[2]/text()').get()
        # 销售价
        prod_sale_price = selector_detailpage.xpath('//*[@id="contents"]/div[1]/div/div[3]/div[5]/div[1]/div/div[2]/span[1]/strong/text()').get()
        # 每毫升克容量单价
        unit_price = selector_detailpage.xpath('//*[@id="contents"]/div[1]/div/div[3]/div[5]/div[1]/div/div[2]/span[2]/text()').get()

        ## 产品主要卖点prod-description
        # prod-description-attribute
        # prod_attr_item = selector_detailpage.xpath('//*[@class="prod-description"]/ul/li/text()').get()
        # print(prod_attr_item)
        # print(prod_buy_header_title, reviews_count,discount_rate,origin_price,prod_sale_price,unit_price,)

        ## 产品review_tab请求链接
        ## https://www.coupang.com/vp/product/reviews?productId=344529480&page=1&size=5&sortBy=ORDER_SCORE_ASC&ratings=&q=&viRoleCode=3&ratingSummary=true

        ## 销售公司信息
        ## 与产品属性的tab在同一个json里
        ## https://www.coupang.com/vp/products/5735830650/items/9639246678/vendoritems/76923492094
        ## 从产品详情页地址可以得到productId, itemId, vendoritems.
        url_detailpage_itemBrief = f'https://www.coupang.com/vp/products/{productId}/items/{itemId}/vendoritems/{vendoritems}'

        response_detailpage_itemBrief = requests.get(url=url_detailpage_itemBrief, headers=headers)
        response_itemBrief = response_detailpage_itemBrief.text
        detailpage_itemBrief_json_data = json.loads(response_itemBrief)
        # pprint.pprint(detailpage_itemBrief_json_data)

        lis_essentials = detailpage_itemBrief_json_data['essentials']
        for bi in lis_essentials:
            bi_title = bi['title']
            bi_description = bi['description']

            # 용량 중량
            if '용량(중량)' in bi_title:
                bi_1 = bi_description
            else:
                bi_1 = ""
            # 제품 주요 사양
            if '제품 주요 사양' in bi_title:
                bi_2 = bi_description
            else:
                bi_2 = ""
            # 사용기한 또는 개봉 후 사용기간
            if '사용기한' in bi_title:
                bi_3 = bi_description
            else:
                bi_3 = ""
            # 사용방법
            if '사용방법' in bi_title:
                bi_4 = bi_description
            else:
                bi_4 = ""

            # 화장품제조업자 및 화장품책임판매업자
            if '화장품제조업자 및 화장품책임판매업자' in bi_title:
                bi_5 = bi_description
                if "/" in bi_5:
                    # 通过判断区分화장품제조업자和화장품책임판매업자
                    # 제조사
                    bi_5_1_raw = re.findall(r"(.*)/", bi_5, re.S)[0]
                    bi_5_1 = "".join(bi_5_1_raw).strip()
                    # 판매업자
                    bi_5_2_raw = re.findall(r"/(.*)", bi_5, re.S)[0]
                    bi_5_2 = "".join(bi_5_2_raw).strip()
                elif ":" in bi_5:
                    # 通过判断区分화장품제조업자和화장품책임판매업자
                    # 제조사
                    bi_5_1_raw = re.findall(r"(.*):", bi_5, re.S)[0]
                    bi_5_1 = "".join(bi_5_1_raw).strip()
                    # 판매업자
                    bi_5_2_raw = re.findall(r":(.*)", bi_5, re.S)[0]
                    bi_5_2 = "".join(bi_5_2_raw).strip()
            else:
                bi_5 = ""
                bi_5_1 = ""
                bi_5_2 = ""

            # 제조국
            if '제조국' in bi_title:
                bi_6 = bi_description
            else:
                bi_6 = ""
            # 성분
            if '표시하여야 하는 모든 성분' in bi_title:
                bi_7 = bi_description
            else:
                bi_7 = ""

            # 기능성 화장품
            if '식품의약품안전처 심사필 유무 (기능성 화장품)' in bi_title:
                bi_8 = bi_description
            else:
                bi_8 = ""

            # 주의사항
            if '주의사항' in bi_title:
                bi_9 = bi_description
            else:
                bi_9 = ""

            # 품질보증기준
            if '품질보증기준' in bi_title:
                bi_10 = bi_description
            else:
                bi_10 = ""

            # 소비자상담관련 전화번호
            if '소비자상담관련 전화번호' in bi_title:
                bi_11 = bi_description
            else:
                bi_11 = ""
            # print(bi_1, bi_2,bi_3,bi_4,bi_5,bi_6,bi_7,bi_8,bi_9, bi_10, bi_11)
        ## returnPolicyVo 退换政策销售者公司信息
        # 사업자번호
        bizNum = detailpage_itemBrief_json_data['returnPolicyVo']['sellerDetailInfo']['bizNum']
        # 判断coupang直营和第三方专营
        if bizNum == 0:
            bizNum = ""
            ecommReportNum = ""
            # 사업장 소재지
            repAddress = ""
            # e-mail
            repEmail = ""
            # 联系人姓名
            repPersonName = ""
            # 연락처
            repPhoneNum = ""
            # 상호/대표자
            sellerWithRepPersonName = "쿠팡(주) / 강한승,박대준"
            # 商号
            vendorName = "쿠팡"
        else:
            # 통신판매업 신고번호
            ecommReportNum = detailpage_itemBrief_json_data['returnPolicyVo']['sellerDetailInfo']['ecommReportNum']
            # 사업장 소재지
            repAddress = detailpage_itemBrief_json_data['returnPolicyVo']['sellerDetailInfo']['repAddress']
            # e-mail
            repEmail = detailpage_itemBrief_json_data['returnPolicyVo']['sellerDetailInfo']['repEmail']
            # 联系人姓名
            repPersonName = detailpage_itemBrief_json_data['returnPolicyVo']['sellerDetailInfo']['repPersonName']
            # 연락처
            repPhoneNum = detailpage_itemBrief_json_data['returnPolicyVo']['sellerDetailInfo']['repPhoneNum']
            # 상호/대표자
            sellerWithRepPersonName = detailpage_itemBrief_json_data['returnPolicyVo']['sellerDetailInfo']['sellerWithRepPersonName']
            # 商号
            vendorName = detailpage_itemBrief_json_data['returnPolicyVo']['sellerDetailInfo']['vendorName']
        # print('流通商信息', bizNum,ecommReportNum,repAddress,repEmail, repPersonName,repPhoneNum, sellerWithRepPersonName, vendorName)

        #时间戳
        rightnow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # print(rightnow)
        print(bi_1, bi_2, bi_3, bi_4, bi_5, bi_6, bi_7, bi_8, bi_9, bi_10, bi_11)
        # 存储到字典文件
        dict = {
            'productId' : productId,
            'itemId' : itemId,
            'vendoritems' : vendoritems,
            '产品名称' : prod_buy_header_title,
            '产品缩略图' : dp_img,
            '销售价' : prod_sale_price,
            '折扣' : discount_rate,
            '市场价' : origin_price,
            '每毫升单价' : unit_price,
            '评论数' : reviews_count,
            '品牌' : brand_name,
            '品牌链接' : brand_url,
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
            '流通公司名称': vendorName,
            '流通公司营业执照号码': bizNum,
            '流通公司通信销售申告号码': ecommReportNum,
            '流通公司地址': repAddress,
            '流通公司邮箱': repEmail,
            '流通公司联系人': repPersonName,
            '流通公司联系电话': repPhoneNum,
            '流通公司&法人姓名': sellerWithRepPersonName,
            '当前网址': url_detailpage,
            '当前时间': rightnow,
            }
        # print(dp_name, dp_price2, dp_promo1, brand_name, bi_1, bi_4)
        csv_writer.writerow(dict)
    print(f'\033[31m时间：\033[0m', rightnow, f'\033[00;42m>>>写入数据：\033[0m', '品牌：', brand_name, '产品名称：', prod_buy_header_title)

    # else:
    #     prod_buy_header_title = "상품을 찾을 수 없습니다"
    #     dp_img = ""
    #     prod_sale_price = ""
    #     discount_rate = ""
    #     origin_price = ""
    #     unit_price = ""
    #     reviews_count = ""
    #     brand_name = ""
    #     brand_url = ""
    #     bi_1 = ""
    #     bi_2 = ""
    #     bi_3 = ""
    #     bi_4 = ""
    #     bi_5 = ""
    #     bi_6 = ""
    #     bi_7 = ""
    #     bi_8 = ""
    #     bi_9 = ""
    #     bi_10 = ""
    #     bi_11 = ""
    #     vendorName = ""
    #     bizNum = ""
    #     ecommReportNum = ""
    #     repAddress = ""
    #     repEmail = ""
    #     repPersonName = ""
    #     repPhoneNum = ""
    #     sellerWithRepPersonName = ""