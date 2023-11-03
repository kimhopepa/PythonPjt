import matplotlib.pyplot as plt

print("start")

# x,y 축 리스트 저장
x = [1, 2, 3, 4, 5]
y = [6, 7, 8, 9, 10]


# matplotlib의 plot() 함수를 사용하여 차트를 생성합니다.
plt.plot(x, y)

# 차트의 제목과 축을 설정합니다.
plt.title("Line Graph")
plt.xlabel("x")
plt.ylabel("y")

# 차트를 표시합니다.
plt.show()

print("end")

