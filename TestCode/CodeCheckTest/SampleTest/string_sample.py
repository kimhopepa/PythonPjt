import re
import chardet

def extract_braces_content(text):
    stack = []
    result = []
    line_number = 1
    start_index = None
    start_line = None

    for i, char in enumerate(text):
        if char == '\n':
            line_number += 1
        elif char == '{':
            if start_index is None:
                start_index = i
                start_line = line_number
            stack.append((i, line_number))
        elif char == '}' and stack:
            start_pos, start_ln = stack.pop()
            if not stack:
                end_line = line_number
                result.append((text[start_index + 1:i], start_ln, end_line))
                start_index = None
                start_line = None

    return result


path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\Emergency_Blackout.ctl'
# 파일의 인코딩을 자동으로 감지하여 읽기
with open(path, 'rb') as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

    text = raw_data.decode(encoding)

line_index = 0
while line_index < len
# 중괄호 안의 내용 추출
#
# contents = extract_braces_content(text)
#
# print(len(contents))
# # 추출된 내용 출력
# for index, content in enumerate(contents):
#     print(index, content[1],content[2])
#
# list_str = [["A", "B"], ["C", "D"]]
#
# list_str = list_str + [["FFF", 11]]
# list_str = list_str + [["FFF2222", 222]]
#
#
# print(list_str)