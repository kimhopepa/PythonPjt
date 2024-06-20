def is_variable_used(c_code, variable_name):
    # 변수 사용 검사를 위해 C 코드를 ';'를 기준으로 문장별로 분리
    statements = c_code.split(';')

    for statement in statements:
        # 공백 제거
        statement = statement.strip()
        if variable_name in statement:
            # 대입 연산자 왼쪽에만 위치한 경우를 제외
            left_side = statement.split('=')[0].strip()
            if variable_name in left_side.split():
                continue  # 대입의 왼쪽에만 있으면 사용으로 간주하지 않음
            return True  # 그 외의 경우 사용으로 간주
    return False  # 모든 문장에서 사용되지 않음


# 예시 사용법
c_code_example = """
int a = 5;
b = a + 1;
c = a;
if(b==1)
    break;
"""
variable_name = "a"
print(is_variable_used(c_code_example, "a"))  # True를 반환해야 함
print(is_variable_used(c_code_example, "b"))  # True
print(is_variable_used(c_code_example, "c"))  # false