import re

def is_global_variable(line):
    # 전역 변수의 패턴을 정의합니다.
    variable_pattern = re.compile(r'^\s*(int|float|string|double|char|struct \w+|unsigned int|long|short|_Bool)(\s+\w+\s*(=\s*[^;]*)?\s*;| \*\w+\s*(=\s*[^;]*)?\s*;)')
    return variable_pattern.match(line)

def is_version_variable(line):
    # 'version'이라는 변수 이름을 포함하는지 확인합니다.
    version_pattern = re.compile(r'\bversion\b')
    return version_pattern.search(line)

def find_version_variable(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    in_function = False
    version_found = False

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('{'):
            in_function = True
        elif stripped_line.startswith('}'):
            in_function = False

        if not in_function and is_global_variable(stripped_line) and is_version_variable(stripped_line):
            version_found = True
            break

    return version_found


def find_unused_variables(filename):
    declared_variables = set()
    used_variables = set()

    with open(filename, 'r') as file:
        for line in file:
            # 변수 선언 찾기
            declaration_match = re.search(r'\b(\w+)\b\s*;', line)
            if declaration_match:
                variable_name = declaration_match.group(1)
                declared_variables.add(variable_name)
            # 대입 연산자로 변수 선언 찾기
            assignment_match = re.search(r'\b(\w+)\b\s*=', line)
            if assignment_match:
                variable_name = assignment_match.group(1)
                declared_variables.add(variable_name)
            # 변수 사용 찾기
            used_matches = re.findall(r'\b(\w+)\b', line)
            for used_variable in used_matches:
                used_variables.add(used_variable)

    # 미사용 변수 찾기
    print("사용 변수 ", type(used_variables), used_variable)
    print("선언 변수 ", type(declared_variables), declared_variables)
    unused_variables = declared_variables - used_variables

    return unused_variables

def find_unused_variables2(filename):
    declared_variables = set()
    used_variables = set()

    with open(filename, 'r') as file:
        for line in file:
            # 변수 선언 및 초기화 찾기
            declaration_match = re.search(r'\b(\w+)\b\s*=\s*\w+\s*;', line)
            print("선언 변수 ", type(declaration_match), declaration_match)
            if declaration_match:
                variable_name = declaration_match.group(1)
                declared_variables.add(variable_name)
            # 변수 사용 찾기
            used_matches = re.findall(r'\b(\w+)\b', line)
            for used_variable in used_matches:
                used_variables.add(used_variable)

    # 미사용 변수 찾기
    print("사용 변수 ", type(used_variables), used_variable)
    print("선언 변수 ", type(declaration_match), declared_variables)
    unused_variables = declared_variables - used_variables

    return unused_variables

# 테스트할 C 파일의 경로를 입력하세요.
c_file_path = '../test.c'
if find_version_variable(c_file_path):
    print("전역 변수 'version'이 선언되어 있습니다.")
else:
    print("전역 변수 'version'이 선언되어 있지 않습니다.")

unused_variables = find_unused_variables2(c_file_path)
if unused_variables:
    print("미사용 변수: ", unused_variables)
else:
    print("미사용 변수가 없습니다.")