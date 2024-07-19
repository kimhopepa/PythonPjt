
import re
import chardet
path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\Emergency_Blackout.ctl'
#path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\2_function_check.txt'

# 파일의 인코딩을 자동으로 감지하여 읽기
with open(path, 'rb') as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

    text = raw_data.decode(encoding)


# pattern = r'(?<!/)\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{\n(.*?)\n\}'
# 예제 코드
code = """
function1() {
    // function1 body
}

function2() {
    function1();
    // function2 body
}

function3() {
    // function3 body
    function2();
}

function4() {
    // function4 body
}
"""

def extract_function_names(text):
    # 정규식을 사용하여 함수 이름 추출
    pattern = r'(?<!/)\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{\n(.*?)\n\}'
    matches = re.finditer(pattern, text, re.DOTALL)
    for match in matches:
        function_name = match.group(1)
        function_body = match.group(2)
        print(f"Function Name:" + function_name)
        print(f"Function body: " + function_body)
def extract_function_names2(text):
    # 함수 시그니처와 여는 중괄호를 찾기 위한 정규식
    pattern = r'(?<!/)\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{'
    matches = re.finditer(pattern, text, re.DOTALL)

    for match in matches:
        function_name = match.group(1)
        start = match.end()  # 여는 중괄호 위치

        # 중첩 중괄호 처리
        depth = 1
        end = start
        while depth > 0 and end < len(text):
            if text[end] == '{':
                depth += 1
            elif text[end] == '}':
                depth -= 1
            end += 1

        # 함수 본문 추출
        function_body = text[start:end - 1].strip()

        print(f"Function Name: {function_name}")
        print(f"Function Body:\n{function_body}\n")


def calculate_line_number(text, index):
    return text.count('\n', 0, index) + 1

def extract_functions3(text):
    # 함수 시그니처와 여는 중괄호를 찾기 위한 정규식
    # \b = 단어경계,([a-zA-Z_][a-zA-Z0-9_]*)=함수이름, \s* = 0개이상 단어
    # \( = 소괄호 , [^)]* = 닫는 괄호를 빼고 매칭
    # pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{'
    # pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(*\)\s*\{'
    # pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(*\)\s*\{'
    pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\)\s*\{'
    # pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(*\)\s*\{'
    # pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(\s*\{'
    # pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^{}]*\s*\{'
    matches = re.finditer(pattern, text, re.DOTALL)

    functions = []

    end_line = 0
    for match in matches:
        function_name = match.group(1)
        start = match.end() - 1  # 여는 중괄호 위치

        start_line = calculate_line_number(text, start)
        if (start_line > end_line):

            # 중첩 중괄호 처리
            depth = 1
            end = start + 1
            while depth > 0 and end < len(text):
                if text[end] == '{':
                    depth += 1
                elif text[end] == '}':
                    depth -= 1
                end += 1

            end_line = calculate_line_number(text, end)

            # 함수 본문 추출
            function_body = text[start:end].strip()
            print(f"Function Name: {function_name} + {start_line} ~ {end_line}")
            # print(f"Function Body:\n{function_body}\n")

    return functions
# print(text)
# extract_function_names(text)
# extract_functions3(text)

def check_function_list(text : str) -> list :
    code_line_number = 0
    for code_text in text.split('\n'):
        code_line_number = code_line_number + 1
        print(code_text, code_line_number)


check_function_list(text)