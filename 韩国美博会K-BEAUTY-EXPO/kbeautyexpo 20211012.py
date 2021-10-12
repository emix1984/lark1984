# 未完成
# 网址 https://k-beautyexpo.co.kr/fairOnline.do?selAction=single_page&SYSTEM_IDX=22&FAIRMENU_IDX=11843&hl=KOR#/?selDynamicInput=%5B%22_select_mod3981_in1%22,%22_select_mod3981_in2%22,%22_select_mod3981_in3%22,%22_select_mod3981_in5%22,%22_select_mod3981_in6%22,%22_select_mod3981_in7%22,%22_select_mod3981_in8%22,%22_select_mod3981_in9%22,%22_select_mod3981_in10%22,%22_select_mod3981_in11%22,%22_select_mod3981_in12%22,%22_phonemeKor_mod3982_in1%22,%22_phonemeEng_mod3982_in2%22%5D&TYPE=uci&selPageNo=42&searchText=
# Request URL: https://k-beautyexpo.co.kr/fairOnline.do
# Request Method: POST

import requests

url = f'https://k-beautyexpo.co.kr/fairOnline.do?selAction=single_page&SYSTEM_IDX=22&FAIRMENU_IDX=11843&hl=KOR#/?selDynamicInput=%5B%22_select_mod3981_in1%22,%22_select_mod3981_in2%22,%22_select_mod3981_in3%22,%22_select_mod3981_in5%22,%22_select_mod3981_in6%22,%22_select_mod3981_in7%22,%22_select_mod3981_in8%22,%22_select_mod3981_in9%22,%22_select_mod3981_in10%22,%22_select_mod3981_in11%22,%22_select_mod3981_in12%22,%22_phonemeKor_mod3982_in1%22,%22_phonemeEng_mod3982_in2%22%5D&TYPE=uci&selPageNo=42&searchText='
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.99 Safari/537.36'
}

response = requests.post(url=url, headers=headers).text

print(response)