import requests

url = 'https://www.coupang.com/'
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
        }

response = requests.get(url=url, headers=headers)
print(response)
ratings_review_option =['','1','2','3','4','5']
for ratings_review in ratings_review_option:
        print(ratings_review)