# number = int(input("몇 단? : "))
# x = 1
#
# def gugudan(number):
#     for x in range(100):
#         x += 1
#         result = number * x
#         if x % 2 != 1 or result > 50:
#             pass
#         else:
#             print("{} X {} = {}".format(number, x, result))
#     return
#
# gugudan(number)


# n = int(input("첫 번째 수 입력 : "))
# m = int(input("두 번째 수 입력 : "))
# numbers = [ 2*i for i in range(n,(m//2+1))]  # 2의 배수로 구성
# mid = numbers[len(numbers)//2 ]   #중앙값
#
# if len(numbers) % 2 == 1:  #리스트안 요소들의 개수가 홀수일 경우
#     print("{}과 {} 사이의 중앙값은 {} 입니다.".format(n, m, mid))
# else: #개수가 짝수인 경우 중앙값을 구하지 않음
#     print("중앙값이 없습니다.")
#
# print(numbers, "개수 : ", len(numbers))

# Q1
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
