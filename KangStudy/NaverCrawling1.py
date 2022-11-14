# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# import pandas as pd #엑셀화 판다스
# from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys #키보드
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pyperclip
import time
import QT as ui

# options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()

# 페이지 이동
def move(url):
    driver.get(url)
    driver.implicitly_wait(2)

# 로그인 입력
def login(id, pw):
    # 아이디 및 비밀번호 입력
    pyperclip.copy(id)
    driver.find_element(By.ID, "id").click()
    driver.find_element(By.ID, "id").send_keys(Keys.CONTROL, 'v')
    pyperclip.copy(pw)
    driver.find_element(By.ID, 'pw').click()
    driver.find_element(By.ID, 'pw').send_keys(Keys.CONTROL, 'v')
    # 로그인 클릭
    driver.find_element(By.ID, 'log.login').click()
    time.sleep(1)

# 카페 검색창에 검색
def search(item):
    pyperclip.copy(item)
    search = driver.find_element(By.NAME, "query")
    search.click()
    search.send_keys(Keys.CONTROL, 'v')
    driver.find_element(By.XPATH, '//*[@id="info-search"]/form/button').click()
    driver.implicitly_wait(5)
# 뉴스 크롤링하기(제목, url)
def C_News():
    try:
        # 페이지의 소스를 가져와서 페이지마다 이동하는 url을 바로 저장
        soup = bs(driver.page_source, "lxml")
        s_page = soup.select('a.press_edit_news_link._es_pc_link') # 뉴스페이지 가져오기
        s_title = soup.select('span.press_edit_news_title') # 뉴스제목 가져오기
        # print(news) # 확인용

        # 해당 태그에서 한개씩 url만 가져오기
        for n,t in zip(s_page, s_title):
            url = n['href']
            url_list.append(url) # url_list에 추가하기
            # 제목 추가하기
            title_list.append(t.text)
            # print(t.text) # 확인용
    except Exception as e:
        print(e)
        print("뉴스 크롤링 중 오류 발생")


# 1. 로그인하기
login_url = "https://nid.naver.com/nidlogin.login"
# 1-1. 로그인 페이지로 이동
move(login_url)
# 1-2. 아이디와 비밀번호 입력하기
# id = ui.WindowClass.id
login('아이디', '비번'); time.sleep(5)
# 2. 뉴스 크롤링하기
hankuk_url = 'https://media.naver.com/press/015?sid=101'
move(hankuk_url) # 한국경제 뉴스버튼을 클릭하면 페이지로 이동함

url_list = [] #url저장 리스트
title_list = [] #뉴스 제목 리스트
# 2-1. 뉴스 페이지와 제목 크롤링하여 리스트에 저장
C_News()
# 2-2. 뉴스 페이지마다 들어가서 기사내용, 날짜, 내용 크롤링해서 저장

# 웹 종료
driver.close()