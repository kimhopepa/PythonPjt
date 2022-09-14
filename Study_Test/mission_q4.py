
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
# count_prime_number(5, 100)