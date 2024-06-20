import re

def parse_c_code(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    code_dict = {}
    global_vars = []
    func_name = ""
    brace_count = 0
    func_body = []
    is_func = False

    func_pattern = re.compile(r'^\s*(\w+\s+\**)?(\w+)\s*\((.*)\)\s*\{?\s*$')

    for line in lines:
        # 함수 시작 파악
        if "{" in line:
            brace_count += 1
            if brace_count == 1:
                is_func = True
                match = func_pattern.match(line)
                if match:
                    func_name = match.group(2)
                    func_body.append(line.strip())
                continue
        elif "}" in line:
            brace_count -= 1
            if brace_count == 0 and is_func:
                # 함수 본문 종료
                code_dict[func_name] = {'body': func_body, 'level': brace_count}
                func_name = ""
                func_body = []
                is_func = False
            continue

        if is_func:
            func_body.append(line.strip())
        else:
            # 전역 변수 추출 부분은 제외
            pass

    return code_dict


def extract_functions_from_code(code : str):
    function_dict = {}

    # 함수 이름과 본문을 찾는 정규 표현식
    pattern = re.compile(r'(\w+)\(\)\s*\{\n(.*?)\n\}', re.DOTALL)

    matches = pattern.findall(code)
    print("matches type", type(matches), matches)
    for match in matches:
        print("매치 성공", type(match), match)
        function_name = match[0]
        function_body = match[1]
        function_dict[function_name] = function_body.strip()

    return function_dict

# Example usage
filename = r'D:\1_기술혁신팀\9_SVN_DATA\4_코드리뷰점검Tool\ELEC\1_Check_Unused_Code.ctl'
code_dict = parse_c_code(filename)

# Print the parsed code dictionary
for func, info in code_dict.items():
    print(f"Function Name: {func}")
    print("Function Body:")
    for line in info['body']:
        print(line)
    print("Level:", info['level'])
    print("-----")


