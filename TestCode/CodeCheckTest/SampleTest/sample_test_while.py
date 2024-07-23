import re

def get_body_info3(text: str) -> list:
    """
    주어진 텍스트에서 중괄호 블록을 추출합니다. 주석을 제거하지 않고 주석에 의한 라인 수 변화를 처리합니다.
    """
    stack = []
    result = []
    line_number = 1
    start_index = None
    start_line = None
    i = 0

    while i < len(text):
        char = text[i]

        # 주석이 시작되면 주석 처리
        if text[i:i+2] == '//':
            while i < len(text) and char != '\n':
                i += 1
                if i < len(text):
                    char = text[i]
            line_number += 1
        elif text[i:i+2] == '/*':
            while i < len(text) and text[i:i+2] != '*/':
                i += 1
                if i < len(text):
                    char = text[i]
            i += 1  # Skip '*/'
        else:
            if char == '\n':
                line_number += 1
            elif char == '{':
                if start_index is None:
                    start_index = i
                    start_line = line_number
                stack.append((i, line_number))
            elif char == '}' and stack:
                start_pos, start_ln = stack.pop()
                if not stack:
                    end_line = line_number
                    result.append([text[start_index + 1:i], start_ln, end_line])
                    start_index = None
                    start_line = None

        i += 1

    return result

# 주어진 코드 예제
text = """
// This is a single line comment
func1()
{
    /* This is a multi-line comment
    spanning multiple lines */
    {
        // Comment inside inner block
        some_code();
    }
}
//func2()
//{
//}
/*func3()
{
}*/
"""

# 블록 정보 추출
block_info = get_body_info2(text)

# 추출된 블록 정보 출력
for block in block_info:
    print(f"Block content:\n{block[0]}\nStart line: {block[1]}, End line: {block[2]}")