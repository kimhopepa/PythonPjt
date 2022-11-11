from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyperclip
import time

class CrawlClass :
    def __init__(self):
        self.init()

    def initialize(self, site_text, id_text, pw_text):
        print("CrawlClass.init()")

        self.browser = webdriver.Chrome()  # 현재파일과 동일한 경로일 경우 생략 가능

    def search(self, search_text):
        print("CrawlClass.init()", search_text)