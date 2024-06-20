import re


def check_variable_usage(code, variables):
    all_variables = set(variables)
    used_variables = set()
    #
    # print(code)
    # print(variables)

    for var in variables:
        # 변수가 할당된 경우를 먼저 확인
        if re.search(rf'\b{var}\b\s*=', code):
            continue

        # 변수가 사용된 경우를 확인
        if re.search(rf'\b{var}\b', code):
            used_variables.add(var)

    unused_variables = all_variables - used_variables
    print(all_variables, type(all_variables))
    print(used_variables, type(used_variables))
    # print(all_variables, used_variables, unused_variables)
    return list(unused_variables)


# 예제 코드
code_example = """
int
a = 5
b = a + 1
c = 10
d = b * c
"""
variables_list = ['a', 'b', 'c', 'd', 'e']

unused_vars = check_variable_usage(code_example, variables_list)
# print("Unused Variables:", unused_vars)