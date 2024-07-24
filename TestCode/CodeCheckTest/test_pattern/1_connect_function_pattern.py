import re
import lib_function_info as lib

# dpConnect 함수가 
def get_dpconnect_function(body_text:str) -> list :
    
    # Connect 코드에서 Connect 함수 이름을 리턴
    def get_function_name(conncet_code_text : str) -> str :
        match = re.search(r'"(.*?)"', conncet_code_text)
        if match :
            return match.group(1)
        else :
            return ""

    result_list = []    # 함수에서 connect 함수만 저장하여 반환
    connect_pattern_list = []                                        # 패턴되는 코드를 리스트에 저장하여 리턴
    pattern = r'dp\w*Connect\w*\s*\(\s*[\s\S]*?\s*\)\s*;'   # dp*Connect* 함수 패턴
    matches = re.findall(pattern, body_text, re.DOTALL)     # re.DOTALL 옵션은
    # 줄바꿈 문자 제거 후 결과 출력
    connect_pattern_list = [re.sub(r'\s+', ' ', match) for match in matches]
    for item in connect_pattern_list :
        connect_function_name = get_function_name(item)
        if len(connect_function_name) > 0 :
            result_list = result_list + [connect_function_name]

    return result_list
if __name__ == '__main__':

    path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\7_loop_dp_function.txt'
    text = lib.get_text_file(path)
    fnc_list = lib.get_function_body2(text)

    total_fnc_list = []
    check_list = get_dpconnect_function(text)
    unique_list = list(set(check_list))
    print(unique_list)
    # for index, item in enumerate(fnc_list) :
    #     fnc_name = item[0]
    #     body_code = item[1]
    #     start_line = item[2]
    #     end_line = item[3]
    #     check_list = get_dpconnect_function(body_code)
    #     total_fnc_list = total_fnc_list + check_list

    # unique_list = list(set(total_fnc_list))
    #
    # [total_fnc_list.append(x) for x in total_fnc_list if x not in total_fnc_list]
    # print(unique_list)