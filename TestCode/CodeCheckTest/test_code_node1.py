
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            file_text = file.read()
            # file_text = file.readlines()
        return file_text
    except Exception as e :
        print(f"An error occurred: {e}")
def split_code_by_braces(c_code):
    lines = c_code.split('\n')
    level = 0
    code_by_level = {}
    current_code = []

    for line in lines:
        stripped_line = line.strip()

        if stripped_line == '':
            continue

        if stripped_line.startswith('}') and level > 0:
            if level in code_by_level:
                code_by_level[level].append('\n'.join(current_code))
            else:
                code_by_level[level] = ['\n'.join(current_code)]
            current_code = []
            level -= 1

        if level not in code_by_level:
            code_by_level[level] = []

        current_code.append(line)

        if stripped_line.endswith('{'):
            if level in code_by_level:
                code_by_level[level].append('\n'.join(current_code))
            else:
                code_by_level[level] = ['\n'.join(current_code)]
            current_code = []
            level += 1

    if current_code:
        if level in code_by_level:
            code_by_level[level].append('\n'.join(current_code))
        else:
            code_by_level[level] = ['\n'.join(current_code)]

    return code_by_level


# 테스트용 C 코드
file_path = r'D:\1_기술혁신팀\9_SVN_DATA\4_코드리뷰점검Tool\ELEC\1_Check_Unused_Code.ctl'
c_code = """
#include <stdio.h>

int main() {
    printf("Hello, World!\\n");

    if (1) {
        printf("Inside if block\\n");

        while (1) {
            printf("Inside while loop\\n");
            break;
        }
    }

    return 0;
}
"""

c_code = read_file(file_path)

# 함수 호출 및 결과 출력
split_code = split_code_by_braces(c_code)
for level, codes in split_code.items():
    print(f"Level {level}:")
    for code in codes:
        print(code)
        print("-----------")