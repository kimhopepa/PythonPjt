import re





def contains_delay_pattern(text):
    def remove_comments(text):
        """
        주석을 제거하는 함수. 한 줄 주석과 여러 줄 주석을 모두 처리합니다.
        """
        # 한 줄 주석 제거
        text = re.sub(r'//.*', '', text)
        # 여러 줄 주석 제거
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        return text
    # 주석을 제거한 텍스트
    text_without_comments = remove_comments(text)

    # 정규식 패턴 정의 (주석 없이 delay*); 패턴을 찾음)
    pattern = r'delay.*\);'

    # 정규식 검색
    match = re.search(pattern, text_without_comments)

    return match is not None


# 테스트용 코드
text1 = "This is some code with delay(1); function."
text2 = "This code does not contain the pattern."
text3 = "// delay1); This is a comment."
text4 = "/* delay2); This is a multi-line comment */ delay1);"
text5 = """
delay(10);
try
{
    delay(1);
    if(test == true)
    {
        // delay(100);
        dpSet();
    }
}
catch
{
    /* delay(50); */
}
finally
{
    delay(1);
}
delay(10);
"""

print(contains_delay_pattern(text1))  # 출력: True
print(contains_delay_pattern(text2))  # 출력: False
print(contains_delay_pattern(text3))  # 출력: False
print(contains_delay_pattern(text4))  # 출력: True
print(contains_delay_pattern(text5))  # 출력: True
