from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd #엑셀화 판다스
from selenium.webdriver.common.keys import Keys #키보드
from bs4 import BeautifulSoup as bs

driver = webdriver.Chrome(ChromeDriverManager().install())