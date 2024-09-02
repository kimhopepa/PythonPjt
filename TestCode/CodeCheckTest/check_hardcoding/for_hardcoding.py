import re

text = "for( int i  = 1 ;  i <= 10; i++)"

# for문에서 하드 코딩으로 설정되어 있는 경우
def is_check_for_hardcoding(code : str) -> bool  :
    def is_check_number(code:str) -> bool :
        pattern = r"\b\d+(\.\d+)?\b"
        match = re.search(pattern, code)

        if match :
            return True
        else :
            return False


    result = False
    pattern =r"for\s*\(.*?\)"
    match = re.search(pattern, code)

    # text에 for문 확인
    split_list = ""
    if match :
        split_list = code.split(';')

        # for문에서 ';' 분리
        if len(split_list) == 3 :
            check_code = split_list[1]
            if is_check_number(check_code) :
                return True

    return False

if __name__ == '__main__':
    print(text, is_check_for_hardcoding(text))
    print(";" in text)
