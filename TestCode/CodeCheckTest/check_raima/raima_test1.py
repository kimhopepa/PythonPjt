import re


def find_all_variable_values(code):
    variables = {}
    # 모든 변수 할당을 찾기 위한 정규 표현식
    pattern = re.compile(r'\b(\w+)\s*=\s*([^;]+);')
    matches = pattern.findall(code)

    for var_name, value_expression in matches:
        value_expression = value_expression.strip()
        if value_expression.startswith('"') and value_expression.endswith('"'):
            # 문자열 리터럴인 경우
            variables[var_name] = value_expression.strip('"')
        elif value_expression.isdigit():
            # 숫자인 경우
            variables[var_name] = value_expression
        else:
            # 변수나 결합된 표현식인 경우
            value_parts = value_expression.split('+')
            final_value = ''
            for part in value_parts:
                part = part.strip().strip('"')
                if part in variables:
                    final_value += variables[part]
                else:
                    final_value += part
            variables[var_name] = final_value

    return variables


# 예제 C 스타일 코드
code = """
string set_test;
set_test = "abcd";
void main()
{
   string check_var = set_test + "1234" + "ttt";
   int check = 19;
}
"""

# 모든 변수 값 찾기
variables = find_all_variable_values(code)

# 변수 값 출력
for var_name, value in variables.items():
    print(f'{var_name}의 값은 "{value}"입니다.')
