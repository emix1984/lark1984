from selenium import webdriver
import time
import csv

def get_product(word):
    driver.find_element_by_css_selector('#key').send_keys(word)
    driver.find_element_by_css_selector('#search-btn').click()

    driver.implicitly_wait(10)
    driver.maximize_window()

def drop_down():
    for x in range(1, 11, 2):
        time.sleep(0.5)
        j = x / 10
        js = "document.documentElement.scrollTop = document.documentElement.scrollHeight * %s" % j
        driver.execute_script(js)

def parse_data():
    lis = driver.find_elements_by_css_selector('.gl-item')
    print(lis)

    for li in lis:
        try:
            name = li.find_element_by_css_selector('div.p-name a em').text
            name = name.replace('京东超市', '').replace('"', "").replace('\n', "")
            price = li.find_element_by_css_selector('div.p-price strong i').text + "元"
            deals = li.find_element_by_css_selector('div.p-commit strong a').text
            title = li.find_element_by_css_selector('span.J_im_icon a').text
            print(name, price,deals, title, sep=' | ')

            with open('data.csv', mode='a', encoding='utf-8', newline="") as f:
                csv_write = csv.writer(f)
                csv_write.writerow([name, price, deals, title])
        except:
             pass

def get_next():
    driver.find_element_by_css_selector('#J_bottomPage > span.p-num > a.pn-next > em').click()

keyword = input('请输入你想要搜索的商品关键字')

driver = webdriver.Chrome(executable_path='C:\Program Files\Google\Chrome\Application\chromedriver.exe')
driver.get('https://www.jd.com')

get_product(keyword)

for page in range(1,101):
    drop_down()
    parse_data()
    get_next()

input()
driver.quit()