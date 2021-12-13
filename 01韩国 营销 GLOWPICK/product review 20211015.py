import requests

url = 'https://www.glowpick.com/products/121312'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.47'
}

response = requests.get(url=url, headers=headers).text

print(response)