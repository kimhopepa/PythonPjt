
import os
import pandas as pd
import glob

def get_folders(path):
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

if __name__ == '__main__':
    path = "C:\Siemens\Automation\WinCC_OA"
    print(path, get_folders(path))
# def get_folder_file_list_dataframe(folder_path) :
#     Woa_Version = []
#     Woa_Patch = []
#
#     # 폴더 내 모든 파일의 경로와 파일 이름을 가져옵니다.
#     for item in os.listdir(folder_path):
#         item_path = os.path.join(folder_path, item)
#         if os.path.isdir(item_path):
#             folders.append(item)
#         elif os.path.isfile(item_path):
#             files.append(item)
#
#     # 해당 경로의
#     data = {'WinCC OA 버전': file_paths, 'Patch': Patch}
#     df = pd.DataFrame(data)
#     return df