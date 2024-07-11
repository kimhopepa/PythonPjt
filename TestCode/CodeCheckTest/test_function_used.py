import re

def extract_functions_from_code(code: str) -> dict:
    function_dict = {}

    # 함수 이름과 본문을 찾는 정규 표현식
    pattern = re.compile(r'(\w+)\s*\(\)\s*\{\n(.*?)\n\}', re.DOTALL)

    matches = pattern.findall(code)
    for match in matches:
        function_name = match[0]
        function_body = match[1]
        function_dict[function_name] = function_body.strip()

    return function_dict

def find_function_usages(code: str, function_dict: dict) -> dict:
    usage_dict = {func: False for func in function_dict.keys()}

    print("usage_dict", usage_dict)

    # 각 함수 이름에 대해 호출이 있는지 찾는 정규 표현식
    for function_name in function_dict.keys():
        pattern = re.compile(r'\b' + re.escape(function_name) + r'\s*\(\s*\)')
        if pattern.search(code):
            usage_dict[function_name] = True

    return usage_dict

# 예제 코드
code = """
function1() {
    // function1 body
}

function2() {
    function1();
    // function2 body
}

function3() {
    // function3 body
    function2();
}

function4() {
    // function4 body
}
"""

function_dict = extract_functions_from_code(code)
usage_dict = find_function_usages(code, function_dict)

print("Function Dictionary:", function_dict)
print("Usage Dictionary:", usage_dict)