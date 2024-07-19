import re

# 정규식 패턴
pattern = r'(?<!\S=)\bdp[A-Z][a-zA-Z0-9_]*\([^)]*\)(?!\s*=\S)'

# 멀티라인 텍스트 예제
text = '''
result=dpA(dd,tt,aa,cc);
dpB(dd,aa);
// dpC(some random text);
dpD(another_example);
result=dpGet("aa"
,a);
dpSet("aa",a);
if (dpSetaaa("AA", a, 
"bb", b)  )
'''

def find_non_assignment_functions(text):
    result = []
    # 주석이 아닌 줄들로 구성된 텍스트를 생성
    lines = text.split('\n')
    code_lines = []
    for line in lines:
        if not line.strip().startswith('//'):
            code_lines.append(line)
    code_text = '\n'.join(code_lines)

    # 정규식 검색
    matches = re.finditer(pattern, code_text, re.MULTILINE | re.DOTALL)
    for match in matches:
        start, end = match.span()
        line_number = code_text[:start].count('\n') + 1
        result.append((match.group().strip(), line_number))

    return result

# 함수 호출 예제
matches = find_non_assignment_functions(text)

# 매칭된 패턴과 라인 수 출력
for match, line_number in matches:
    print(f"Matched pattern: {match}, Line: {line_number}")
