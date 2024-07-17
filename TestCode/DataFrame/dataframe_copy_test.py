import pandas as pd

# 샘플 DataFrame 생성
data = {
    'Name': ['Alice', 'Bob', 'Alice', 'David', 'Bob', 'Eve'],
    'Age': [25, 30, 25, 35, 30, 28],
    'City': ['New York', 'Los Angeles', 'New York2', 'Chicago', 'Los Angeles', 'Miami']
}
df = pd.DataFrame(data)

print("Original DataFrame:")
print(df)

# 중복된 'Name' 컬럼 값 제거
df_unique = df.drop_duplicates(subset='Name', keep='first')

print("\nDataFrame with unique 'Name' values:")
print(df_unique)
