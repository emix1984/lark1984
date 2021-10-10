import requests
import parsel
import csv

for page in range (1,30):
    print(f'==================正在爬取{page}页内容=======================')

    url = f'https://www.coupang.com/vp/product/reviews?productId=133257156&page={page}&size=5&sortBy=ORDER_SCORE_ASC&ratings=&q=&viRoleCode=3&ratingSummary=true'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.99 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    html_data = response.text

    selector = parsel.Selector(html_data)
    lis = selector.css('body > article').getall() # body > article > div.sdp-review__article__list__info > div.sdp-review__article__list__info__user > span::text

    for li in lis:
        selector_1 = parsel.Selector(li)
        user = selector_1.css('div.sdp-review__article__list__info > div.sdp-review__article__list__info__user > span::text').get()
        time = selector_1.css('div.sdp-review__article__list__info > div.sdp-review__article__list__info__product-info > div.sdp-review__article__list__info__product-info__reg-date::text').get()
        title = selector_1.css('div.sdp-review__article__list__info > div.sdp-review__article__list__info__product-info__name::text').get()
        headline = selector_1.css('div.sdp-review__article__list__headline::text').get()
        review_content = selector_1.css('div.sdp-review__article__list__review.js_reviewArticleContentContainer > div').get()
        img_url = selector_1.css('div.sdp-review__article__list__attachment.js_reviewArticleListGalleryContainer > div > img::attr(src)').get()
        img_url_origin = selector_1.css('div.sdp-review__article__list__attachment.js_reviewArticleListGalleryContainer > div > img::attr(data-origin-path)').get()

        print(user, time, title, headline, review_content, img_url,img_url_origin)
        with open('coupang_product_reviews_data.csv', mode='a', encoding='utf-8', newline="") as f:
            csv_write = csv.writer(f)
            csv_write.writerow([user, time, title, headline, review_content, img_url,img_url_origin])
f.close()