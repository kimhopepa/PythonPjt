import pandas as pd

# 예시 DataFrame 생성
data = {
    'file_name': ['ACB_ATO_CNT.pnl', 'crc_test_variable_notused.ctl', 'Emergency_Blackout.ctl',
                  'SYM_ATO_ACB - 복사본.pnl', 'SYM_ATO_ACB.pnl'],
    'file_path': ['D:/1_기술혁신팀/9_SVN_DATA/4_코드리뷰점검Tool/ELEC/ACB_ATO_CNT.pnl',
                  'D:/1_기술혁신팀/9_SVN_DATA/4_코드리뷰점검Tool/ELEC/crc_test_variable_notused.ctl',
                  'D:/1_기술혁신팀/9_SVN_DATA/4_코드리뷰점검Tool/ELEC/Emergency_Blackout.ctl',
                  'D:/1_기술혁신팀/9_SVN_DATA/4_코드리뷰점검Tool/ELEC/SYM_ATO_ACB - 복사본.pnl',
                  'D:/1_기술혁신팀/9_SVN_DATA/4_코드리뷰점검Tool/ELEC/SYM_ATO_ACB.pnl']
}
df = pd.DataFrame(data)

# 파일 이름으로 파일 경로를 가져오는 함수
def get_file_path(file_name):
    file_path = df[df['file_name'] == file_name]['file_path'].iloc[0]
    return file_path if not pd.isnull(file_path) else "File not found"

print("test", (df[df['file_name'] == 'ACB_ATO_CNT.pnl']['file_path']).to_string())