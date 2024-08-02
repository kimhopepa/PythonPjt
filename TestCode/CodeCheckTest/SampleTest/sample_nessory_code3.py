import re


# 입력받은 패턴의 캡쳐를 문자열로 반환
def get_pattern(text : str, pattern : str) -> str :
    match = re.search(pattern, text)
    
    if match :
        return match.group(1)
    else :
        return text

def get_varable_list(text:str, depth_number:int = 0) -> list:

    # 텍스트를 줄 단위로 분리
    lines = text.splitlines()
    result = []

    brace_depth = 0
    for line_number, line in enumerate(lines):
        line = line.strip()

        # Update brace depth
        brace_depth += line.count('{')
        brace_depth -= line.count('}')

        # 설정한 depth보다 낮은 경우는 제외
        if brace_depth > depth_number :
            continue

        # 괄호가 포함된 줄은 제외
        if re.search(r"[()]", line):
            continue

        # 콤마(,)와 세미콜론(;)이 포함된 줄만 결과에 추가
        if ',' in line or ';' in line:

            line = line.replace(';', "")
            parts = line.split(',')

            for part in parts :
                part = part.strip()
                if '=' in part :
                    part = get_pattern(part, r'^\s*(.*?)\s*=')

                temp_var_list = part.split(' ')
                list_length = len(temp_var_list)
                if list_length > 0 :
                    part = temp_var_list[list_length-1]

                result = result + [[line_number + 1, part]]
            # result.append({
            #     'line_number': line_number,
            #     'line_content': part
            # })

    return result

# 예제 텍스트
text = '''
dpSet("test", false);
dpGetValue("anotherTest");
dpFunction("arg");
func()
{
dpExample("example") = someValue;
dpSetWait(all_sts_dp + cfg_stoptime_para, t) != 0;
Another line without commas or semicolons
Yet another line, with some text; and a semicolon;

int a, b, c ;
}
const string version = "test" ;
'''

# 함수 호출 및 결과 출력
results = get_varable_list(text)

for result in results:
    print(result)

