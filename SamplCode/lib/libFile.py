
import os
import pandas as pd

def get_folder_file_list_dataframe(folder_path):
    file_paths = []
    file_names = []

    # 폴더 내 모든 파일의 경로와 파일 이름을 가져옵니다.
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
            file_names.append(file)

    # 파일 경로와 파일 이름을 DataFrame으로 변환합니다.
    data = {'Folder_Path': file_paths, 'File_Name': file_names}
    df = pd.DataFrame(data)
    return df