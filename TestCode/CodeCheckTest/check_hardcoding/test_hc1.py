import re


def extract_non_operators_with_line_numbers(input_string):
    # 정규식 패턴: 괄호 안의 내용을 추출 (멀티라인 지원, 비연산자 포함)
    pattern = re.compile(r'\(([^)]*)\)', re.DOTALL)
    matches = pattern.finditer(input_string)

    result = []
    for match in matches:
        # 공백이나 빈 인자도 포함하여 캡쳐
        parts = re.split(r'\s*[\+\-\*/\%,]\s*', match.group(1))
        cleaned_parts = [part.strip() for part in parts if part.strip() or part == ""]

        # 매칭된 그룹의 시작 줄 번호를 계산
        start_line = input_string.count('\n', 0, match.start()) + 1

        result.append((cleaned_parts, start_line))

    return result


# 테스트 문자열들
test_strings = [
    'Debug(123)',
    'writeLog("test")',
    'Thread(456)',
    'dpQueryConnectSingle("example")',
    'func(789)',
    'call(tag_name )',
    'dpConnect(100)',
    'processConnection("example")',
    'if(value > 50)',
    'if(value < 50) || if(value ==100)',
    'dpGet(dp_name + CHECK,CHECK_TAG,',
    'dp_name + TIME,VOLT_TIME,',
    'dp_name + MIN,TMP_MIN_VALUE,',
    'dp_name + MAX,TMP_MAX_VALUE,',
    'dp_name + HOLDTIME,Delay_time,',
    'dp_name + ".OFFSET",OFFSET_VALUE);'
]

# 전체 문자열을 하나로 합침
combined_string = '\n'.join(test_strings)

# 전체 문자열에서 괄호 안의 비연산자를 추출
result = extract_non_operators_with_line_numbers(combined_string)

# 결과 출력
for item in result:
    cleaned_parts, start_line = item
    for sub_item in cleaned_parts:
        print(f"Line {start_line}: {sub_item}")
