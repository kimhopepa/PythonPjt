import py61850
import time

# 서버 초기화
server = py61850.Server()

# 서버의 논리 장치 및 논리 노드 생성
ld = server.add_logical_device('LD0')
ln = ld.add_logical_node('LLN0')

# 데이터 객체 추가 (예: 상태 값)
status = ln.add_data_object('Status', py61850.DataTypeEnum.BOOLEAN)
status.value = False

# 서버 시작
server.start()

print("IEC 61850 서버가 시작되었습니다.")

try:
    while True:
        # 상태 값을 주기적으로 변경
        status.value = not status.value
        time.sleep(5)
except KeyboardInterrupt:
    # 서버 종료
    server.stop()
    print("IEC 61850 서버가 종료되었습니다.")