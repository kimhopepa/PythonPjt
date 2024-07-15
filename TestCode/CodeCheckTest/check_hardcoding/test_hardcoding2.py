import re
path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\2_function_check.txt'

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

pattern = r'(?<!/)\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{\n(.*?)\n\}'


def extract_function_names(text):
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
# # 예제 텍스트
# text = """
# void _Func1()
# {
# 	DebugTN("test func1()");
# }
#
# void func2(){
# 	DebugTN("test func2()");
# }
#
# void func_3(int a, int b){
# 	DebugTN("test func3()");
# }
# //func_4(){
# 	DebugTN("test func4()");
# }
# void func_5(int a, int b){
# 	DebugTN("test func5()");
# }
# """

# 함수 이름 추출
function_names = extract_function_names(text)

# 추출된 함수 이름 출력
print(function_names)