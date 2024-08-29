import re

pattern = r"(\b\w+\b)\s*\{"  # 정규식 패턴
text = """
function {
    code block
}
main{
    more code
}
anotherFunction    {
    code here
}
"""

# re.findall을 사용하여 일치하는 모든 단어를 찾습니다.
compile_pattern = re.findall(pattern, re.DOTALL)
matches = list(compile_pattern.finditer(text))

if matches:
    print("일치하는 단어들:", matches)
else:
    print("일치하는 부분이 없습니다.")