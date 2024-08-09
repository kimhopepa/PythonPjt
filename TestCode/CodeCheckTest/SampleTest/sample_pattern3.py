import re

def get_patterns_with_line_numbers(text: str, pattern: str) -> list:
    matches = re.finditer(pattern, text)
    results = []

    for match in matches:
        start_pos = match.start()
        # 텍스트의 0부터 start_pos까지의 줄바꿈 문자 개수를 세어 몇 번째 라인인지 계산

        matched_text = match.group(0)
        matched_line_count = matched_text.count('\n')
        line_number = text.count('\n', 0, start_pos) + 1 + matched_line_count
        print("matched_line_count", matched_line_count)

        matched_text = match.group(0).strip()  # 공백을 제거함
        results.append((matched_text, line_number))

    return results

# 테스트 예시
text = """
int result = dpSetWait("test", value);

dpSetWait("test", value);




dpGet("", value);
"""
pattern = r'(?<![!=\s])\s*dp[a-zA-Z][a-zA-Z0-9_]*\([^()\n]*\)\s*(?![!=\s])'
matches_with_line_numbers = get_patterns_with_line_numbers(text, pattern)

for match, line_number in matches_with_line_numbers:
    print(f"Match: '{match}' on line {line_number}")