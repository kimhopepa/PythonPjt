import os


def get_folder_size_limited_depth(folder, max_depth=3):
    total_size = 0
    base_depth = folder.rstrip(os.path.sep).count(os.path.sep)

    # 폴더 내 모든 파일과 하위 폴더를 순회
    for dirpath, dirnames, filenames in os.walk(folder):
        current_depth = dirpath.count(os.path.sep) - base_depth
        if current_depth >= max_depth:
            # 현재 깊이가 최대 깊이를 넘으면 하위 폴더 탐색 중단
            dirnames[:] = []
            continue

        for file in filenames:
            file_path = os.path.join(dirpath, file)
            try:
                # 각 파일의 크기를 가져와서 합산
                total_size += os.path.getsize(file_path)
            except OSError:
                # 파일에 접근할 수 없는 경우 예외 처리
                continue

    return total_size


# 사용 예시 (해당 디렉토리 경로를 입력하세요)
folder_path = r"D:\SIT_PROGRAM\312"
folder_size = get_folder_size_limited_depth(folder_path, max_depth=3)

print("")

# 결과 출력 (바이트 단위로 표시)
print(f"Folder size up to depth 3: {folder_size} bytes")