import re
import lib_function_info as lib

# Function의 Body 코드를 입력받아
def loop_pattern_check(body_code:str,  start_line:int) -> list:

    def check_pattern(loop_block_code:str, pattern_text:str,) -> bool:
        #1. 정규식 패턴: dp로 시작하고 대문자 문자로 이어진 후 (로 끝나는 패턴
        # pattern = re.compile(r'(dp[A-Z]\w*\()', re.MULTILINE)
        pattern = re.compile(pattern_text, re.MULTILINE)
        matches = pattern.finditer(loop_block_code)
        found = False

        #2. dp* 함수가 있는 경우 체크
        for match in matches:
            found = True
            break
        return found

    # 1. for문의 정규식 생성
    pattern = re.compile(r'(for\s*\(.*?\)\s*\{[^}]*\})', re.DOTALL)

    #2. 정규식에 맞는 코드 매칭
    matches = pattern.finditer(body_code)

    #3. 리턴할 데이터 리스트 저장(에러 반복문) : string, int -> result_list
    result_list = []
    lines = body_code.splitlines()

    #3. for문 패턴 매칭 동작
    for match in matches:
        match_text = match.group(0) # 캡쳐 되는 첫번째 그룹
        match_start = match.start()

        # Calculate line number
        line_number = body_code[:match_start].count('\n') + 1

        # for문 Block에 dp*패턴이 있는지 확인
        dp_function_pattern = r'(dp[A-Z]\w*\()'
        if check_pattern(match_text ,dp_function_pattern) == True :
            # title 찾는 정규식
            title_match = re.match(r'(for\s*\(.*?\))', match_text)

            if title_match:
                title = title_match.group(0)
                result_list = result_list + [[title, start_line + line_number]]
            else :
                result_list = result_list + [[title_match, start_line + line_number]]
    return result_list




if __name__ == '__main__':
    path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\7_loop_dp_function.txt'
    text = lib.get_text_file(path)
    fnc_list = lib.get_function_body2(text)
    loop_function_list = []
    for index, item in enumerate(fnc_list):
        fnc_name = item[0]
        body_code = item[1]
        start_line = item[2]
        end_line = item[3]
        tmp_list = loop_pattern_check(body_code, start_line)
        for item in tmp_list :
            print(fnc_name, item[0], item[1])
        # print(index, fnc_name, tmp_list)


