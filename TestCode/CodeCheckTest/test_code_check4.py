import re

# 파일 읽어서 text로 리턴
def read_file_and_return_text(file_path):
    # test_list = []
    try:
        with open(file_path, 'r') as file:
            file_text = file.read()

        # 공백, 탭, 개행 문자만 포함된 줄을 제외하고 나머지 라인들을 다시 합칩니다.
        non_empty_lines = [line for line in file_text if line.strip()]

        # for line in file_text.split('\n'):
        #     print('line', line, len(line))

        return ''.join(non_empty_lines)

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def read_file_empry_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()


        # 공백, 탭, 개행 문자만 포함된 줄을 제외하고 나머지 라인들을 다시 합칩니다.
        non_empty_lines = [line for line in lines if line.strip() != ""]
        result_text =''.join(non_empty_lines)
        # print("read_file_empry_lines \n", result_text)

        return result_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def remove_comments(code):

    # print("test1", code)
    # code = code.replace("\n", "")

    # 한 줄 주석 제거
    code = re.sub(r'//.*', '', code)

    # 여러 줄 주석 제거
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

    # 여러 줄 주석 내의 모든 행 삭제
    code = re.sub(r'(/\*.*?\*/)', lambda x: '\n' * x.group(0).count('\n'), code, flags=re.DOTALL)

    # print('remove_comments1', code)
    # non_empty_lines = [line for line in code if line.strip() != ""]
    # result_text = ''.join(non_empty_lines)
    lines = code.splitlines(True)
    non_empty_lines = [line for line in lines if line.strip() != ""]
    result_text = ''.join(non_empty_lines)
    # print('remove_comments2', result_text)
    # non_empty_lines = [line for line in code if line.strip() != ""]
    # print("test3",non_empty_lines )
    # code = ''.join(non_empty_lines)
    return result_text


def extract_functions_from_code(code):
    function_dict = {}
    # 함수 이름과 본문을 찾는 정규 표현식
    pattern = re.compile(r'(\w+)\(\)\s*\{\n(.*?)\n\}', re.DOTALL)

    matches = pattern.findall(code)
    for match in matches:
        function_name = match[0]
        function_body = match[1]
        function_dict[function_name] = function_body.strip()

    return function_dict

def save_dict_to_file(file_path, dictionary):
    try:
        with open(file_path, 'w') as file:
            for key, value in dictionary.items():
                file.write(f'Function Name: {key}\n')
                file.write('Function Body:\n')
                file.write(value)
                file.write('\n\n')
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")
def save_text_to_file(file_path, text):
    try:
        with open(file_path, 'w') as file:
            file.write(text)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

# 파일 경로 입력
file_path = r'D:\1_기술혁신팀\9_SVN_DATA\4_코드리뷰점검Tool\ELEC\1_Check_Unused_Code.ctl'

# 파일 읽어서 텍스트 반환

#1. 파일 읽기 - 행 삭제
text = read_file_empry_lines(file_path)

#2. 주석 삭제
result_text = remove_comments(text)

#3. 함수 & Body 분리
func_dict = extract_functions_from_code(result_text)
save_dict_to_file("result_text_dict.txt", func_dict)

# save_text = "[Before]\n" + text + "\n[After]\n" + result_text

# save_text_to_file("result_text.txt", func_dict)
#2. 주석 제거
# print("test1", result_text)
# print(text.replace('\n', '\\n'))
# print(repr(text))
#
# for line in text.splitlines():
#     print(line + '\\n')
# text = remove_comments(text)
# print("test2", text)

#1. 개행 문자 제거
#2. 함수와 Body -> Dictionary 저장
#3.