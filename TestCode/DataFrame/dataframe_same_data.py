import pandas as pd

def update_cell_with_index(df: pd.DataFrame, target_column: str, condition_column: str, condition_value) -> pd.DataFrame:
    """
    DataFrame의 특정 컬럼에서 조건을 만족하는 경우에만 다른 값으로 일련 번호를 붙여 변경하는 함수.

    Parameters:
    - df: pandas DataFrame
    - target_column: 값을 변경할 컬럼 이름
    - condition_column: 조건을 확인할 컬럼 이름
    - condition_value: 조건에 맞는 값

    Returns:
    - pandas DataFrame: 값이 변경된 DataFrame
    """
    # 조건을 만족하는 인덱스를 찾기
    mask = (df[condition_column] == 'Alice') & (df[target_column] == condition_value)
    indices = df.index[mask].tolist()

    # 일련 번호를 붙여서 업데이트
    for idx, original_index in enumerate(indices):
        df.at[original_index, target_column] = f"{condition_value}({idx + 1})"

    return df

# 예제 DataFrame 생성
data = {
    'Name': ['Alice', 'Bob', 'Alice', 'David', 'Alice', 'Eve'],
    'Age': [25, 30, 25, 35, 25, 28],
    'City': ['New York', 'Los Angeles', 'New York2', 'Chicago', 'Los Angeles', 'Miami']
}
df = pd.DataFrame(data)

# Name 컬럼의 값이 'Alice'인 경우에만 Age가 25인 것을 25(1), 25(2), ...으로 변경
df = update_cell_with_index(df, target_column='Age', condition_column='Name', condition_value=25)
print(df)
