import re
# path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\1_testcode.txt'
path = r'C:\Users\KIMJH\Documents\GitHub\PythonPjt\CodeReviewTool\doc\3_hardcoding.txt'



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

def check_str_hard_coding(input_string:str) -> bool :
    if is_number(input_string) or is_string(input_string) :
        return True
    else :
        return False

#[하드 코딩 검출1] 대입 연산식에 하드코딩 사용 케이스
def check_hardcoding_operation(line_code : str) -> bool:
    r_pattern = re.compile(r'=\s*([^;]+)\s*;')              #[Pattern] 대입 연산자에서 우항 캡쳐
    non_operaion_pattern = re.compile(r'[^\s\+\-\*/\%]+')   #[Pattern] 대입 연산자에서 우항 캡쳐
    match = r_pattern.search(line_code)

    result = False
    if match:
        # 1. 우항 데이터 캡쳐
        r_expression = match.group(1).strip()
        # 2. 우항 데이터에서 비연산자들만 리스트로 반환
        non_operators = non_operaion_pattern.findall(r_expression)
        # 3. 문자열 or 숫자만 있는 경우 체크
        for item in non_operators :
            if check_str_hard_coding(item) == True :
                result = True
                break

    return result

#[하드 코딩 검출2] 조건문 or 함수내에 하드 코딩 사용 케이스

def extract_non_operators_with_line_numbers(input_string):
    # 정규식 패턴: 괄호 안의 내용을 추출 (멀티라인 지원, 비연산자 포함)
    pattern = re.compile(r'\(([^)]*)\)', re.DOTALL)
    matches = pattern.finditer(input_string)

    lines = input_string.split('\n')

    result = []
    for match in matches:
        # 공백이나 빈 인자도 포함하여 캡쳐
        parts = re.split(r'\s*[\+\-\*/\%,]\s*', match.group(1))
        non_operators = [part.strip() for part in parts if part.strip() or part == ""]

        # 매칭된 그룹의 시작 줄 번호를 계산
        start_line = input_string.count('\n', 0, match.start()) + 1
        # 원본 문자열을 포함하여 저장
        original_line = lines[start_line-1].strip()
        # skip 대상 있는지 확인
        if(check_skip_string(original_line) == False) :
            for operator_item in non_operators:
                if check_str_hard_coding(operator_item) == True:
                    result.append((start_line, original_line))
                    break


    return result

def check_skip_string(input_text : str) -> bool :
    skip_list =['Debug', 'dpConnect', 'writeLog', 'startThread']
    skip_check = False
    skip_check = any(list_item in input_text for list_item in skip_list)

    return skip_check




#0 파일을 읽어서 문자열로 변수에 저장
text = ""
with open(path, 'r',  encoding='utf-8') as file:
    text = file.read()

#1. 대입 연산자
for line_code in text.split('\n'):
    if(check_hardcoding_operation(line_code) == True):
        print("check", line_code)


#2. 괄호안 확인
result = extract_non_operators_with_line_numbers(text)
for item in result :
    print(item)
