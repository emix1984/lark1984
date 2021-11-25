import requests

url = 'https://www.google.com'
response = requests.get(url)
print(response.text)
if 'head' in response.text:
    print('200yes')
else:
    print(response)