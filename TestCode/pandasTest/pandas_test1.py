import pandas as pd

# 예시 데이터프레임
df = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [6, 7, 8, 9, 10], 'C': [11, 12, 13, 14, 15]})

# 5보다 큰 값을 가진 'A' 열의 값을 100으로 변경
df.loc[df['A'] == 1, 'B'] = "absc"  # 1번째 인덱스 행, 'B' 열 값을 10으로 변경
# select_rows = df.query("A == 5")
# 변경된 값을 df에 다시 삽입 (update 메서드 사용)
print(df)
# df.update(select_rows)
# print(df)