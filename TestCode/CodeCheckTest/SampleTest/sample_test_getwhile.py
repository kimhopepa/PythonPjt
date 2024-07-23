import re


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

    while_block = body_code[start_index + 1:end_index].strip()

    return while_block


# 테스트용 코드
body_code = """
void func_6(int a, int b)
{
    while(true)
    {
        try
        {
            delay(1);
            if(test == true)
            {
                // Some code
            }
        }
        catch
        {
            // Handle exception
        }
        finally
        {
            delay(1);
        }
    }
}
"""

# while 블록 내용 추출
while_code = get_while_code(body_code)

# 추출된 while 블록 출력
print("While block content:")
print(while_code)