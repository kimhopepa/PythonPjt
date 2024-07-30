import re

def find_comma_semicolon_lines(text):
    # 텍스트를 줄 단위로 분리
    lines = text.splitlines()
    result = []

    for line_number, line in enumerate(lines, start=1):
        # 괄호가 포함된 줄은 제외
        if re.search(r'\(.*?\)', line):
            continue

        # 콤마와 세미콜론이 포함된 줄만 결과에 추가
        if ',' in line or ';' in line:
            # 콤마로 분리하여 리스트로 저장
            parts = line.split(',')
            result.append({
                'line_number': line_number,
                'line_content': parts
            })

    return result

# 예제 텍스트
text = '''
dpSet("test", false);
dpGetValue("anotherTest");
dpFunction("arg");
dpExample("example") = someValue;
dpSetWait(all_sts_dp + cfg_stoptime_para, t) != 0;
Another line without commas or semicolons
Yet another line, with some text; and a semicolon;
'''

# 함수 호출 및 결과 출력
results = find_comma_semicolon_lines(text)

for result in results:
    print(f"Line {result['line_number']}:")
    for part in result['line_content']:
        print(f"  {part.strip()}")
