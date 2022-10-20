from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyperclip
import time

print("Start")
browser = webdriver.Chrome() # 현재파일과 동일한 경로일 경우 생략 가능
# driver = webdriver.Chrome(ChromeDriverManager().install())
print("1. Chron Browser Open")
#
user_id = 'greenpia1225'
user_pw = '@qwerasdf'


# 1. 네이버 이동
browser.get('http://naver.com')
print("2. Naver ")

# 2. 로그인 버튼 클릭
# elem = browser.find_element_by_class_name('link_login')
elem = browser.find_element(By.CLASS_NAME, 'link_login')
elem.click()
print("3. Login Button Click ")

# browser.find_element_by_id('id').send_keys('greenpia1225')
# browser.find_element_by_id('pw').send_keys('@qwerasdf')

# 3. id 복사 붙여넣기
elem_id = browser.find_element_by_id('id')
elem_id.click()
pyperclip.copy(user_id)
elem_id.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

# 4. pw 복사 붙여넣기
elem_pw = browser.find_element_by_id('pw')
elem_pw.click()
pyperclip.copy(user_pw)
elem_pw.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

# 5. 로그인 버튼 클릭
browser.find_element_by_id('log.login').click()

# 6. html 정보 출력
print(browser.page_source)

# 7. 브라우저 종료
# browser.close() # 현재 탭만 종료
# browser.quit() # 전체 브라우저 종료