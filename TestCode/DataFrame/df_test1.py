import pandas as pd

# 샘플 DataFrame 생성
df = pd.DataFrame({
    'Group': ['Mod1', "Mod1", "Mod2", "Mod2", "Mod2"],
    'A': [1, 2, 3, 4, 5],
    'Data': ["", "", "", "", ""],
    'C': [100, 200, 300, 400, 500]
})

# A가 3인  index 찾기


print("Original DataFrame:")
print(df)

# 1) C가 100인 행 복사 후 100 유지
new_row1 = df[df['C'] == 100].copy()

# 2) 복사한 행에서 A,B 값을 +1씩 변경
new_row1['A'] += 1
new_row1['B'] += 1

# 3) 복사한 행에서 A,B 값을 +2씩 변경
new_row2 = new_row1.copy()
new_row2['A'] += 2
new_row2['B'] += 2

# 4) 기존 행 삭제 후 2개 행을 DataFrame에 저장
df = df[df['C'] != 100]
df = pd.concat([df.reset_index(drop=True), new_row1, new_row2], ignore_index=True)

print("\nUpdated DataFrame:")
print(df)