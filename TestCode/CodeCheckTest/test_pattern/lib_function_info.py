
import re
import chardet


path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\Emergency_Blackout.ctl'
# 파일의 인코딩을 자동으로 감지하여 읽기
def get_text_file(path :str) -> str:
    with open(path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        text = raw_data.decode(encoding)

    return text


# 함수 body 부분 추출 : body code, body start line, body end line
def get_body_info(text):
    try:
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
                    result = result + [[text[start_index + 1:i], start_ln, end_line]]
                    start_index = None
                    start_line = None

        return result
    except Exception as e:
        print("e")
        # Logger.error("CodeReviewCheck.extract_functions_from_code - Exception : " + str(e))

def get_function_name(text:str) -> str :
    # try :
    # pattern = r'(?<!/)\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
    pattern = r'(?<!/)\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\('

    matches = re.finditer(pattern, text)
    func_name = ""
    for match in matches :
        func_name = match.group(1)
        match_start_pos = match.start()

        # 주석의 경우는 제외
        l_pos = text.find('/')
        # print(f"Opening brace starts at line {start_line} and matching closing brace is at line {end_line}")
        # print(f"function {text}, {l_pos} , {match_start_pos}")
        if l_pos >= 0 and l_pos <  match_start_pos :
            func_name = ""
        else :
            break

    return str(func_name)
    # except Exception as e:
    #     print("e")
        # Logger.error("CodeReviewCheck.extract_functions_from_code - Exception : " + str(e))


def get_function_list(text : str) -> list :
    function_info = []
    code_line_number = 0

    #1. 먼저 body의 정보를 먼저 저장 : body_code, body_start_line, body_end_line
    body_info = get_body_info(text)
    # for index, item in enumerate(body_info) :
    #     print(index, item[1], item[2])

    #1. 텍스트 '\n' 분리하여 리스트에 저장
    # code_texts = text.split('\n')

    #2. function과 body를 분리하여 리스트에 저장 -> 2차원 배열 function 이름, body, start_line, end_line
    end_line = 0
    # for index, code_text in enumerate(code_texts) :
    code_line_number = 0
    for code_text in text.split('\n'):
        code_line_number = code_line_number + 1
        
        #3. 정규식으로 함수이름 조회
        if code_line_number >= end_line :
            func_name = get_function_name(code_text)

        if len(func_name) > 0 :
            body_item= body_info.pop(0)
            body_code = body_item[0]
            start_line = body_item[1]
            end_line = body_item[2]

            # 함수 이름, 함수 body, 함수 body 시작 라인, 함수 body 마지막 라인
            function_info = function_info + [[func_name, body_code, start_line, end_line]]
            func_name = ""
    return function_info

# print("start")
# function_info = get_function_list(text)
#
# for index, item in enumerate(function_info) :
#     print(index, item)


## Function, Body 가져오기 개선
def get_body_info2( text : str) -> list:
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
                result = result + [[text[start_index + 1:i], start_ln, end_line]]
                start_index = None
                start_line = None

    return result

def get_body_info3(text: str) -> list:
    """
    주어진 텍스트에서 중괄호 블록을 추출합니다. 주석을 제거하지 않고 주석에 의한 라인 수 변화를 처리합니다.
    """
    stack = []
    result = []
    line_number = 1
    start_index = None
    start_line = None
    i = 0

    while i < len(text):
        char = text[i]

        # 주석이 시작되면 주석 처리
        if text[i:i+2] == '//':
            while i < len(text) and char != '\n':
                i += 1
                if i < len(text):
                    char = text[i]
            line_number += 1
        elif text[i:i+2] == '/*':
            while i < len(text) and text[i:i+2] != '*/':
                i += 1
                if i < len(text):
                    char = text[i]
            i += 1  # Skip '*/'
        else:
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
                    result.append([text[start_index + 1:i], start_ln, end_line])
                    start_index = None
                    start_line = None

        i += 1

    return result

def get_function_name2( text: str) -> str:
    # pattern = r'(?<!/)\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
    pattern = r'(?<!/)\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\('

    matches = re.finditer(pattern, text)
    func_name = ""
    for match in matches:
        func_name = match.group(1)
        match_start_pos = match.start()

        # 주석의 경우는 제외
        l_pos = text.find('/')
        if l_pos >= 0 and l_pos < match_start_pos:
            func_name = ""
        else:
            break

    return str(func_name)

def get_function_body2(text : str) -> list:
    function_info = []
    code_line_number = 0
    text = remove_line_comments(text)
    # 1. 먼저 body의 정보를 먼저 저장 : body_code, body_start_line, body_end_line
    body_info = get_body_info3(text)
    # for index, item in enumerate(body_info):
    #     print(index, item[1], item[2])

    # 2. function과 body를 분리하여 리스트에 저장 -> 2차원 배열 function 이름, body, start_line, end_line
    end_line = 0
    # for index, code_text in enumerate(code_texts) :
    code_line_number = 0
    for code_text in text.split('\n'):
        code_line_number = code_line_number + 1

        # 3. 정규식으로 함수이름 조회
        if code_line_number >= end_line:
            func_name = get_function_name2(code_text)

        if len(func_name) > 0:
            body_item = body_info.pop(0)
            body_code = body_item[0]
            start_line = body_item[1]
            end_line = body_item[2]

            # 함수 이름, 함수 body, 함수 body 시작 라인, 함수 body 마지막 라인
            function_info = function_info + [[func_name, body_code, start_line, end_line]]
            func_name = ""

    return function_info

def is_check_pattern(pattern : str, check_test : str) -> bool :
    compile_pattern = re.compile(pattern)
    if compile_pattern.search(check_test) :
        return True
    else :
        return False


# 입력받은 패턴의 캡쳐를 문자열로 반환
def get_pattern(text: str, pattern: str) -> str:
    match = re.search(pattern, text) # 첫번째 매칭만 찾을 때 search 사용

    if match:
        return match.group(1)
    else:
        return text

def get_patterns(text: str, pattern: str, fnc_pos_line:int) -> list:
    result_list = []
    matches = re.finditer(pattern, text)    # 여러 매칭만 찾을 때 finditer 사용
    for match in matches :
        start_pos = match.start()
        match_line_number = match.group(0).count('\n')
        line_number = text.count('\n',0, start_pos) + fnc_pos_line + match_line_number
        result_list = result_list + [[match.group(0).strip(),line_number]]

    return result_list

# 주석으로 공백으로 제거
def remove_line_comments(code : str) -> str:
    lines = code.splitlines()
    modified_lines = []
    for line in lines:
        # Remove comments starting with /
        if '/' in line:
            line = line.split('/')[0] + ' ' * len(line.split('//')[1])
        modified_lines.append(line)
    return '\n'.join(modified_lines)