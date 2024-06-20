import re


def extract_variables_from_declaration(code: str) -> list:
    # 변수 타입을 정의하는 정규 표현식 부분을 수정하여, 영문자로 시작하고 영문자, 숫자, 언더스코어(_)를 포함할 수 있도록 함
    # 변수 타입과 변수 이름 사이에 최소 한 개 이상의 공백이 있어야 함
    pattern = re.compile(r'\s+([a-zA-Z_][a-zA-Z0-9_]*\s+)+((\w+)(\s*,\s*\w+)*)(\s*=\s*[^;]+)?;')

    matches = pattern.finditer(code)
    variables = []

    for match in matches:
        # 변수 이름들을 추출
        vars_group = match.group(2)
        # 쉼표로 분리된 변수 이름들을 리스트로 변환
        vars_list = [var.strip() for var in vars_group.split(',')]
        variables.extend(vars_list)

    return variables


# 예시 코드
code_example = """
 int a, b = 5;
 float c, d, e = 7.5;
 string f, g = "example";
 for( int i = 1 ; i <= 10; i++)
 {
    anytype t1 = dp_name;
 }
"""

# 함수 실행 및 결과 출력
variables = extract_variables_from_declaration(code_example)
print(variables)


