import re
import lib_function_info as lib



def get_while_code(body_code:str) -> str :
    # 정규식 패턴: while 블록 내의 코드 추출
    pattern = r'while\s*\([^)]*\)\s*{([^{}]*(?:{[^{}]*}[^{}]*)*)}'
    while_block = ""
    # # 정규식 컴파일
    regex = re.compile(pattern, re.DOTALL)
    #
    # # 패턴 검색
    match = regex.search(body_code)
    #
    # # 결과 출력
    #
    if match:
        while_block = match.group(1)
        print("While 문 내의 코드:")
        print(while_block.strip())

    else:
        print("While 문을 찾을 수 없습니다.")

    return while_block

if __name__ == '__main__':

    path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\6_while_delay.txt'
    text = lib.get_text_file(path)
    fnc_list = lib.get_function_list(text)
    # print(text)
    for index, item in enumerate(fnc_list) :
        fnc_name = item[0]
        body_code = item[1]
        start_line = item[2]
        end_line = item[3]
        while_code = get_while_code(body_code)
        if len(while_code) > 0 :
            print(f"Function = {fnc_name}, while code = {while_code}")