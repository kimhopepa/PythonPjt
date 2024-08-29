import re
import lib_function_info as lib


# def get_while_code(body_code:str) -> str :
#     # 정규식 패턴: while 블록 내의 코드 추출
#     pattern = r'while\s*\([^)]*\)\s*{([^{}]*(?:{[^{}]*}[^{}]*)*)}'
#     while_block = ""
#
#     # 정규식 컴파일
#     regex = re.compile(pattern, re.DOTALL)
#     match = regex.search(body_code)
#
#
#     if match:
#         while_block = match.group(1)
#
#     return while_block

def get_while_code(body_code: str) -> str:
    """
    주어진 코드에서 while 블록의 내용을 추출합니다.
    """

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

    pattern = r'while\s*\([^)]*\)\s*{'
    match = re.search(pattern, body_code, re.DOTALL)

    if not match:
        return ""

    start_index = match.end() - 1
    end_index = find_closing_brace_index(body_code, start_index)

    if end_index == -1:
        return ""

    while_block = body_code[start_index + 1:end_index]

    return while_block

def strip_nested_blocks(content):
    """
    중첩된 중괄호 블록을 제거 하고 가장 바깥의 코드만 반환 합니다.
    """
    result = []
    stack = 0
    index = 0
    length = len(content)

    while index < length:
        char = content[index]
        if char == '{':
            if stack == 0:
                # 첫 번째 중괄호는 유지
                result.append('{')
            stack += 1
        elif char == '}':
            stack -= 1
            if stack == 0:
                # 닫는 중괄호는 유지
                result.append('}')
        elif stack == 0:
            result.append(char)
        index += 1
        # print("test", result)

    return "".join(result).strip()


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


def extract_outer_block_content(text:str) -> list:
    """
    가장 바깥의 중괄호 블록에서 중첩된 블록을 제거하고 내용을 반환합니다.
    """
    pattern = re.compile(r'(\b\w+\b)\s*\{', re.DOTALL)
    matches = list(pattern.finditer(text))

    # 가장 바깥 블록 을 저장할 변수
    last_index = 0
    outer_blocks = []


    for match in matches:
        block_name = match.group(1)
        start_index = match.end() - 1

        # { 시작으로 } index 찾기
        end_index = find_closing_brace_index(text, start_index)

        if end_index == -1:
            continue

        block_content = text[start_index + 1:end_index].strip()

        # 중첩 블록을 제거 하기 위한 처리
        # print("test0", text)
        # print(f"test1, block = {block_name} , block_content = {block_content}")
        stripped_content = strip_nested_blocks(block_content)
        # print("test2", stripped_content)
        outer_blocks.append(f"{block_name} {{ {stripped_content} }}")
        # print(f"[extract_outer_block_content] , block_name = {block_name}, code = {stripped_content} ")

    return "\n".join(outer_blocks)




# 주어진 C언어 코드 텍스트
text = """
try
{
    if(avtive == true)
    {
        //if코드
        //test
        dpSet("test", true);
        delay(1);
    }
    delay(1);
}
catch
{
    DebugTN("test1");
}
"""

# # 가장 바깥의 중괄호 블록에서 내용 추출
# outer_block_content = extract_outer_block_content(text)
#
# # 추출된 내용 출력
# print(outer_block_content)





def contains_delay_pattern(text:str) -> bool:
    def remove_comments(text):
        """
        주석을 제거하는 함수. 한 줄 주석과 여러 줄 주석을 모두 처리합니다.
        """
        # 한 줄 주석 제거
        text = re.sub(r'//.*', '', text)
        # 여러 줄 주석 제거
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        return text
    # 주석을 제거한 텍스트
    text_without_comments = remove_comments(text)

    # 정규식 패턴 정의 (주석 없이 delay*); 패턴을 찾음)
    pattern = r'delay.*\);'

    # 정규식 검색
    match = re.search(pattern, text_without_comments)

    return match is not None

# while문내의 코드 블럭에서 delay가 작성 되어있는지 확인
def is_check_while_delay(text : str) -> bool:

    # 중첩된 중괄호를 처리하여 닫는 중괄호 인덱스를 찾기
    def find_closing_brace_index(text : str, open_brace_index:int) -> int:
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
    """
    모든 블록을 추출하고 블록 외부의 코드를 'main' 블록으로 저장합니다.
    """
    result = False
    pattern = re.compile(r'(\b\w+\b)\s*\{', re.DOTALL)
    matches = list(pattern.finditer(text))

    if not matches:
        return False

    # key = Block의 제목 , value = Block 코드의 내부(이중 블록 안의 내용은 삭제하여 저장)
    main_block = "main"
    block_dict = {}
    blocks = []
    last_index = 0

    # 블록에서 delay 유/무를 판단
    for match in matches:
        block_name = match.group(1)
        start_index = match.end() - 1

        # { 시작으로 } index 찾기
        end_index = find_closing_brace_index(text, start_index)

        if end_index == -1:
            continue

        # 블록 외부의 코드 추가
        if last_index < match.start():
            external_code = text[last_index:match.start()].strip()
            if external_code:
                blocks.append(f"main {{ {external_code} }}")
                if contains_delay_pattern(external_code) == True :
                    result = True

        block_content = text[start_index + 1:end_index].strip()
        if contains_delay_pattern(block_content) == True:
            result = True

        last_index = end_index + 1

    # 마지막 블록 이후의 코드 처리
    if last_index < len(text):
        remaining_content = text[last_index:].strip()
        if remaining_content:
            if contains_delay_pattern(remaining_content) == True:
                result = True


    return  result



if __name__ == '__main__':

    path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\7_loop_dp_function.ctl'
    text = lib.get_text_file(path)
    fnc_list = lib.get_function_body2(text)
    # print(text)
    for index, item in enumerate(fnc_list) :
        fnc_name = item[0]
        body_code = item[1]
        start_line = item[2]
        end_line = item[3]
        while_code = get_while_code(body_code)
        # print(f"function = {fnc_name} , body_code = {body_code}")
        print(f"Function True = {fnc_name} , while = {len(while_code)}")
        if len(while_code) > 0 :

            # print(f"Function = {fnc_name}, body_code =  {body_code}, while_code = {while_code}")
            if is_check_while_delay(while_code) == True :
                print(f"Function True = {fnc_name}")
            else :
                print(f"Function False = {fnc_name}")
            # , body_code =  {body_code}, while_code = {while_code}")
            # print(f"Block name = {outer_block_content[0]}, while code = {outer_block_content}")
            # print(type(outer_block_content))
            # print(outer_block_content)