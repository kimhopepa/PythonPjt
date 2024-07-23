# import re
#
#
# def find_closing_brace_index(text, open_brace_index):
#     """
#     중첩된 중괄호를 처리하여 닫는 중괄호의 인덱스를 찾습니다.
#     """
#     stack = 0
#     for index, char in enumerate(text[open_brace_index:], start=open_brace_index):
#         if char == '{':
#             stack += 1
#         elif char == '}':
#             stack -= 1
#             if stack == 0:
#                 return index
#     return -1
#
#
# def strip_nested_blocks(content):
#     """
#     중첩된 중괄호 블록을 제거하고 가장 바깥의 코드만 반환합니다.
#     """
#     result = []
#     stack = 0
#     index = 0
#     length = len(content)
#
#     while index < length:
#         char = content[index]
#         if char == '{':
#             if stack == 0:
#                 result.append('{')
#             stack += 1
#         elif char == '}':
#             stack -= 1
#             if stack == 0:
#                 result.append('}')
#         elif stack == 0:
#             result.append(char)
#         index += 1
#
#     return "".join(result).strip()
#
#
# def extract_outer_block_content(text):
#     """
#     모든 블록을 추출하고 블록 외부의 코드를 'main' 블록으로 저장합니다.
#     """
#     pattern = re.compile(r'(\b\w+\b)\s*\{', re.DOTALL)
#     matches = list(pattern.finditer(text))
#
#     if not matches:
#         return f"main {{ {text.strip()} }}"
#
#     blocks = []
#     block_ranges = []
#     last_index = 0
#
#     for match in matches:
#         block_name = match.group(1)
#         start_index = match.end() - 1
#
#         # { 시작으로 } index 찾기
#         end_index = find_closing_brace_index(text, start_index)
#
#         if end_index == -1:
#             continue
#
#         block_content = text[start_index + 1:end_index].strip()
#         stripped_content = strip_nested_blocks(block_content)
#         blocks.append(f"{block_name} {{ {stripped_content} }}")
#         block_ranges.append((last_index, start_index))
#         last_index = end_index + 1
#
#     # 마지막 블록 이후의 코드 처리
#     block_ranges.append((last_index, len(text)))
#     remaining_content = ""
#     for start, end in block_ranges:
#         if start < end:
#             remaining_content += text[start:end].strip() + "\n"
#
#     # 블록 외부의 코드를 'main'으로 저장
#     remaining_content = remaining_content.strip()
#     if remaining_content:
#         blocks.append(f"main {{ {remaining_content} }}")
#
#     return "\n".join(blocks)
#
#
# # 테스트용 코드
# text = """
#     delay(100);
#     try
#     {
#         delay(1);
#         if(test == true)
#         {
#         }
#     }
#     catch
#     {
#
#     }
#     finally
#     {
#         delay(1);
#     }
#     delay(10);
# """
#
# # 블록 제목과 내용 추출
# outer_blocks = extract_outer_block_content(text)
#
# # 추출된 블록 정보 출력
# print("Extracted blocks:")
# print(outer_blocks)






import re


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
def extract_outer_block_content(text : str) -> bool:

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

                # if main_block in block_dict :
                #     block_dict[main_block] += external_code
                # else :
                #     block_dict[main_block] = external_code


        block_content = text[start_index + 1:end_index].strip()
        if contains_delay_pattern(block_content) == True:
            result = True
        # blocks.append(f"{block_name} {{ {block_content} }}")
        # block_dict[block_name + str(start_index)] = block_content

        last_index = end_index + 1

    # 마지막 블록 이후의 코드 처리
    if last_index < len(text):
        remaining_content = text[last_index:].strip()
        if remaining_content:
            # blocks.append(f"main {{ {remaining_content} }}")
            if contains_delay_pattern(remaining_content) == True:
                result = True
            # if main_block in block_dict:
            #     block_dict[main_block] += remaining_content
            # else:
            #     block_dict[main_block] = remaining_content

    return  result
    # print("blocks", blocks)
    # print(block_dict)
    # return "\n".join(blocks)

# 테스트용 코드
text = """
    delay(100);
    try
    {
        delay(1);
        if(test == true)
        {
        }
    }
    catch
    {
        DebugTN();
        if(vlaue)
        {
        }
    }
    finally
    {
        delay(1);
    }
    delay(10);
"""

# 블록 제목과 내용 추출
outer_blocks = extract_outer_block_content(text)

# 추출된 블록 정보 출력
print("Extracted blocks:")
print(outer_blocks)
