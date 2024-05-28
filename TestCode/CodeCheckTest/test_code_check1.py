# import re
#
# def is_global_variable(line):
#     # 전역 변수의 패턴을 정의합니다.
#     variable_pattern = re.compile(r'^\s*(int|float|string|double|char|struct \w+|unsigned int|long|short|_Bool)(\s+\w+\s*(=\s*[^;]*)?\s*;| \*\w+\s*(=\s*[^;]*)?\s*;)')
#     return variable_pattern.match(line)
#
# def is_version_variable(line):
#     # 'version'이라는 변수 이름을 포함하는지 확인합니다.
#     version_pattern = re.compile(r'\bversion\b')
#     return version_pattern.search(line)
#
# def find_version_variable(filename):
#     with open(filename, 'r') as file:
#         lines = file.readlines()
#
#     in_function = False
#     version_found = False
#
#     for line in lines:
#         stripped_line = line.strip()
#         if stripped_line.startswith('{'):
#             in_function = True
#         elif stripped_line.startswith('}'):
#             in_function = False
#
#         if not in_function and is_global_variable(stripped_line) and is_version_variable(stripped_line):
#             version_found = True
#             break
#
#     return version_found
#
#
# def find_unused_variables(filename):
#     declared_variables = set()
#     used_variables = set()
#
#     with open(filename, 'r') as file:
#         for line in file:
#             # 변수 선언 찾기
#             declaration_match = re.search(r'\b(\w+)\b\s*;', line)
#             if declaration_match:
#                 variable_name = declaration_match.group(1)
#                 declared_variables.add(variable_name)
#             # 대입 연산자로 변수 선언 찾기
#             assignment_match = re.search(r'\b(\w+)\b\s*=', line)
#             if assignment_match:
#                 variable_name = assignment_match.group(1)
#                 declared_variables.add(variable_name)
#             # 변수 사용 찾기
#             used_matches = re.findall(r'\b(\w+)\b', line)
#             for used_variable in used_matches:
#                 used_variables.add(used_variable)
#
#     # 미사용 변수 찾기
#     print("사용 변수 ", type(used_variables), used_variable)
#     print("선언 변수 ", type(declared_variables), declared_variables)
#     unused_variables = declared_variables - used_variables
#
#     return unused_variables
#
# def find_unused_variables2(filename):
#     declared_variables = set()
#     used_variables = set()
#
#     with open(filename, 'r') as file:
#         for line in file:
#             # 변수 선언 및 초기화 찾기
#             declaration_match = re.search(r'\b(\w+)\b\s*=\s*\w+\s*;', line)
#             print("선언 변수 ", type(declaration_match), declaration_match)
#             if declaration_match:
#                 variable_name = declaration_match.group(1)
#                 declared_variables.add(variable_name)
#             # 변수 사용 찾기
#             used_matches = re.findall(r'\b(\w+)\b', line)
#             for used_variable in used_matches:
#                 used_variables.add(used_variable)
#
#     # 미사용 변수 찾기
#     print("사용 변수 ", type(used_variables), used_variable)
#     print("선언 변수 ", type(declaration_match), declared_variables)
#     unused_variables = declared_variables - used_variables
#
#     return unused_variables
#
# # 테스트할 C 파일의 경로를 입력하세요.
# c_file_path = '../test.c'
# if find_version_variable(c_file_path):
#     print("전역 변수 'version'이 선언되어 있습니다.")
# else:
#     print("전역 변수 'version'이 선언되어 있지 않습니다.")
#
# unused_variables = find_unused_variables2(c_file_path)
# if unused_variables:
#     print("미사용 변수: ", unused_variables)
# else:
#     print("미사용 변수가 없습니다.")



# import re
#
# def find_unused_variables(file_path):
#     with open(file_path, 'r') as file:
#         code = file.read()
#
#     # 정규 표현식으로 변수 선언 찾기
#     # 변수 선언을 잡아내기 위해 타입 뒤에 오는 변수 이름과 세미콜론을 찾습니다.
#     declaration_pattern = re.compile(r'\b(int|char|float|double|long|short)\s+(\w+)\s*(=\s*[^;]+)?\s*;')
#     # 코드에서 변수 이름을 모두 추출합니다.
#     usage_pattern = re.compile(r'\b\w+\b')
#
#     # 변수 선언 찾기
#     declarations = declaration_pattern.findall(code)
#     declared_variables = {decl[1] for decl in declarations}
#
#     # 변수 사용 찾기
#     usages = usage_pattern.findall(code)
#     used_variables = {usage for usage in usages if usage not in {'int', 'char', 'float', 'double', 'long', 'short'}}
#
#     # 선언된 변수 중 초기화된 변수는 사용된 것으로 간주합니다.
#     initialized_variables = {decl[1] for decl in declarations if decl[2]}
#
#     # 사용된 변수 집합에 초기화된 변수를 추가합니다.
#     used_variables.update(initialized_variables)
#
#     # 사용되지 않은 변수 찾기
#     unused_variables = declared_variables - used_variables
#
#     print("declared_variables", declared_variables, type(declared_variables))
#     print("used_variables", used_variables, unused_variables)
#
#
#     return unused_variables
#
# # 사용 예제
# c_file_path = '../test.c'
# unused_vars = find_unused_variables(c_file_path)
# print(f"사용되지 않은 변수: {unused_vars}")


import re


def extract_declared_variables(code):
    # 정규식을 사용하여 변수 선언 패턴 찾기
    pattern = r'\b(\w+)\s*(?:=\s*[^;]*)?;'
    matches = re.findall(pattern, code)
    return matches


def extract_rhs_variables(code):
    # 정규식을 사용하여 변수 선언과 할당문에서 우항에 사용된 변수 추출
    pattern = r'\b(\w+)\s*=\s*([^;]+);'
    matches = re.findall(pattern, code)

    rhs_variables = set()
    for match in matches:
        assigned_var, expression = match
        # 우항에서 변수만 추출
        variables = re.findall(r'\b\w+\b', expression)
        for var in variables:
            if not re.match(r'^\d+$', var) and not re.match(r'^[\'\"].*[\'\"]$', var):
                rhs_variables.add(var)
        # 할당되는 변수도 추가
        rhs_variables.add(assigned_var)

    return rhs_variables

def find_unused_declared_variables(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    print(code)
    declared_variables = extract_declared_variables(code)
    rhs_variables = extract_rhs_variables(code)

    # 선언되었지만 우항에서 사용되지 않은 변수 찾기
    unused_variables = [var for var in declared_variables if var not in rhs_variables]
    return unused_variables

c_file_path = '../test.c'
unused_vars = find_unused_declared_variables(c_file_path)
print(f"사용되지 않은 변수: {unused_vars}")