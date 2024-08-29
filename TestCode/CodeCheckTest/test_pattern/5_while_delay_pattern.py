import re
import lib_function_info as lib


def find_closing_brace_index(text, open_brace_index):
    """
    중첩된 중괄호를 처리하여 닫는 중괄호의 인덱스를 찾습니다.
    """
    stack = 0
    for index, char in enumerate(text[open_brace_index:], start=open_brace_index):
        if char == '{':
            stack += 1
        elif char == '}':
            stack -= 1
            if stack == 0:
                return index
    return -1

def get_while_code(body_code : str) -> list:
    pattern = r'while\s*\([^)]*\)\s*{'
    match = re.search(pattern, body_code, re.DOTALL)
    while_block_code = ""

    if match :
        while_code_start_pos = match.end() - 1
        end_index = find_closing_brace_index(text, while_code_start_pos)
        if end_index == -1 :
            while_block_code =  ""
        else :
            while_block_code = body_code[while_code_start_pos + 1 : end_index]

    else :
        while_block_code = ""

    return while_block_code

def is_check_while_delay(body_code : str) -> bool :
    check_result = False
    pattern = re.compile(r'([^\s].*?)\s*(?=\{)')
    matches = list(pattern.finditer(body_code))

    for match in matches:
        block_name = match.group(1)
        block_start_pos = match.end()
        print("is_check_while_delay - match :", match.group(1))


    return check_result
if __name__ == '__main__':
    path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\7_loop_dp_function.ctl'
    text = lib.get_text_file(path)
    fnc_list = lib.get_function_body2(text)
    for index, item in enumerate(fnc_list) :
        fnc_name = item[0]
        body_code = item[1]
        start_line = item[2]
        end_line = item[3]
        while_code = get_while_code(body_code)

        if len(while_code) > 0 :
            if is_check_while_delay(while_code) == True :
                print(f"Function True = {fnc_name}")
            else :
                print(f"Function False = {fnc_name}")
# # text = """
# # 		config_section_name = section + section_index;
# #
# #
# # 		if (paCfgReadValue(config_path, config_section_name, "STS_TAG", tmp_sts_tag) != 0)
# # 		{
# # 			if (section_index == 1)
# # 			{
# # 				writeLog(g_script_name, "Failed to load : [dp_name] STS_TAG", LV_ERR);
# # 				is_result = false;
# # 			}
# # 			else
# # 			{
# # 				writeLog(g_script_name, "DP Group Load to " + section + (section_index - 1) + " complete", LV_INFO);
# # 				break;
# # 			}
# #         }
# # 	"""
#
# text = """
#     config_section_name = section + section_index;
#
#
#     if (paCfgReadValue(config_path, config_section_name, "STS_TAG", tmp_sts_tag) != 0)
#     {
#         if (section_index == 1)
#         {
#             writeLog(g_script_name, "Failed to load : [dp_name] STS_TAG", LV_ERR);
#             is_result = false;
#         }
#         else
#         {
#             writeLog(g_script_name, "DP Group Load to " + section + (section_index - 1) + " complete", LV_INFO);
#             break;
#         }
#     }
# config_section_name = section + section_index;
# if (condition) {
#     // some code
# }
#
# try {
#     // some code
# }
#
# no_braces_condition
# """
#
# #1. while문이 있는 경우 코드를 추출
#
# #2. while문 내에서 조건문이 있는 블럭은 제외 하고 delay가 있는지 확인
#
# #3. delay 판단 기준 while문에서
# # while문 블럭 박에서 delay 있는지 확인
# # finnaly 에 delay가 있는 경우는 참으로 판단
#
# # 정규식 패턴: 중괄호 앞에 오는 문자열을 캡처
# # pattern = re.compile(r'(.+?)\s*(?=\{)', re.DOTALL)
# pattern = re.compile(r'([^\s].*?)\s*(?=\{)')
#
#
# matches = list(pattern.finditer(text))
# for match in matches:
#     print("Captured:", match.group(1))
#     print(f"start")
