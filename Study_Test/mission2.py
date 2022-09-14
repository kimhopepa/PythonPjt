#가위바위보
import random
def rsp_game(my_rsp):
    game_result = ""
    if ((my_rsp == "가위" or my_rsp =="바위" or my_rsp == "보") == False) :
        print("잘못 입력하였습니다. 입력 = " + my_rsp)
        return
    #1. 컴퓨터 가위,바위,보 입력
    computer_rsp = random.randint(0,2)
    if computer_rsp == 0 :
        computer_rsp = "가위"
    elif computer_rsp == 1 :
        computer_rsp = "바위"
    else :
        computer_rsp = "보"
    #2. 컴퓨터 vs 나 비교
    if my_rsp == "가위":
        if computer_rsp == "가위" :
            game_result = "무승부입니다."
        elif computer_rsp == "바위" :
            game_result = "컴퓨터 승리!"
        else :
            game_result = "나의 승리!"
    elif my_rsp == "바위":
        if computer_rsp == "가위" :
            game_result = "나의 승리!"
        elif computer_rsp == "바위" :
            game_result = "무승부입니다."
        else :
            game_result = "컴퓨터 승리!"
    # my_rsp == "보"
    else :
        if computer_rsp == "가위" :
            game_result = "컴퓨터 승리!"
        elif computer_rsp == "바위" :
            game_result = "나의 승리!"
        else :
            game_result = "무승부입니다."
    #3. 게임 결과 출력
    print("나 = " + my_rsp + ", 컴퓨터 = " + computer_rsp)
    print("결과는 " + game_result)

print("게임을 시작합니다.")
my_rsp = input("가위 바위 보 \n")
rsp_game(my_rsp)