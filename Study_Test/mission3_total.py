# Q1 숫자를 입력 받고 그 숫자의 구구단을 출력하는 함수를 만들어 봅시다.
max_value = 50
def gugudan(input_number) :
    if input_number <= 0 :
        print("잘못입력하였습니다.")
        return

    print(str(input_number) + " 단")

    gugu_count = 1
    while True :
        result = input_number * gugu_count
        if gugu_count > 9 or result > 50 :
             break
        else:
            if gugu_count % 2 != 0 :
                print("{0} × {1} = {2}".format(input_number, gugu_count, result))

        gugu_count = gugu_count + 1

number = int(input("몇 단? : "))
gugudan(number)

# Q2 가위바위보 업그레이드 버젼을 함수로 만들어 봅시다. 아래와 같은 조건을 만족해 주세요.
# 가위바위보
import random


def rsp_game(my_rsp_number, game_count):
    game_result = ""
    my_rsp = ""
    my_win = False
    computer_win = False
    draw = False
    if my_rsp_number == 0:
        my_rsp = "가위"
    elif my_rsp_number == 1:
        my_rsp = "바위"
    elif my_rsp_number == 2:
        my_rsp = "보"
    else:
        print("잘못 입력하였습니다. 입력 = " + my_rsp)
        return

    # 1. 컴퓨터 가위,바위,보 입력
    computer_rsp = random.randint(0, 2)
    if computer_rsp == 0:
        computer_rsp = "가위"
    elif computer_rsp == 1:
        computer_rsp = "바위"
    else:
        computer_rsp = "보"

    # 2. 컴퓨터 vs 나 대결
    if my_rsp == "가위":
        if computer_rsp == "가위":
            game_result = "무승부입니다."
            draw = True
        elif computer_rsp == "바위":
            game_result = "컴퓨터 승리!"
            computer_win = True
        else:
            game_result = "나의 승리!"
            my_win = True

    elif my_rsp == "바위":
        if computer_rsp == "가위":
            game_result = "나의 승리!"
            my_win = True
        elif computer_rsp == "바위":
            game_result = "무승부입니다."
            draw = True
        else:
            game_result = "컴퓨터 승리!"
            computer_win = True
    # my_rsp == "보"
    else:
        if computer_rsp == "가위":
            game_result = "컴퓨터 승리!"
            computer_win = True
        elif computer_rsp == "바위":
            game_result = "나의 승리!"
            my_win = True
        else:
            game_result = "무승부입니다."
            draw = True

    # 3. 게임 결과 출력
    print("나 = " + my_rsp + ", 컴퓨터 = " + computer_rsp)
    print("{0} 째판 {1}".format(game_count, game_result))
    return my_win, draw


def rsp_advanced(games):
    count = 1
    my_win_count = 0
    draw_count = 0
    computer_win_count = 0
    for i in range(games):
        my_rsp_number = int(input("가위 바위 보 : "))
        my_win, draw = rsp_game(my_rsp_number, count)
        if draw == True:
            draw_count = draw_count + 1
            continue
        if my_win == True:
            my_win_count = my_win_count + 1
        else:
            computer_win_count = computer_win_count + 1

    print("나의 전적 : {0}승 {1}무 {2} 패".format(my_win_count, draw_count, computer_win_count))
    print("컴퓨터 전적 : {0}승 {1}무 {2} 패".format(computer_win_count, draw_count, my_win_count))


games = int(input("몇 판을 진행하시겠습니까? : "))
rsp_advanced(games)

# Q3 2개의 숫자를 입력하여 그 사이에 짝수만 출력하는 함수를 만들어 봅시다.
# 그리고 중앙값도 함께 출력 해봅시다.(단, 중앙값이 짝수가 아닐 경우에는 중앙값은 출력을 하지 않고, 짝수인 수만 출력한다)
def find_even_number (n, m) :
    numbers = [i for i in range(n , m+1)]
    center_count = -1

    if len(numbers) % 2 != 0 :
        center_count = round(len(numbers) / 2)

    for i in range(len(numbers)) :
        if numbers[i] % 2 == 0 :
            print("{0} 짝수".format(numbers[i]))
            if i == center_count :
                print("{0} 중앙값".format(numbers[i]))


n = int(input("첫 번째 수 입력 : "))
m = int(input("두 번째 수 입력 : "))
find_even_number(n,m)

# Q4  2개의 숫자를 입력하여 그 사이에 소수가 몇 개인지 출력하는 함수를 만들어 봅시다.
def count_prime_number(n, m) :
    prime_count = 0
    if n < 2 :
        n = 2
    for i in range(n,m) :
        if is_prime(i) == True :
            print("소수 ok = {0}".format(i))
            prime_count = prime_count + 1

    print("소수개수 = {0}".format(prime_count))

def is_prime(number) :
    result = True
    for i in range(2,number) :
        if number % i == 0 :
            result = False
            break

    return result


n = int(input("첫 번째 수 입력 : "))
m = int(input("두 번째 수 입력 : "))
count_prime_number(n,m)