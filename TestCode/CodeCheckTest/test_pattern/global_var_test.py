import re
import lib_function_info as lib

def get_variables(code : str, start_line : int = 0) -> dict :

    # 변수 이름과 변수 초기화값을 리턴
    def get_variable_info(code: str) -> list:
        result_list = []
        tmp_var = None

        # '=' 이걸로 분리
        code_list = code.split('=')
        # 초기화 값이랑 변수 이름을 분리
        if len(code_list) > 1 :
            init_value = code_list[1].strip()
            tmp_var = code_list[0]
        else :
            tmp_var = code_list[0]
            init_value = None

        # 최종 변수 이름 저장
        var_name = tmp_var.split()[-1]
        # 패턴 정의: \w는 문자(대소문자), 숫자, 밑줄을 의미함
        pattern = re.compile(r'^\w+$')
        if bool(pattern.match(var_name)) == True :
            result_list = [var_name, init_value]
        return result_list

    result_dict = {}            # 변수 이름, 초기화 값, 라인수
    lines = code.splitlines()   # 코드를 \n 으로 분리하여 리스트에 저장
    line_count = 0
    block_depth = 0

    # 함수 Body Code인 경우
    if(start_line != 0) : 
        line_count = -1

    # 코드에서 한 줄씩 탐색
    for index, line in enumerate(lines) :
        line_count = line_count + 1
        line = line.strip()

        #1. 블록 depth가 -인 경우의 코드는 제외
        if start_line == 0 :
            if '{' in line :
                block_depth += line.count('{')
            if '}' in line :
                block_depth -= line.count('}')

        if block_depth > 0 :
            continue

        # 변수 선언에 필요한 문자
        if (',' in line or ';' in line) == False :
            continue
        # 변수 선언에 Skip하는 문자
        if ('for' in line or '(' in line or ')' in line) == True :
            continue

        #2. 주석 제거
        line = re.sub(r'//.*', '', line).strip()
        line = re.sub(r'/\*.*?\*/', '', line).strip()

        #3. 코드에서 변수 별로 단위 분리
        parts = re.split(r'[;,]', line )
        parts = [part.strip() for part in parts if part.strip()]
        # print("test parts", parts)

        #4. Code Line에서
        for part in parts :
            var_info = get_variable_info(part)
            if len(var_info) == 2 :
                result_dict[var_info[0]] = [var_info[1], start_line + line_count]

    return result_dict

# Body Code를 입력 받아서
def check_raima(body_code : str, body_number : int,
                global_dict : dict, local_dict : dict) -> list :
    def find_dpSet_pattern(line : str) -> str :
        pattern = r'\bdpSet\w*\(\s*(.*?)\s*,'
        match = re.search(pattern, line)
        if match :
            return match.group(1)
        return ""

    def get_tag_list( tag_info : str) -> list :
        pattern = re.compile(r'\s+|[^\w\s]+')
        split_list = pattern.split(tag_info)        # 정규식 패턴으로 Tag 분리
        tag_list = [s for s in split_list if s]     # 빈 문자열 제거
        return tag_list

    return_list = []                # 파라미터 및
    lines = body_code.splitlines()  # 코드를 \n 으로 분리하여 리스트에 저장
    
    #1. Body 코드를 한줄 씩 실행
    for line_number, line in enumerate(lines) :

        #2. dpSet 패턴이 있으면 첫번째 파라미터를 출력
        dpSet_text = find_dpSet_pattern(line)

        #3. dpSet에서 사용하는 Tag 중에서 ':_alert_hdl' 있는지 체크
        if len(dpSet_text) > 0 :
            print("dpSet_text", dpSet_text)
            tag_list = get_tag_list(dpSet_text)
            while True :
                tag_name = tag_list.pop(0)
                if tag_name in global_dict :
                    tag_value = global_dict[tag_name]
                elif tag_name in local_dict:
                    tag_value = local_dict[tag_name]

                # Tag Value에 대한 검색
                if ':_alert_hdl' in tag_value :
                    return_list = return_list + [[line, body_number + line_number]]
                    break

                tmp_value_list = get_tag_list(tag_value)
                tag_list.extend(tmp_value_list)


        #     while True :
        #         if len(tag_list) == 0 :
        #             break
        #         # dpSet 첫번째 파리미터 정보를 리스트로 반환
        #         tag_item = tag_list.pop(0)
        #         if tag_item in global_dict :
        #             tag_value = global_dict[tag_item]
        #             tmp_tag_list = get_tag_list(tag_value)

                    # (1) tag_value가 변수인 경우 체크
                    # 변수인 경우
                    # 변수가 아닌 경우는 ':_alert_hdl' 포함되는지 확인. 확인되면
                    # (2) tag_value가 문
        #
        #         tag_item =
            #
            #
            # # dpSet에 사용된 파라미터를
            # for tag_item in tag_list :


            # print(body_number + line_number, tag_list)
            # for tag_item in tag_list :
            #     tag_item
            # print(body_number + line_number, dpSet_text)
        # if lib.is_check_pattern(r'dpSetTimed', line)

    return return_list




if __name__ == '__main__':

    path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\8_raima_db_test.ctl'
    text = lib.get_text_file(path)
    global_dict = get_variables(text)        # 전역 변수를 저장
    for index, key in enumerate(global_dict) :
        print(key, global_dict[key])

    fnc_list = lib.get_function_body2(text)
    vars1 = get_variables()
    print("vars1", vars1)
    # for item in fnc_list :
    #     fnc_name = item[0]
    #     body_code = item[1]
    #     body_start_line = item[2]
    #     local_dict = get_variables(body_code, body_start_line)
        # print(body_code)

        # raima_up_list = check_raima(body_code, body_start_line, global_dict, local_dict)
        # # print("fnc_name start line = " + fnc_name, body_start_line)
        # # for index, key in enumerate(local_dict) :
        # #     print(fnc_name, f"[{key}]", local_dict[key])


