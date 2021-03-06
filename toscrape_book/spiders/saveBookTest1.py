import json
import time

import scrapy
from ..items import BookItem
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from scrapy.linkextractors import LinkExtractor
from selenium.webdriver.chrome.options import Options


class BooksSpider(scrapy.Spider):
    name = 'save1'
    allowed_domains = ['localhost:8086']
    start_urls = ['http://localhost:8086/list']

    def parse(self, response):
        f = open('D:\\pythonwork\\fullstack\\toscrape_book\\jsonFile.json', 'r')
        cookiessu = f.read()
        cookiessu = json.loads(cookiessu)
        # 进行循环
        for le in response.css('.booktr'):
            book = BookItem()
            # time.sleep(2)
            # 提取链接
            url1 = le.css('.bookUrl::text')
            # 提取密码
            pwd1 = le.css('.pwd::text')
            # id
            bookId1 = le.css('.bookid::text')
            # 书名
            bookname1 = le.css('.bookName::text')

            chrome_options = Options()
            # chrome_options.add_argument('headless')
            # chrome_options.add_argument("window-size=1920,1080")
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument('log-level=3')
            # browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome Beta\Application\chromedriver.exe')
            browser = webdriver.Chrome(chrome_options=chrome_options)
            print(browser.title)
            # 打开浏览器
            # browser = webdriver.Chrome()
            # 抽取具体链接
            url = url1[0].extract()
            # 抽取具体密码
            pwd = pwd1[0].extract()
            bookId = bookId1[0].extract()
            bookname = bookname1[0].extract()
            # url = 'https://pan.baidu.com/s/1_QuWZDoyPmsXNtYsCqqirA'
            # pwd = 'ci7y'

            # 请求目标地址
            browser.get(url)
            time.sleep(1)
            # 浏览器最大化
            # browser.maximize_window()
            time.sleep(1)
            if cookiessu != "":
                for cssu in cookiessu:
                    print(cssu)
                    browser.add_cookie(cssu)
                time.sleep(1)
            else:
                # 你的百度去帐号，保存到你的网盘肯定需要你自己的帐号密码
                user_name = ''
                password = ''
                # 登陆自己的百度云
                browser.find_element(By.CLASS_NAME, "CDaavKb").find_element_by_xpath(
                    '//*[@node-type="header-login-btn"]').click()
                time.sleep(4)
                browser.find_element(By.CLASS_NAME, "tang-pass-footerBarULogin").click()

                # 输入用户名密码
                time.sleep(5)
                user_name_input = browser.find_element(By.ID, "TANGRAM__PSP_10__userName")
                pwd_input = browser.find_element(By.ID, "TANGRAM__PSP_10__password")
                user_name_input.send_keys(user_name, Keys.ARROW_DOWN)
                pwd_input.send_keys(password, Keys.ARROW_DOWN)

                # 点击登陆
                browser.find_element(By.ID, "TANGRAM__PSP_10__submit").click()
                time.sleep(10)
                cookies = browser.get_cookies()
                print(cookies)
                jsObj = json.dumps(cookies)

                fileObject = open('jsonFile.json', 'w')
                fileObject.write(jsObj)
                fileObject.close()
                time.sleep(20)
            # browser.refresh()
            input_ = None
            # 获取输入分享密码的输入框
            try:
                input_ = browser.find_element(By.CLASS_NAME, "QKKaIE")
                # 输入分享密码
                input_.send_keys(pwd, Keys.ARROW_DOWN)
                # 获取提交按钮
                submit_button = browser.find_element(By.CLASS_NAME, "text")
                # 提交
                submit_button.click()
                time.sleep(2)
                # print(getCookie)
                # 保存到网盘

                browser.find_element_by_css_selector(".zbyDdwb").click()
                browser.find_element(By.CLASS_NAME, "x-button-box").find_element_by_xpath('//*[@data-button-id="b1"]').click()
                time.sleep(3)
                # 选取保存位置
                browser.find_element_by_xpath('//*[@node-path="/我的小书屋"]').click()
                time.sleep(2)
                browser.find_element(By.CLASS_NAME, "dialog-footer").find_element_by_xpath('//*[@data-button-id="b35"]').click()
                time.sleep(3)
                book['name'] = bookname
                book['url'] = url
                book['password'] = pwd
                book['save_state'] = 1
                book['id'] = bookId
            except:
                book['id'] = bookId
                book['save_state'] = 3
                print('保存失败')
                print('save faile :' + bookname)
                # fileObject = open('faile.txt', 'a',encoding='utf8')
                # fileObject.write(bookname)
                # fileObject.close()
            browser.close()
            browser.quit()
            yield book
        le = LinkExtractor(restrict_css='#weiye')
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)
    # try:
    # except:
    #     print('save faile :' + bookname)
    #     fileObject = open('faile.txt', 'w')
    #     fileObject.write(bookname)
    #     fileObject.close()
