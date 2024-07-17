import re
def is_number(s:str) -> bool :
    if s.isdigit() :
        return True
    else :
        return False

def is_string(s:str) -> bool :
    if '"' in s :
        return True
    else :
        return False

def check_str(input_string:str) -> bool :
    if is_number(input_string) or is_string(input_string) :
        return True
    else :
        return False

def check_hardcoding_operation(line_code : str):
    r_pattern = re.compile(r'=\s*([^;]+)\s*;')              #[Pattern]
    non_operaion_pattern = re.compile(r'[^\s\+\-\*/\%]+')
    match = r_pattern.search(line_code)

    result_comment = "None"
    if match:
        # 1. 우항 데이터 캡쳐
        r_expression = match.group(1).strip()
        # 2. 우항 데이터에서 비연산자들만 리스트로 반환
        non_operators = non_operaion_pattern.findall(r_expression)
        # 3. 문자열 or 숫자만 있는 경우 체크
        for item in non_operators :
            if check_str(item) == True :
                result_comment = "하드코딩 되었습니다. code = %s" % (line_code)
                break
            else :
                result_comment = "[Pass] code = %s" % (line_code)

    return result_comment

# 테스트 문자열들
test_strings = [
    'variable = 123;',              # '123'
    ' variable = 456 ; // comment', # '456'
    'variable = "abc";',            # '"abc"'
    'variable = 789; // comment',   # '789'
    'variable = 0123;    ',         # '0123'
    'a1 = b1;    ',                 # 'b1'
    'a1 = b1 + "TEST";    ',        # 'b1 + "TEST"'
    'a1 = "TEST" + b1 ;    ',       # '"TEST" + b1'
    'a1 = b1 + 50 ;    ',           # 'b1 + 50'
    'a1 = 50 - b1 ;    ',           # '50 - b1'
]

# 테스트
for test_string in test_strings:
    result = check_hardcoding(test_string)
    print("result", result)
    # print(f'Expression: {test_string}  RHS: {result}')
