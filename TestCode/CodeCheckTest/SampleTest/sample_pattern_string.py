import re


def contains_delay_pattern(text):
    # 정규식 패턴 정의
    pattern = r'delay.*\);'

    # 정규식 검색
    match = re.search(pattern, text)

    return match is not None


# 테스트용 코드
text1 = "This is some code with delay_cycle(10); function."
text2 = "This code does not contain the pattern."

print(contains_delay_pattern(text1))  # 출력: True
print(contains_delay_pattern(text2))  # 출력: False

