import pandas as pd

# 예제 DataFrame 생성
data = {
    'A': ['가', '나', 'ㄴ'],
    'B': [10, 20, 25, 15, 30, 22, 35, 12],
    'C': [100, 200, 250, 150, 300, 220, 350, 120]
}

df = pd.DataFrame(data)

print("Original DataFrame:")
print(df)

# 사용자 정의 정렬 순서
custom_order = [2,1,3]


# 'A' 컬럼을 사용자 정의 순서로 정렬하는 함수
def sort_by_custom_order(df, column, order):
    # Check if all values in the column are in the order list
    if not set(df[column]).issubset(order):
        raise ValueError("The DataFrame contains values that are not in the desired order list.")

    # Convert the column to a categorical type with the desired order
    df[column] = pd.Categorical(df[column], categories=order, ordered=True)

    # Sort the DataFrame by the column
    sorted_df = df.sort_values(by=column).reset_index(drop=True)

    return sorted_df


# 정렬 함수 호출
sorted_df = sort_by_custom_order(df, 'A', custom_order)

print("\nSorted DataFrame by Custom Order:")
print(sorted_df)
