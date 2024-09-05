import pandas as pd


def find_duplicates_with_counts(df: pd.DataFrame, column: str) -> pd.Series:
    """
    특정 컬럼에서 중복된 값과 그 빈도를 찾아 반환하는 함수.

    Parameters:
    - df: pandas DataFrame
    - column: 중복을 확인할 컬럼 이름

    Returns:
    - pd.Series: 중복된 값과 그 빈도
    """
    # 특정 컬럼에서 각 값의 빈도를 계산
    value_counts = df[column].value_counts()

    # 빈도가 1보다 큰 값만 필터링
    duplicates_with_counts = value_counts[value_counts > 1]

    return duplicates_with_counts


# 예제 DataFrame 생성
data = {
    'Class': ['A', 'A', 'B', 'B', 'A', 'C', 'B', 'C', 'C', 'A'],
    'Item': ['X', 'X', 'Y', 'Y', 'Z', 'Z', 'Y', 'X', 'Z', 'X'],
    'Result': ['Pass', 'Fail', 'Pass', 'Pass', 'Fail', 'Pass', 'Fail', 'Fail', 'Pass', 'Pass']
}

df = pd.DataFrame(data)

if __name__ == '__main__':
    duplicate_data = find_duplicates_with_counts(df, "Item")
    print(duplicate_data)

    duplicate_data = find_duplicates_with_counts(df, "Class")
    print(type(duplicate_data), duplicate_data)

    for index , value in duplicate_data.items():
        print(index, value)