# 패키지 선언
import numpy as np
import matplotlib.pyplot as plt

# 파이썬 실시간 그래프 그리기
x = 0
for i in range(1000):
    x = x + 0.1
    y = np.sin(x)

    plt.scatter(x, y)
    plt.pause(1)

plt.show()