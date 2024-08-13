import time
import os
import stat



# file_path = r"D:\SIT_PROGRAM\312\SVR_K1_E66M_SMART_IO\SVR_K1_E66M\log\PVSS_II.log"
# file_path = r"D:\SIT_PROGRAM\316\SVR_P2_M154_UPS\log\PVSS_II.log"
file_path = r"D:\SIT_PROGRAM\318\SVR_P3_M154\log\PVSS_II.log"





if __name__ == '__main__':
    print("File Size = " + str(os.path.getsize(file_path)/(1024 * 1024)))

    # # 파일을 읽기 전용으로 설정 (모든 사용자)
    os.chmod(file_path, stat.S_IREAD)
    # os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)  # 사용자만 읽기/쓰기 가능
    # # 파일을 읽기 전용으로 열기
    # file = open(file_path, 'r')
    # time.sleep(1000)
    # try:
    #     fcntl.flock(file, fcntl.LOCK_SH)
    #
    #     # 파일을 읽기 전용으로 사용할 수 있습니다.
    #     content = file.read()
    #     time.sleep(500)
    #     print(content)
    # finally:
    #     file.close()
    #
    # file = open(file_path, 'a')
    # try:
    #     file.write('Hello, World!')
    #     time.sleep(1000)
    # finally:
    #     file.close()
    # for i in range(1000):
    #     with open(file_path, "a") as file :
    #         print("write a ")
    #         for i in range(500):
    #             file.writelines("a\n")
    #         time.sleep(0.5)
