import os
import chardet

def check_text_in_ctl_files(folder_path, search_text):
    # os.walk를 사용해 폴더와 하위 폴더의 모든 파일을 탐색합니다.
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.ctl'):
                file_path = os.path.join(root, file)
                try:
                    # 파일을 읽기 모드로 엽니다.
                    with open(file_path, 'rb') as f:
                        raw_data = f.read()
                        result = chardet.detect(raw_data)
                        encoding = result['encoding']
                        text = raw_data.decode(encoding)

                        # 특정 텍스트가 파일 내용에 있는지 확인합니다.
                        if search_text in text:
                            print(f"'{search_text}' 텍스트가 '{file_path}' 파일에 존재합니다.")
                        # else:
                        #     print(f"'{search_text}' 텍스트가 '{file_path}' 파일에 존재하지 않습니다.")
                except Exception as e:
                    print(f"파일 '{file_path}'을(를) 읽는 도중 오류 발생: {e}")


# 예시 호출
# check_text_in_ctl_files('path_to_folder', '검색할 텍스트')


if __name__ == '__main__':
    print("start")
    # folder_path = r"D:\1_기술혁신팀\5_스크립트관리\5_11_SEC 코드 리뷰"
    folder_path = r"D:\1_기술혁신팀\9_SVN_DATA\1_표준스크립트"
    # folder_path= r"D:\1_기술혁신팀\9_SVN_DATA\1_표준스크립트\공통라이브러리\공통라이브러리_20240805"
    check_text_in_ctl_files(folder_path, "init_standard_script")
    print("end")
