import re

# def remove_comments(code):
#     # 한 줄 주석 제거  '.*' -> 모든 문자를 체크
#     code = re.sub(r'//.*', '', code)
#
#     # 여러 줄 주석 제거
#     code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
#
#     print('remove_comments', code)
#     return code

def extract_declared_variables(code):
    # 주석 제거
    code = remove_comments(code)

    # 변수 선언 패턴 찾기
    pattern = r'\b(\w+)\s*(?:=\s*[^;]*)?;'
    matches = re.findall(pattern, code)
    return matches


def extract_declared_variables2(code):
    # 주석 제거
    code = remove_comments(code)

    # 변수 선언 패턴 찾기
    pattern = r'\b(?:\w+\s+)(\w+(?:\s*=\s*[^,;]*)?(?:\s*,\s*\w+(?:\s*=\s*[^,;]*)?)*)\s*;'
    matches = re.findall(pattern, code)

    # 각각의 변수 분리
    variables = []
    for match in matches:
        variables.extend([var.strip().split('=')[0].strip() for var in match.split(',')])

    return variables

def extract_rhs_variables(code):
    # 주석 제거
    code = remove_comments(code)

    # 변수 선언과 할당문, return문에서 우항에 사용된 변수 추출
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

def extract_function_names(code):
    # 함수 선언 패턴 찾기
    pattern = r'\b\w+\s+\w+\s*\([^)]*\)\s*\{'
    matches = re.findall(pattern, code)

    function_names = set()
    for match in matches:
        function_name = re.findall(r'\b\w+\s+(\w+)\s*\(', match)
        if function_name:
            function_names.add(function_name[0])

    return function_names

def extract_called_functions(code):
    # 함수 호출 패턴 찾기
    pattern = r'\b(\w+)\s*\([^)]*\)\s*;'
    matches = re.findall(pattern, code)
    return set(matches)

def find_unused_declared_variables(code):
    declared_variables = extract_declared_variables(code)
    rhs_variables = extract_rhs_variables(code)

    # 선언되었지만 우항에서 사용되지 않은 변수 찾기
    unused_variables = [var for var in declared_variables if var not in rhs_variables]
    return unused_variables

def find_unused_functions(code):
    declared_functions = extract_function_names(code)
    called_functions = extract_called_functions(code)

    # 'main' 함수는 제외
    declared_functions.discard('main')

    # 선언되었지만 호출되지 않은 함수 찾기
    unused_functions = declared_functions - called_functions
    return unused_functions

# 예제 코드
code = """
// test
/*
    주석작성한 부분입니다.
    int teest1111111111 = 100000l;
*/
//string version = "v1.0";
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
    int c,k,e, jj;
    int sum = a + b;
    int a, b, c;
    int d = 10;
    dyn_anytype list1, list2; 
    printf("%d\\n", sum);
    printf("Hello, World!\\n");
    function_sum(c); 
    //int fun_result = function_sum(c);
    printf("Sum Result = %d\\n", fun_result);
    return sum;
}
void test()
{
    int b;
}
"""


def extract_declared_variables2(code):
    # 주석 제거
    code = remove_comments(code)

    # 변수 선언 패턴 찾기
    pattern = r'\b(?:\w+\s+)(\w+(?:\s*=\s*[^,;]*)?(?:\s*,\s*\w+(?:\s*=\s*[^,;]*)?)*)\s*;'
    matches = re.findall(pattern, code)

    # 각각의 변수 분리
    variables = []
    for match in matches:
        variables.extend([var.strip().split('=')[0].strip() for var in match.split(',')])

    return variables

def remove_comments(code):
    # 한 줄 주석 제거
    code = re.sub(r'//.*', '', code)

    # 여러 줄 주석 제거
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

    # 여러 줄 주석 내의 모든 행 삭제
    code = re.sub(r'(/\*.*?\*/)', lambda x: '\n' * x.group(0).count('\n'), code, flags=re.DOTALL)

    # print('remove_comments', code)
    return code

remove_comments(code)
# unused_variables = find_unused_declared_variables(code)
# unused_functions = find_unused_functions(code)
#
# print("Unused Variables:", unused_variables)
# print("Unused Functions:", unused_functions)

print(extract_declared_variables2(code))





def split_code_by_functions(code):
    functions = []
    current_function_lines = []

    for line in code.split('\n'):
        # 여는 중괄호를 찾으면 함수 코드 시작
        if '{' in line:
            current_function_lines.append(line)
        # 닫는 중괄호를 찾으면 함수 코드 종료
        elif '}' in line:
            current_function_lines.append(line)
            functions.append('\n'.join(current_function_lines))
            current_function_lines = []
        # 함수 코드가 아니라면 현재 함수에 추가
        elif current_function_lines:
            current_function_lines.append(line)
    print(functions, current_function_lines)
    return functions



def read_file_and_return_text(file_path):
    try:
        with open(file_path, 'r') as file:
            file_text = file.read()
        return file_text
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None





def extract_functions(file_content):
    functions = {}
    current_function_name = None
    current_function_body = []

    for line in file_content.split('\n'):
        # 소괄호() 다음에 중괄호{}가 있으면 함수로 간주
        if '(' in line and ')' in line :
            # 함수 이름 추출
            function_name = line.split('(')[0].strip()
        elif '{' in line:
            # 함수 본체 저장 시작
            current_function_name = function_name
            current_function_body = []
        # 함수 본체를 저장
        elif current_function_name and '}' not in line:
            current_function_body.append(line)
        # 함수 본체가 끝나는 지점을 찾음
        elif current_function_name and '}' in line:
            functions[current_function_name] = '\n'.join(current_function_body)
            current_function_name = None

    return functions

# 파일 경로 입력
file_path = r'D:\1_기술혁신팀\9_SVN_DATA\4_코드리뷰점검Tool\ELEC\1_Check_Unused_Code.ctl'

# 파일 읽어서 텍스트 반환

#1. 파일 읽기
text = read_file_and_return_text(file_path)

#2. 주석 제거
text = remove_comments(text)

#3.
functions = extract_functions(text)


# 결과 출력
for function_name, function_body in functions.items():
    print(f"Function Name: {function_name}")
    print("Function Body:")
    print(function_body)
    print()