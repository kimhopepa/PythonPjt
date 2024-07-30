import requests

url = 'http://example.com/data'  # 데이터를 가져올 웹 페이지의 URL을 넣어주세요

url = 'http://its.sithome.com/projects/tech-inno/wiki/2024-07_4%EC%A3%BC%EC%B0%A8'
# GET 요청을 보내서 데이터를 가져오기
response = requests.get(url)

# 응답 코드가 성공(200)일 때 데이터를 출력합니다.
if response.status_code == 200:
    data = response.text
    print(data)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
