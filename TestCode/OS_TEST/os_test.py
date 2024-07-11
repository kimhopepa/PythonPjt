import os

filename = 'saved_file.txt'
content = '저장할 내용입니다.'
current_directory = os.getcwd()
path = os.path.join(current_directory, filename)

print("path = " + path )
# 파일 저장
with open(path, 'w', encoding = 'utf-8') as file:
    file.write(content)

