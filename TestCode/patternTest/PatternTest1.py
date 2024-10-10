import re

# 수정된 패턴: dpGet 또는 dpSet 다음에 이어지는 문자를 찾는 패턴
dp_function_pattern = r'(dp(?:Get|Set)\w*\()'

# 예시 텍스트
text = """
dpGetValue()
dpSetValue()
dpUpdate()
dpGetAnotherValue()
dpSetConfig()
dpGet()
dpSet()
"""

# 패턴에 맞는 모든 함수 호출 찾기
matches = re.findall(dp_function_pattern, text)

print(matches)
