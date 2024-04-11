
import os
import glob
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

def get_Winccoa_version(path):
    Woa_Version = []
    Woa_Patch = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            Woa_Version.append(item)
            version_path = get_first_file_sorted_by_pattern_desc(path + "\\" + item,"ReadmeP*.txt" )
            Woa_Patch.append(version_path)

    data = {'WinCC OA 버전': Woa_Version, 'Patch': Woa_Patch}
    df = pd.DataFrame(data)
    return df

def get_first_file_sorted_by_pattern_desc(path, pattern):
    files = glob.glob(os.path.join(path, pattern))
    # 파일 이름을 내림차순으로 정렬합니다.
    files.sort(reverse=True)
    # 정렬된 파일 중에서 첫 번째 파일의 이름을 가져옵니다.
    if files:
        return os.path.basename(files[0])
    else:
        return None