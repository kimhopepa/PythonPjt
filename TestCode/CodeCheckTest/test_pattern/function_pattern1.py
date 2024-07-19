import re


def extract_functions(text):
    # 함수 시그니처와 여는 중괄호를 찾기 위한 정규식
    pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{'
    matches = re.finditer(pattern, text, re.DOTALL)

    functions = []

    for match in matches:
        function_name = match.group(1)
        start = match.end() - 1  # 여는 중괄호 위치

        # 중첩 중괄호 처리
        depth = 1
        end = start + 1
        while depth > 0 and end < len(text):
            if text[end] == '{':
                depth += 1
            elif text[end] == '}':
                depth -= 1
            end += 1

        # 함수 본문 추출
        function_body = text[start:end].strip()
        functions.append((function_name, function_body))

    return functions


# 예시 텍스트
example_function = '''
int cx_change(dyn_string k_false_list, bool all_blackout, dyn_int step_list = makeDynInt())
{
    if (condition) {
        // code...
    }
}

void another_function()
{
    // another code...
}
'''

# 함수 이름과 본문 추출
functions = extract_functions(example_function)

for name, body in functions:
    print(f"Function Name: {name}")
    print(f"Function Body:\n{body}\n")