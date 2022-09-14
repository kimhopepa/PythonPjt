# # Q1. 세자리마다 ,를 찍어주는 함수 만들기
# def make_comma(in_number):
#     # in_number = int(in_number)
#     result = f"{in_number:,}"
#     print(result)
#
# make_comma(1000000)

# # Q2 특정 글자가 몇 개 있는지 궁금
import pandas as pd

# a = """안녕하세요
# 반갑습니다. 파이썬 공부는 정말 재밌습니다."""
#
# with open("생성.txt", "a", encoding = "UTF-8") as file:
#     file.write(a)
#
# def count_word(a, word):
#     count_number = a.count(word)
#     return count_number
#
# print(count_word(a, "습니다"))


 # Q4. 주민번호를 입력하면 몇년 몇월 생인지 그리고 남자인지 여자인지
# 주민번호는 6자리, -로 구분 -> 만족안하면 "잘못된 번호입니다"출력
# 1,3은 남자, 2,4는 여자
# 00~21로 시작할 경우 2000년 이후 출생자인지 물어볼 것
# 3,4를 가질 수 있는 사람은 00년생 이후 출생자 밖에 없음

def check_if():
    while True:
        a = input("주민번호를 입력하세요. \na = ")
        hypen = a.find("-")
        year = a[0:2]
        month = a[2:4]

        # print(len(a), hypen)

        if len(a) != 14 or hypen == -1 or hypen != 6:  # 14자리가 아니라면 또는 하이픈이 없는 경우
            print("잘못된 번호입니다.\n올바른 번호를 넣어주세요.")

        elif len(a) == 14 and hypen == 6:  # 입력한 번호가 14자리 맞는 경우
            if int(a[0:1]) >= 0 and int(a[0:1]) <= 21:  # 00~21 사이 수로 시작하는 경우
                answer = input("2000년 이후 출생자 입니까? 맞으면 o 아니면x : ")
                print("answer = " + answer)

                if answer == "o":
                    if a[hypen+1] in [1,3]:
                        print(f"{year}년{month}월 남자")
                    elif a[hypen+1] in [2,4]:
                        print(f"{year}년{month}월 여자")

                elif answer == "x":
                    print(a, a[hypen + 1])
                    print(a[hypen + 1] in [1, 2])
                    fisrt_number = int(a[hypen + 1])
                    if fisrt_number in [1, 2]:
                        if a[hypen + 1] == 1:
                            print(f"{year}년{month}월 남자")
                        else:
                            print(f"{year}년{month}월 여자")
                    elif a[hypen + 1] not in [1, 2]:
                        print("잘못된 번호입니다. 주민번호 또는 답변을 확인하세요.")

                else:
                    print("o 또는 x로 다시 입력하세요!")

check_if()