import requests

url = f''
headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.114 Safari/537.36'
        }
timeout = 5 # 设置超时秒数

# 发送请求
# response = requests.get(url=url_dp, headers=headers, timeout=timeout)
    html_data_dp = response.text