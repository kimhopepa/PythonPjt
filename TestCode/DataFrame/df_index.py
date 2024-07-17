import pandas as pd
COL_CR_ITEM = '코드 리뷰 항목'
COL_CR_RESULT = '코드 리뷰 결과'

ROW_CR_RESULT_OK = 'OK'
ROW_CR_RESULT_NG = 'NG'
ROW_CR_RESULT_NONE = 'N/A'
COL_CR_LINE = 'Line'
COL_CR_RESULT_DETAIL = '상세 내용'

# 샘플 DataFrame 생성
df = pd.DataFrame({
    '분류': ['성능', '성능', 'DB', 'DB', '코드 표준', '코드 표준'],
    COL_CR_ITEM: ['적절한 DP 처리 함수', 'Loop문 내 처리 조건', 'DB Query 바인딩 처리', 'Query 주석 작성', '스크립트 이력 관리', '하드 코딩 지양'],
    COL_CR_RESULT: [ROW_CR_RESULT_NONE, ROW_CR_RESULT_NONE, ROW_CR_RESULT_NONE, ROW_CR_RESULT_NONE, ROW_CR_RESULT_NONE, ROW_CR_RESULT_NONE],
    COL_CR_LINE: ["", "", "", "", "", ""],
    COL_CR_RESULT_DETAIL: ["", "", "", "", "", ""]
})

# 1) 'A' 열에서 값이 3인 행의 인덱스 찾기
item_index = df.index[df['코드 리뷰 항목'] == 'DB Query 바인딩 처리'].tolist()[0]

print("item index = " + str(item_index))


# 2) 'A' 열에서 값이 3인 행을 가져오기 & 가져오고 삭제
row_A3 = df.loc[df[COL_CR_ITEM] == 'DB Query 바인딩 처리']
new_row = row_A3.copy()
# df = df.drop(index=item_index)
df = df.loc[df[COL_CR_ITEM] != 'DB Query 바인딩 처리']

# 인덱스를 초기화
df.reset_index(drop=True, inplace=True)
# print(df)
# print(new_row)
# exit()
#
#
# row_A3.loc[row_A3['코드 리뷰 항목'] == 'DB Query 바인딩 처리', '코드 리뷰 결과'] = 'Error1111'
# row_A3.loc[:, '코드 리뷰 결과'] = 'Error'
coding_result = [[10, "delay 처리 누락"],
[50, "delay 처리 누락2"],
[60, "delay 처리 누락2"]
]
total_result = []
total_result = coding_result + coding_result
# total_result.append(coding_result)
print(total_result)
exit()

def update_check_result(review_item : str, review_result : list, df : pd.DataFrame) :
    item_index = 0    
    if len(review_result) == 0 :
        df.loc[df[COL_CR_ITEM] == review_item, COL_CR_RESULT] = ROW_CR_RESULT_OK
    else :
        select_row = df.loc[df[COL_CR_ITEM] == review_item]
        item_index = df.index[df[COL_CR_ITEM] == review_item].tolist()[0] + 1
        df = df.loc[df[COL_CR_ITEM] != review_item]

        # Error List를 Dataframe에 저장
        for item in review_result :
            new_row = select_row.copy()
            new_row.loc[:, COL_CR_RESULT] = ROW_CR_RESULT_NG
            new_row.loc[:, COL_CR_LINE] = item[0]
            new_row.loc[:, COL_CR_RESULT_DETAIL] = item[1]
            # 상위 부분, 새로운 행, 하위 부분 결합
            upper_half = df.iloc[:item_index + 1]
            lower_half = df.iloc[item_index + 1:]
            df = pd.concat([upper_half, new_row, lower_half]).reset_index(drop=True)
            item_index = item_index + 1

    return df

df = update_check_result('Loop문 내 처리 조건', coding_result, df)
print(df)
exit()
def insert_row_at_index(df, row, index):
    index = index - 1
    if isinstance(row, dict):
        row = pd.DataFrame([row])
    elif isinstance(row, pd.Series):
        row = row.to_frame().T

    # 상위 부분, 새로운 행, 하위 부분 결합
    upper_half = df.iloc[:index + 1]
    lower_half = df.iloc[index + 1:]
    new_df = pd.concat([upper_half, row, lower_half]).reset_index(drop=True)

    return new_df

# print(row_A3, index)
df = insert_row_at_index(df, row_A3, index_A3[0]-1)
# df = insert_row_at_index(df, row_A3, index_A3[0]-1)
# df = insert_row_at_index(df, row_A3, index_A3[0]-1)
print(df)
