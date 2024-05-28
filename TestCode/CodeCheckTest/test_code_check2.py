import re

# def remove_string_literals(code):
#     # 문자열 리터럴 제거
#     code = re.sub(r'\".*?\"', '', code, flags=re.DOTALL)
#     code = re.sub(r'\'.*?\'', '', code, flags=re.DOTALL)
#     return code
def remove_comments(code):
    # 한 줄 주석 제거
    code = re.sub(r'//.*', '', code)
    # 여러 줄 주석 제거
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    return code

def extract_declared_variables(code):
    print("test1", code)
    # 문자열 리터럴 제거
    code = remove_comments(code)
    print("test2", code)

    # 정규식을 사용하여 변수 선언 패턴 찾기 (자료형 제외)
    pattern = r'\b(\w+)\s*(?:=\s*[^;]*)?;'
    matches = re.findall(pattern, code)
    return matches

def extract_rhs_variables(code):
    # 문자열 리터럴 제거
    code = remove_comments(code)

    # 정규식을 사용하여 변수 선언과 할당문, return문에서 우항에 사용된 변수 추출
    pattern = r'\b\w+\s*=\s*([^;]+);|return\s+([^;]+);'
    matches = re.findall(pattern, code)

    rhs_variables = set()
    for match in matches:
        for group in match:
            if group:
                # 우항에서 변수만 추출 (숫자, 문자열 제외)
                variables = re.findall(r'\b\w+\b', group)
                for var in variables:
                    if not re.match(r'^\d+$', var) and not re.match(r'^[\'\"].*[\'\"]$', var):
                        rhs_variables.add(var)

    # 함수 호출에서 인수를 추출
    function_call_pattern = r'\b\w+\s*\(([^)]+)\)'
    function_calls = re.findall(function_call_pattern, code)
    for call in function_calls:
        variables = re.findall(r'\b\w+\b', call)
        for var in variables:
            if not re.match(r'^\d+$', var) and not re.match(r'^[\'\"].*[\'\"]$', var):
                rhs_variables.add(var)

    return rhs_variables

def find_unused_declared_variables(code):
    declared_variables = extract_declared_variables(code)
    rhs_variables = extract_rhs_variables(code)

    # 선언되었지만 우항에서 사용되지 않은 변수 찾기
    unused_variables = [var for var in declared_variables if var not in rhs_variables]
    return unused_variables

# 예제 코드
code = """
// test
string version = "v1.0";
string release_version = "2024.05.23";
int function_sum(int a, int b)
{
    int i_sum = a + b;
    return i_sum;
}
int main() 
{
    int a = 5;
    int b = 10;
    int c ;
    int sum = a + b;
    printf("%d\\n", sum);
    printf("Hello, World!\\n");
    int fun_result = function_sum(12, 13);
    printf("Sum Result = %d\\n", fun_result);
    return sum;
}
void test()
{
    int b;
}
"""

unused_variables = find_unused_declared_variables(code)
print(unused_variables)