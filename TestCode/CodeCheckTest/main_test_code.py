import re



def save_dict_to_file(file_path, dictionary):
    try:
        with open(file_path, 'w') as file:
            for key, value in dictionary.items():
                file.write(f'Function Name: {key}\n')
                file.write('Function Body:\n')
                file.write(value)
                file.write('\n\n')
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            file_text = file.read()
            # file_text = file.readlines()
        return file_text
    except Exception as e :
        print(f"An error occurred: {e}")

def extract_functions_from_code(code : str) -> dict:
    function_dict = {}

    # 함수 이름과 본문을 찾는 정규 표현식
    pattern = re.compile(r'(\w+)\(\)\s*\{\n(.*?)\n\}', re.DOTALL)

    matches = pattern.findall(code)
    # print("matches type", type(matches), matches)
    for match in matches:
        # print("매치 성공", type(match), match)
        function_name = match[0]
        function_body = match[1]
        function_dict[function_name] = function_body.strip()

    return function_dict

def save_dict_to_file(file_path, dictionary):
    try:
        with open(file_path, 'w') as file:
            for key, value in dictionary.items():
                file.write(f'Function Name: {key}\n')
                file.write('Function Body:\n')
                file.write(value)
                file.write('\n\n')
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

def remove_comments(code: str) -> str:
    # 라인 주석 제거
    code = re.sub(r'//.*', '', code)
    # 블록 주석 제거
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    return code

# def remove_comments(code: str) -> str:
#     # 라인 주석 제거
#     code = re.sub(r'//.*', '', code)
#     # 블록 주석 제거
#     code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
#     return code

# 괄호안의 코드 모두 삭제
def extract_global_scope_code(code: str) -> str:
    # 괄호 안의 내용(지역 영역)을 제외하고 전역 영역의 코드만을 추출
    nested_braces_pattern = re.compile(r'{[^{}]*}')
    while re.search(nested_braces_pattern, code):
        code = re.sub(nested_braces_pattern, '', code)
    return code


def extract_global_variables(code: str) -> list:
    # 중괄호 내용(함수 정의 등)을 제외하고 전역 영역의 코드만 추출
    code = remove_comments(code)

    # 괄호 안의 내용을 제외하고 전역 연역의 코드만을 추출
    code_without_braces = extract_global_scope_code(code)
    # code_without_braces = re.sub(r'{[^{}]*}', '', code_without_braces)



    # 라인 별로 처리하여 주석 제거
    lines = code_without_braces.split('\n')
    lines_without_comments = [re.sub(r'//.*', '', line).strip() for line in lines if '//' in line or line.strip() != '']
    # print("lines_without_comments", lines_without_comments)

    # 전역 변수를 찾기 위한 정규식 패턴: 세미콜론으로 끝나는 모든 선언 찾기
    pattern = re.compile(r'\b(\w+)\s*([^;]+);')

    global_variables = []

    for line in lines_without_comments:
        matches = pattern.finditer(line)
        for match in matches:
            # 변수 이름만 추출
            variables_part = match.group(2)
            # 쉼표로 구분된 여러 변수 처리
            variables = [var.split('=')[0].strip() for var in variables_part.split(',')]
            global_variables.extend(variables)

    return global_variables





def extract_global_variables2(code: str) -> list:
    # 주석 제거
    code_without_comments = remove_comments(code)

    # 중괄호 내용(함수 정의 등)을 제외하고 전역 영역의 코드만 추출
    code_without_braces = re.sub(r'{[^{}]*}', '', code_without_comments)

    # 전역 변수를 찾기 위한 정규식 패턴: 세미콜론으로 끝나는 모든 선언 찾기
    pattern = re.compile(r'\b(\w+)\s*([^;]+);')

    global_variables = []

    matches = pattern.finditer(code_without_braces)
    for match in matches:
        # 변수 이름만 추출
        variables_part = match.group(2)
        # 쉼표로 구분된 여러 변수 처리
        variables = [var.split('=')[0].strip() for var in variables_part.split(',')]
        global_variables.extend(variables)

    return global_variables


