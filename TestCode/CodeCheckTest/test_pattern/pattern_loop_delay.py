import re

# 정규 표현식 패턴
pattern = r'(\b\w+\b).*?\{'

# 테스트 문자열들
texts = [
    "example {",
    "test123(true==1)    {",
    "word_with_underscores   {",
    "no_match_here",
    "example_with_text_before {",
    "test123  other_text{"
]

for text in texts:
    match = re.search(pattern, text)
    if match:
        print(f"Matched in text '{text}': {match.group(1)}")
    else:
        print(f"No match found in text '{text}'")