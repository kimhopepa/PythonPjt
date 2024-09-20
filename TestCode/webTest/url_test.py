import urllib.request
from urllib.error import URLError, HTTPError

def check_url(url):
    try:
        response = urllib.request.urlopen(url)
        print(f"URL {url}에 접속 성공!")
        # 여기서 추가적인 작업 수행 가능
        return True
    except HTTPError as e:
        print(f"HTTP 에러 발생: {e.code} - {e.reason}")
    except URLError as e:
        print(f"URL 에러 발생: {e.reason}")
    return False

# 사용 예시
# url = "https://www.example.com"
url = 'http://its.sit2home.com/'
if check_url(url):
    # 접속 성공 시 추가 작업 수행
    print("url ok")
else:
    # 접속 실패 시 처리
    print("url ng")