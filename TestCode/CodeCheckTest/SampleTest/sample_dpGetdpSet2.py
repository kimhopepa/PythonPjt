import re


def check_consecutive_dp_calls(code_block):
    # 함수 호출을 찾기 위한 정규 표현식 패턴
    pattern = r'dp\w+\('

    # 코드 블록 내에서 중괄호 { } 내의 텍스트를 추출
    blocks = re.findall(r'\{(.*?)\}', code_block, re.DOTALL)

    # 중괄호 내에서 연속된 dp* 함수 호출 확인
    for block in blocks:
        dp_calls = re.findall(pattern, block)
        if any(dp_calls[i] == dp_calls[i + 1] for i in range(len(dp_calls) - 1)):
            return True

    return False


def check_same_function(body_code : str):


def check_dpfunction(text : str) -> list :
    # 정규 표현식 패턴: dp로 시작하는 함수 호출 찾기
    pattern = r'dp\w*\('

    # 모든 dp* 함수 호출 찾기
    dp_calls = re.findall(pattern, text)

    return dp_calls

# 예시 코드 블록
code_block = """
if(value == true)
{
    dp_function1();

    dp_function3();
}

dp_function2();
"""

# 함수 호출 확인
if check_consecutive_dp_calls(code_block):
    print("연속된 dp* 함수 호출이 있습니다.")
else:
    print("연속된 dp* 함수 호출이 없습니다.")
