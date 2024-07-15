import re
path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\1_testcode.txt'

print(path)

# 파일을 읽어서 텍스트를 변수에 저장
with open(path, 'r',  encoding='utf-8') as file:
    text = file.read()


pattern = r'^/.*'
# 텍스트를 한 줄씩 출력
for line in text.splitlines():
    if re.match(pattern, line) :
        print("/문자 포함 OK", line)
    else :
        print("/문자 포함 NG", line)