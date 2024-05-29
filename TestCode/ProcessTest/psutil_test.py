# import psutil
#
# # 현재 실행 중인 프로세스 목록 가져오기
# process_list = psutil.process_iter()
#
# # 결과 출력
# for process in process_list:
#     try:
#         print(process.name(), process)
#     except psutil.AccessDenied:
#         # 접근 권한이 없는 프로세스가 있을 경우, 해당 프로세스는 무시합니다.
#         pass

import psutil

# 현재 실행 중인 프로세스 목록 가져오기
process_list = psutil.process_iter()

# 결과 출력
for process in process_list:
    try:
        cmdline = process.cmdline()
        print(f"PID: {process.pid}, Command Line: {' '.join(cmdline)}")
    except psutil.AccessDenied:
        # 접근 권한이 없는 프로세스가 있을 경우, 해당 프로세스는 무시합니다.
        pass