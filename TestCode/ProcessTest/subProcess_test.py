import subprocess

# tasklist 명령어 실행
tasklist_output = subprocess.check_output(["tasklist"]).decode("cp949")

# 결과 출력
print(tasklist_output)