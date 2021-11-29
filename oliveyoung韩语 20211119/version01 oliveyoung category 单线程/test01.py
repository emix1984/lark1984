# 20211129 测试request post方式获取tab信息
import requests
import re
goodsNos = {}
print(type(goodsNos))
goodsNos = ["A000000159230", "A000000156209",]
print(goodsNos)
for goodsNo in goodsNos:
    url = 'https://www.oliveyoung.co.kr/store/goods/getGoodsArtcAjax.do'
    preload = {
        'goodsNo': goodsNo,
        'itemNo': '001',
        'pkgGoodsYn': 'N',
    }
    response = requests.post(url, data=preload)
    html_data = response.text
    # bi_1 = html_data.replace(" ", "").replace("\t", "").strip()
    html_data1 = html_data.replace("\n", "").replace("\t", "")
    print(html_data1)
    print("=========")
    bi_1 = re.findall(f'<dt>용량 또는 중량</dt><dd>(.*?)</dd>', html_data1)[0]
    bi_2 = re.findall(f'<dt>제품 주요 사양</dt><dd>(.*?)</dd>', html_data1)[0]
    bi_3 = re.findall(f'<dt>사용기간\(개봉 후 사용기간\)</dt><dd>(.*?)</dd>', html_data1)[0]
    bi_4 = re.findall(f'<dt>소비자상담 전화번호</dt><dd>(.*?)</dd>', html_data1)[0]

    print(bi_1,bi_4)
    # print(response.text)
    print("=========")
