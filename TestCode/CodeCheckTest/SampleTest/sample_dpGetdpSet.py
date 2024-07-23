# import re
#
#
# def extract_for_blocks(code):
#     pattern = re.compile(r'(for\s*\(.*?\)\s*\{[^}]*\})', re.DOTALL)
#     matches = pattern.findall(code)
#
#     blocks = []
#     for match in matches:
#         title_match = re.match(r'(for\s*\(.*?\))', match)
#         if title_match:
#             title = title_match.group(1)
#             blocks.append({"title": title, "content": match})
#
#     return blocks
#
#
# def print_blocks(blocks):
#     for block in blocks:
#         print(f"{block['title']} 제목으로 블록 코드 부분:")
#         print(block['content'])
#         print()
#
#
# # Example usage
# code = """if(true)
# {
#     // not captured
#     for(int i = 1 ; i <= 10 ; i ++)
#     {
#         // captured code part
#         printf("Hello World");
#     }
#     // not captured
# }"""
#
# blocks = extract_for_blocks(code)
# print_blocks(blocks)


import re


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


def print_blocks(blocks):
    for block in blocks:
        print(f"{block['title']} (라인 {block['line_number']}) 제목으로 블록 코드 부분:")
        print(block['content'])
        print()


# Example usage
code = """if(true)
{
	string dp_name = "test1.pvlast" ; 
	string dp_name2 = "test2.pvlast" ; 
	float value;
	dyn_string dp_list;
	dyn_anytype list;
	
	for(int i = 1 ; i <= dynlen(dp_list); i++)
	{
		dpGet(dp_list[i], list[i]);
	}
	
	delay(1);
	
	for(int i = 1 ; i <= dynlen(list); i++)
	{
		dpSet(list[i], 0);
	}

}"""

if __name__ == '__main__':
    print("Start")
    loop_dpfunction_list = loop_pattern_check(code, 0)
    print(loop_dpfunction_list)
