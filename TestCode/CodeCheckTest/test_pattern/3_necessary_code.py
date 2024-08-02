import re
import lib_function_info as lib

# 주석으로 공백으로 제거
def remove_line_comments(code):
    lines = code.splitlines()
    modified_lines = []
    for line in lines:
        # Remove comments starting with //
        if '/' in line:
            line = line.split('/')[0] + ' ' * len(line.split('//')[1])
        modified_lines.append(line)
    return '\n'.join(modified_lines)


# 입력받은 패턴의 캡쳐를 문자열로 반환
def get_pattern(text: str, pattern: str) -> str:
    match = re.search(pattern, text)

    if match:
        return match.group(1)
    else:
        return text


def get_varable_list(text:str, is_depth_check : bool = False ) -> list:

    # 텍스트를 줄 단위로 분리
    lines = text.splitlines()
    result = []

    brace_depth = 0
    for line_number, line in enumerate(lines):
        line = line.strip()

        # Update brace depth
        brace_depth += line.count('{')
        brace_depth -= line.count('}')

        # 설정한 depth보다 낮은 경우는 제외
        if brace_depth > 0 and is_depth_check == False:
            continue

        # 괄호가 포함된 줄은 제외
        if re.search(r"[()]", line):
            continue

        # 콤마(,)와 세미콜론(;)이 포함된 줄만 결과에 추가
        if ',' in line or ';' in line:

            line = line.replace(';', "")
            parts = line.split(',')

            for part in parts :
                part = part.strip()
                if '=' in part :
                    part = get_pattern(part, r'^\s*(.*?)\s*=')

                temp_var_list = part.split(' ')
                list_length = len(temp_var_list)
                if list_length > 0 :
                    part = temp_var_list[list_length-1]

                result = result + [[line_number + 1, part]]
            # result.append({
            #     'line_number': line_number,
            #     'line_content': part
            # })

    return result

def find_variable_usage(code : str, variable : str):
    # Use a word boundary to ensure exact match
    pattern = re.compile(r'\b' + re.escape(variable) + r'\b')
    matches = pattern.findall(code)
    return len(matches) > 1  # Tru

if __name__ == '__main__':
    path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\7_loop_dp_function.txt'
    text = lib.get_text_file(path)
    fnc_list = lib.get_function_body2(text)
    not_user_vars = []
    re_text = remove_line_comments(text)

    list_global_vars = get_varable_list(re_text, True)     # list [['define_dp_name', 1], ['dp_name', 19], ['min_prio', 20], ['catch', 71], ['catch', 98], ['finnally', 102]]

    # print

    for line_number, global_var_name in list_global_vars:
        # print(line_number, global_var_name)
    #     print(f"var name = {var_name}")
        result = find_variable_usage(re_text, str(global_var_name))
    #
        if  result == True:
            print("find OK",line_number, global_var_name)
        else :
            print("find NG",line_number, global_var_name)
