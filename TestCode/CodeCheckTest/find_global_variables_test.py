import re

def find_global_variables(code:str) -> list:
    # 전역 변수를 찾기 위한 정규식
    # 이 정규식은 타입, 공백, 변수 이름(들), 세미콜론으로 구성된 패턴을 찾습니다.
    # 변수 이름은 쉼표로 구분될 수 있습니다.
    pattern = re.compile(r'\b(\w+\s+)((\w+)(\s*,\s*\w+)*)\s*;')

    # 찾은 전역 변수를 저장할 리스트
    global_variables = []

    # 코드의 각 라인에 대해 반복
    for line in code.split('\n'):
        match = pattern.match(line.strip())
        if match:
            # 변수 이름들을 추출하고 쉼표로 구분된 이름을 개별적으로 처리
            variables = match.group(2).split(',')
            # 공백 제거 후 리스트에 추가
            global_variables.extend([var.strip() for var in variables])

    return global_variables


# 예제 코드
code = '''
int a, b, c;
anytype result_list1, result_list2;
'''

# 전역 변수 찾기
global_vars = find_global_variables(code)

print("Found global variables:", global_vars)