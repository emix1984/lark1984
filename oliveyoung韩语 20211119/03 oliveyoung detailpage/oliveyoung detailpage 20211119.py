from time import sleep
from selenium import webdriver
import requests
import parsel

url = 'https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000145114&dispCatNo=1000001000200060003&trackingCd=Cat1000001000200060003_Small'
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.99 Safari/537.36'
    }

driver = webdriver.Chrome("D:\PycharmProjects\selenium\chromedriver.exe")
sleep(0.5)
driver.get(url)
sleep(3) #等待页面加载
driver.find_element_by_xpath('//*[@id="buyInfo"]/a').click() #登录
detailpage = driver.find_element_by_xpath('//*[@id="artcInfo"]/text()').getall()
print(detailpage)


#退出
# browser.close()
# browser.quit()