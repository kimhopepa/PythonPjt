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
    is_multiline_comment = False

    func_pattern = re.compile(r'^\s*(\w+\s+\**)?(\w+)\s*\((.*)\)\s*\{?\s*$')

    global_var_pattern = re.compile(r'^\s*(\w+\s+\**)?(\w+)\s*=\s*[^;]*;')

    print("lines", lines)
    for line in lines:
        # 멀티라인 주석 처리
        if '/*' in line:
            is_multiline_comment = True
        if '*/' in line:
            is_multiline_comment = False
            continue
        if is_multiline_comment:
            continue

        # 라인 주석 처리
        line = re.sub(r'//.*', '', line).strip()
        if not line:
            continue

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
            # 전역 변수 추출
            match = global_var_pattern.match(line)
            if match:
                global_vars.append(match.group(2))

    return code_dict, global_vars

# Example usage
filename = r'D:\1_기술혁신팀\9_SVN_DATA\4_코드리뷰점검Tool\ELEC\1_Check_Unused_Code.ctl'
code_dict, global_vars = parse_c_code(filename)

print("Parsed Functions:", code_dict)
print("Global Variables:", global_vars)