import re
import lib_function_info as lib



# 멀티라인 텍스트 예제
text = '''
result=dpA(dd,tt,aa,cc);
dpB(dd,aa);
// dpC(some random text);
dpD(another_example);
result=dpGet("aa"
,a);
dpSet("aa",a);
'''


def extract_functions_with_lines(text):
    result = []
    lines = text.split('\n')
    # 정규식 패턴
    pattern = r'^(?:(?!//).)*(.*\bdp[A-Z][a-zA-Z0-9_]*)\('

    for line_number, line in enumerate(lines, start=1):
        match = re.search(pattern, line)
        if match:
            # result = result + [str(line_number) + match.group(1).strip()]
            result = result + [f"{line_number} | {match.group(1).strip()}"]
            # result.append((match.group(1).strip(), line_number))

    return result


def find_non_assignment_functions(text, start_line):
    pattern = r'(?<!\S=)\bdp[A-Z][a-zA-Z0-9_]*\([^)]*\)(?!\s*=\S)'
    result = []

    # 정규식 검색
    matches = re.finditer(pattern, text, re.MULTILINE | re.DOTALL)
    for match in matches:
        start, end = match.span()
        line_number = text[:start].count('\n')
        total_number = start_line + line_number
        result = result + [f"{total_number} | {match.group().strip()}"]
        # result.append((match.group().strip(), line_number))

    return result

if __name__ == '__main__':

    path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\Emergency_Blackout.ctl'
    text = lib.get_text_file(path)
    fnc_list = lib.get_function_list(text)

    for index, item in enumerate(fnc_list) :
        fnc_name = item[0]
        body_code = item[1]
        start_line = item[2]
        end_line = item[3]
        if fnc_name == "cx_check" :
            dp_function_list = find_non_assignment_functions(body_code, start_line)
            print('\n'.join(dp_function_list))