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

if __name__ == '__main__':
    path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\7_loop_dp_function.txt'
    text = lib.get_text_file(path)
    fnc_list = lib.get_function_body2(text)
    not_user_vars = []
    re_text = remove_line_comments(text)

    list_global_vars = find_global_variables5(re_text)     # list [['define_dp_name', 1], ['dp_name', 19], ['min_prio', 20], ['catch', 71], ['catch', 98], ['finnally', 102]]

    for var_name, line in list_global_vars:
        print(f"var name = {var_name}")
        result = find_variable_usage(re_text, str(var_name))

        if  result == True:
            print("find OK", var_name)
        else :
            print("find NG", var_name)
