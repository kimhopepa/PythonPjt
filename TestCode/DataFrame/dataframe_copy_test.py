import pandas as pd

# 샘플 DataFrame 생성
data = {
    'Name': ['Alice', 'Bob', 'Alice', 'David', 'Bob', 'Eve'],
    'Age': [25, 30, 25, 35, 30, 28],
    'City': ['New York', 'Los Angeles', 'New York2', 'Chicago', 'Los Angeles', 'Miami']
}
df = pd.DataFrame(data)

print("Original DataFrame:")
# print(df)

df["No"] = df.index + 1

# print(df)


# 중복된 'Name' 컬럼 값 제거
df_unique = df.drop_duplicates(subset='Name', keep='first').reset_index(drop=True)
df_unique.loc[:, "No"] = df_unique.index + 1

cols = ['No'] + [col for col in df_unique.columns if col != 'No']
df_unique = df_unique[cols]
#
# print("\nDataFrame with unique 'Name' values:")
print(df_unique)


