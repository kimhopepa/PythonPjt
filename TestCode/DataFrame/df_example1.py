import pandas as pd

# 예시 DataFrame 생성
data = {
    '이름': ['홍길동', '김철수', '이영희'],
    '나이': [25, 30, 22],
    '주소': ['서울', '부산', '대구']
}
df = pd.DataFrame(data)

# '나이' 컬럼을 첫 번째 위치로 이동
df = df[['주소', '이름', '나이']]
# column_to_move = '나이'
# new_column_order = ['나이'] + [col for col in df.columns if col != column_to_move]
# df = df[new_column_order]
#
print(df)
