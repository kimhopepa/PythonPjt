import re
path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\3_hardcoding.txt'

print(path)

# 파일을 읽어서 텍스트를 변수에 저장
with open(path, 'r',  encoding='utf-8') as file:
    text = file.read()
# C 언어 함수 정의 패턴 정규식
# pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{'
# pattern = re.compile(r'\b(\w+)\(\)\s*\{\n(.*?)\n\}', re.DOTALL)
# pattern = re.compile(r'(\w+)\(\)\s*\{\n(.*?)\n\}', re.DOTALL)

# pattern = re.compile(r'\b(\w+)\(\)\s*\{\n(.*?)\n\}', re.DOTALL)
# pattern = r'(?<!/)\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{\n(.*?)\n\}'


# def extract_function_names(text):
#     # 정규식을 사용하여 함수 이름 추출
#     matches = re.findall(pattern, text)
#     return matches




def extract_function_names(text):
    pattern = r'(?<!/)\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{\n(.*?)\n\}'
    matches = re.finditer(pattern, text, re.DOTALL)
    results = []
    for match in matches:
        function_name = match.group(1)
        function_body = match.group(2)
        start_pos = match.start()
        end_pos = match.end()
        start_line = calculate_line_number(text, start_pos)
        end_line = calculate_line_number(text, end_pos)
        results.append((function_name, function_body, start_line, end_line))
    return results

def calculate_line_number(text, index):
    return text.count('\n', 0, index) + 1

def print_for(input_list) :
    for item in input_list :
        # print("item 길이 = " + str(len(item)))
        # print("함수 이름 : " + item[0] + "body 내용 : " + item[1])
        body_code = item[1]
        function_line = item[2]
        pattern_hardcoding = re.compile(r'^\s*[^/]*=\s*[^;]*(\d+|".*?")\s*[^;]*;\s*(//.*)?$')
        pattern_hardcoding2 = re.compile(r'\b(?!Debug|Log)\w+\s*\([^)]*(\d+|".*?")[^)]*\)')
        function_last_line = item[3]
        print("function = " + item[0], "line = " + str(function_line))
        for line in body_code.split('\n'):
            line_count = function_line + 1
            if pattern_hardcoding.search(line) or pattern_hardcoding2.search(line) :

                print("Pattern matches -> OK" + line + ", " + str(line_count))
            else:
                print("Pattern matches -> NG" + line)
        # print("Start line : " + str(item[2]))
        # print("End Line: " + str(item[3]))
# 함수 이름 추출
function_names = extract_function_names(text)
# 출력 함수
print_for(function_names)
# 추출된 함수 이름 출력
# print(function_names)