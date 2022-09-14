import time

#1. 파일 읽기
import timeit

f = open('examples/lorem.txt', 'r')

#2-1.
#2-1.전체 읽기
# str_text = f.read()
#2-2. 한행 읽기
# str_text = f.readline()
#2-3 개행 문자 포함하여 리스트로 저장
# str_text = f.readlines()
# print(str_text)
# count = 0
# for word in str_text :
#     count = count + 1
#     print(count, word)

#2-4 file 객체로 사용
print(f, type(f))
for line in f :
    print(line)

print("timer")
time.sleep(10)

f.close()

with open('examples/lorem.txt', 'r') as f :
    print(f.readlines())


