def find_brace_lines(text, start_index):
    # 텍스트를 라인 단위로 분리
    lines = text.split('\n')

    # 시작 인덱스가 속한 라인 번호 찾기
    line_count = 0
    current_index = 0
    start_line = 0
    for line in lines:
        line_count += 1
        current_index += len(line) + 1  # +1은 줄 바꿈 문자
        if current_index > start_index:
            start_line = line_count
            break

    # 여는 중괄호부터 시작하여 중첩된 중괄호 추적
    depth = 1
    for i in range(start_index + 1, len(text)):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1

        if depth == 0:
            end_index = i
            break
    else:
        raise ValueError("No matching closing brace found")

    # 종료 인덱스가 속한 라인 번호 찾기
    end_line = 0
    current_index = 0
    line_count = 0
    for line in lines:
        line_count += 1
        current_index += len(line) + 1  # +1은 줄 바꿈 문자
        if current_index > end_index:
            end_line = line_count
            break

    return start_line, end_line


# 예시 텍스트
example_text = '''


void example_function() {
    if (condition) {
        // nested block
        while (true) {
            // inner block
        }
    }
}
void func_3(int a, int b){
	DebugTN("test func3()");
}
'''

# 함수 테스트
start_index = example_text.find('{')
if start_index != -1:
    start_line, end_line = find_brace_lines(example_text, start_index)
    print(f"Opening brace starts at line {start_line} and matching closing brace is at line {end_line}")
else:
    print("No opening brace found")