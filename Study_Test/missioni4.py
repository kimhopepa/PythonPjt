# Q1. 숫자를 입력받아 3자리마다 "," 찍어주는 함수 구현
def make_comma(in_number):
    str_number = str(in_number) # 1234 -> "1234"
    comma_number = ""
    count = 1

    for i in range(len(str_number)):

        # 1. 역으로 숫자 출력 "123456" -> "654321"
        number_index = len(str_number) - count

        # 2. 숫자를 저장
        comma_number = str_number[number_index] + comma_number

        # 2. 3번째 자릿수 부터 "," 입력
        if count % 3 == 0 and count != len(str_number):
            comma_number = "," + comma_number

        count = count + 1

    print(comma_number)


make_comma(1234)