# def body_unused_variable(code :str) -> bool :
#     try:
#         # 라인 별로 처리하여 주석 제거
#         lines = code.split('\n')
#         lines_without_comments = [re.sub(r'//.*', '', line).strip() for line in lines if
#                                   '//' in line or line.strip() != '']
#     except Exception as e:
def global_used_check(global_vars : list, code_dict : dict ) -> dict:
    try :
        unused_var_dict = {}
        for fun_name, body_code in code_dict.items():
            print("fun_name = ", fun_name)

            #1.1 함수 지역 변수 체크
            body_vars = extract_variables_from_declaration(body_code)

            #1.2 지역 변수 미사용 체크
            unused_vars = check_variable_usage(body_code, body_vars)
            if len(unused_vars) > 0 :
                print("Local unused_vars", unused_vars)

            #2. 전역 변수 함수내 미사용 체크
            unused_vars = check_variable_usage(body_code, global_vars)
            if len(unused_vars) > 0:
                print("Global unused_vars", unused_vars)

        return unused_var_dict
    except Exception as e:
        print("exception : ", e)

# 코드에서 변수 이름 찾기
def extract_variables_from_declaration(code: str) -> list:
    # 줄의 시작에 있는 공백을 포함하여 변수 타입과 변수 이름들을 매칭할 수 있도록 정규 표현식 수정
    pattern = re.compile(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*\s+)+((\w+)(\s*,\s*\w+)*)(\s*=\s*[^;]+)?;$', re.MULTILINE)

    matches = pattern.finditer(code)
    variables = []

    for match in matches:
        vars_group = match.group(2)  # 변수 이름들을 추출
        vars_list = [var.strip() for var in vars_group.split(',')]  # 쉼표로 분리된 변수 이름들을 리스트로 변환
        variables.extend(vars_list)

    return variables


def check_variable_usage(code : str, variables : list) -> list:
    all_variables = set(variables)
    used_variables = set()

    for var in variables:
        # 변수가 할당된 경우를 먼저 확인
        # if re.search(rf'\b{var}\b\s*=', code):
        #     continue

        # 변수가 괄호 안에 사용된 경우
        if re.search(rf'\(\s*{var}\s*\)|\(\s*.*,\s*{var}\s*[,\)]', code):
            used_variables.add(var)

        # 변수가 대입 연산자 우항에 사용된 경우
        if re.search(rf'=\s*.*\b{var}\b', code):
            used_variables.add(var)

        # # 변수가 세미콜론 좌측에 사용된 경우
        # if re.search(rf'\b{var}\b.*;', code):
        #     used_variables.add(var)

    unused_variables = all_variables - used_variables
    # print(all_variables, used_variables, unused_variables)
    return list(unused_variables)

if __name__ == '__main__':
    try:
        file_path = r'D:\1_기술혁신팀\9_SVN_DATA\4_코드리뷰점검Tool\ELEC\1_Check_Unused_Code.ctl'

        # 1. 파일 읽기
        file_code = read_file(file_path)

        # 2. 함수, Body Dictionary 저장
        code_dict = extract_functions_from_code(file_code)
        save_dict_to_file("result_text_dict.txt", code_dict)
        # for fun_name, body_code in code_dict.items() :
        #     print("key = " + fun_name)
        #     print("body = " + body_code)

        # 3. 전역 변수 리스트에 저장
        global_vars = extract_global_variables(file_code)

        print("global_vars", global_vars)

        # 3-1. 전역 변수 사용 체크
        g_var_dict = global_used_check(global_vars, code_dict)

        print("global_used_check - end")

        # 3. 지역 변수 미사용 체크

        # 4. 전역 변수 미사용 체크



        save_dict_to_file("result_text_dict.txt", code_dict)
        # print(type(file_text))
        # exit()
        # print("file_text \n" + str(file_text), )

        # 2. 주석 삭제
        # code_dict = parse_code(file_text)
        # for func, info in code_dict.items():
        #     print(f"Function Name: {func}")
        #     print("Function Body:")
        #     for line in info['body']:
        #         print(line)
        #     print("Level:", info['level'])
        #     print("-----")

    except Exception as e:
        print("exception : ", e)