
def find_even_number (n, m) :
    numbers = [i for i in range(n , m+1)]
    center_count = -1

    if len(numbers) % 2 != 0 :
        center_count = round(len(numbers) / 2)

    print(numbers, center_count)
    for i in range(len(numbers)) :
        if numbers[i] % 2 == 0 :
            print("{0} 짝수".format(numbers[i]))
            if i == center_count :
                print("{0} 중앙값".format(numbers[i]))


n = int(input("첫 번째 수 입력 : "))
m = int(input("두 번째 수 입력 : "))
# find_even_number(1, 5)
# find_even_number(1, 7)
# find_even_number(1, 8)
# find_even_number(1, 9)
# find_even_number(1, 11)