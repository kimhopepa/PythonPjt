import re


def find_strings_in_function_calls(code, function_name):
    # 정규 표현식을 사용하여 함수 호출에서 문자열 리터럴을 찾기
    pattern = re.compile(rf'{function_name}\(([^)]*)\)')
    matches = pattern.findall(code)

    strings = []
    string_pattern = re.compile(r'"([^"]+)"')

    for match in matches:
        # 함수 인자에서 문자열 리터럴을 추출
        strings += string_pattern.findall(match)

    return strings


# 예제 코드
code = """
result = dpSetTimedWait(0, in_manager_dp_name + ".alert.Heartbeat_ALM:_alert_hdl.._active", false,
in_manager_dp_name + ".alert.ConnAlarm_WARN:_alert_hdl.._active", false,
in_manager_dp_name + ".alert.ConnAlarm_ALM:_alert_hdl.._active", false);

dpSet("AA.PVLAST", true);
"""

# 함수 호출에서 문자열 리터럴 찾기
function_name1 = "dpSetTimedWait"
strings_in_function1 = find_strings_in_function_calls(code, function_name1)

function_name2 = "dpSet"
strings_in_function2 = find_strings_in_function_calls(code, function_name2)

# 결과 출력
print(f'{function_name1}에서 사용된 문자열:')
for s in strings_in_function1:
    print(f'"{s}"')

print(f'\n{function_name2}에서 사용된 문자열:')
for s in strings_in_function2:
    print(f'"{s}"')
