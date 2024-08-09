import re
import lib_function_info as lib



if __name__ == '__main__':
    path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\5_DP_Exception.ctl'
    text = lib.get_text_file(path)
    re_text = lib.remove_line_comments(text)
    fnc_list = lib.get_function_body2(re_text)
    not_user_vars = []

    dp_function_pattern = r'(?<![!=\s])\s*dp[a-zA-Z][a-zA-Z0-9_]*\([^)]*\)\s*(?![!=\s])'

    for item in fnc_list :
        fnc_name = item[0]
        body_code = item[1]
        start_line = item[2]
        end_line = item[3]
        # print("function name = " + fnc_name )
        error_list = lib.get_patterns(body_code, dp_function_pattern, start_line)
        print(fnc_name, start_line, error_list)
