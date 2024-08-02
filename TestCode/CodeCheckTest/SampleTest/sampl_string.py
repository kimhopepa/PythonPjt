import re

# 예제 문자열
text = "    dpGet(dp_name + CHECK,CHECK_TAG,"

# 정규식 패턴
pattern = r"[()]"

# 매칭 확인
match = re.search(pattern, text)

if match:
    print("괄호가 포함되어 있습니다.")
else:
    print("괄호가 포함되어 있지 않습니다.")