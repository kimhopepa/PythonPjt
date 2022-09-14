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
