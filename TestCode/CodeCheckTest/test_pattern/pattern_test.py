import re
import chardet
# path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\Emergency_Blackout.ctl'
path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\1_testcode.txt'
# 파일을 읽어서 텍스트를 변수에 저장
# text = ""
# with open(path, 'r',  encoding='utf-8') as file:
#     text = file.read()
# 파일의 인코딩을 자동으로 감지하여 읽기
with open(path, 'rb') as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

    text = raw_data.decode(encoding)

print(text)
print(encoding)
# pattern = r'\b(?:[a-zA-Z_][a-zA-Z0-9_]*)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{\s*([\s\S]*?)\s*\}'
# pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{'
pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^()]*)\)\s*\{\n(.*?)\n\}'
# pattern = r'(?<!/)\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{\n(.*?)\n\}'
# pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{\n(.*?)\n\}'
#
# matches = re.findall(pattern, text)
matches = re.finditer(pattern, text, re.DOTALL)
print(matches, type(matches))
#
for match in matches:
    print(f"Function Name: {match[0]}")
    print(f"Function Name: {match[1]}")
    # print(f"Function Body:\n{match[1]}")