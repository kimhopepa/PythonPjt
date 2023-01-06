from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyperclip
import time
from bs4 import BeautifulSoup as bs

class CrawlClass :
    def __init__(self):
        print("CrawlClass.__init__()")

    def initialize(self, site_text, id_text, pw_text):
        try:
            print("1. CrawlClass().initialize : webdriver.Chrome() ")
            self.browser = webdriver.Chrome()

            print("2. CrawlClass().initialize : browser.get ", site_text)
            self.browser.get(site_text)

            print("3. CrawlClass().initialize : find_element")
            elem = self.browser.find_element(By.CLASS_NAME, 'link_login')
            elem.click()

            # 3. id 복사 붙여넣기
            elem_id = self.browser.find_element_by_id('id')
            elem_id.click()
            pyperclip.copy(id_text)
            elem_id.send_keys(Keys.CONTROL, 'v')
            time.sleep(1)

            # 4. pw 복사 붙여넣기
            elem_pw = self.browser.find_element_by_id('pw')
            elem_pw.click()
            pyperclip.copy(pw_text)
            elem_pw.send_keys(Keys.CONTROL, 'v')
            time.sleep(1)

            self.browser.find_element_by_id('log.login').click()

        except Exception as e:
            print("Exception : CrawlClass.initialize()", e)
    def search(self, search_text):
        url_list = []  # url저장 리스트
        title_list = []  # 뉴스 제목 리스트
        try :
            print("1. CrawlClass.search()", search_text)
            self.move(search_text)

            print("2. CrawlClass.search() - soup")
            soup = bs(self.browser.page_source, "lxml")

            print("4. CrawlClass.search() - select")
            soup_page_list = soup.select('a.press_edit_news_link._es_pc_link') # 뉴스페이지 가져오기
            soup_title_list = soup.select('span.press_edit_news_title') # 뉴스제목 가져오기
            # print(news) # 확인용

            # 해당 태그에서 한개씩 url만 가져오기
            for page,title in zip(soup_page_list, soup_title_list):
                url = page['href']
                url_list.append(url)
                title_list.append(title.text)
            print("5. CrawlClass.search() - end")
        except Exception as e:
            print("Exception : CrawlClass.search", e)

        return url_list, title_list
    def move(self, url):
        try :
            self.browser.get(url)
            self.browser.implicitly_wait(2)
        except Exception as e:
            print("Exception : CrawlClass.move()", e)

