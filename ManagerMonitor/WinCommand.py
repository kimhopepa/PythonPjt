import os
import pandas as pd
import re
import datetime
import threading
import time
import traceback

class WinCommand:
    _command_process = "wmic process where \"name like 'WCC%'\" get commandline, name, parentprocessid, processid, WorkingSetSize"
    _df_process_info = None
    _df_win32_info = None
    _df_total_info = None
    _thread_flag = True
    _thread = None
    _pjt_list = None

    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self._thread = threading.Thread(target=self.initThread)
        self._thread.start()

    def initThread(self):
        while self._thread_flag:
            try:
                # 1. commad 결과 저장 : _df_process_info, _df_win32_info
                t_start = datetime.datetime.now()
                self.processCommand()
                self.win32Command()
                self._df_total_info = pd.merge(self._df_process_info, self._df_win32_info, left_on='PID',
                                               right_on='PID', how='inner')
                t_end = datetime.datetime.now()

                # 2. 결과 출력
                print("WinCommand Thread period = " + str(t_end - t_start), t_end)

                # self._df_total_info[]
                # self._df_process_info.to_csv("_df_process_info.csv")
                # self._df_win32_info.to_csv("_df_win32_info.csv")
                self._df_total_info.to_csv("_df_total_info.csv")


            except Exception  as e:
                print("initThread except", e)
                traceback.print_exc()
            finally:
                time.sleep(1)

    # wmic Process 명령어 실행 : 프로젝트별 Manager 정보를 조회
    def processCommand(self):
        # 1. wmic prcess 명령어 실행

        command_wmic = "wmic process where \"name like 'WCC%'\" get commandline, name, parentprocessid, processid"
        command_column_list = ['commandline', 'name', 'parentprocessid', 'PID', 'MANAGER_NAME', 'PROJ']
        command_result = os.popen(command_wmic)
        command_text = command_result.read()
        command_result.close()

        # 2. Commnad 명령어 결과를 DataFrame으로 조회
        self._df_process_info = self.get_process_dataframe(command_text, command_column_list)

    # wmic Win32 명령어 실행 : PID별 CPU 부하 및 메모리 조회
    def win32Command(self):
        command_wmic = 'wmic path Win32_PerfFormattedData_PerfProc_Process where "name like \'WCC%\'" get idprocess, name,  PercentProcessorTime, workingset '
        command_column_list = ['PID', 'name', 'PercentProcessorTime', 'workingset']

        command_result = os.popen(command_wmic)
        command_text = command_result.read()
        command_result.close()

        # 2. Commnad 명령어 결과를 DataFramen으로 조회
        self._df_win32_info = self.get_win32_dataframe(command_text, command_column_list)

    # get_process_dataframe() -> command 명령어 결과를 DataFrame으로 리턴 (wmic Process)
    def get_process_dataframe(self, text, column_list):
        ser_header = pd.Series(column_list)

        df_task_info = pd.DataFrame(columns=ser_header)
        text_list = text.split('\n\n')

        for i in range(1, len(text_list)):
            # 1. cmd 결과 리스트로 분리
            result_list = self.get_process_list(text_list[i])

            # 2. CommandLine에서 PRJ 이름 분리
            if len(result_list) == (len(column_list) - 1):
                command_line = result_list[0]
                prj_name = self.get_prj_name(command_line)
                result_list.append(prj_name)
                df_task_info = df_task_info.append(pd.DataFrame([result_list], columns=ser_header), ignore_index=True)
            # else:
            #     print("ERROR", len(result_list), (len(column_list) - 1), result_list)

        return df_task_info

    # get_win32_dataframe() -> command 명령어 결과를 DataFrame으로 리턴 (wmic Win32)
    def get_win32_dataframe(self, text, column_list):
        ser_header = pd.Series(column_list)
        df_task_info = pd.DataFrame(columns=ser_header)
        text_list = text.split('\n\n')

        for i in range(1, len(text_list)):
            result_list = self.get_process_list(text_list[i], 2)

            if len(result_list) == (len(column_list)):
                #             print(" get_win32_dataframe ok", type(result_list), result_list)
                df_task_info = df_task_info.append(pd.DataFrame([result_list], columns=ser_header), ignore_index=True)
            # else:
            #     print(" get_win32_dataframe NG", type(result_list), result_list)

        return df_task_info

    # get_process_list() -> text 정보를 리스트로 변환 (command_list_result)
    def get_process_list(self, in_text, MODE=1):
        command_list = []

        # 1. 패턴으로 Name 정보 위치 확인
        pattern_text = r' WCC.*exe'
        pattern_regex = re.compile(pattern_text)
        pattern_match = pattern_regex.search(in_text)

        # 2. command line 정보 저장
        if pattern_match:
            name_idx = pattern_match.start()
            commandline_text = in_text[:name_idx].strip()
            #         print("pattern correct", type(in_text), type(command_list), name_idx)
            command_list.append(commandline_text)  # 명령줄 저장
            tmp_list = in_text[name_idx:].split()  # Name, ParrentPID, PID 저장
            command_list.extend(tmp_list)

            if tmp_list[0] == "WCCOActrl.exe":
                ctrl_name = self.get_ctl_name(commandline_text)
            else:
                ctrl_name = tmp_list[0]

            command_list.append(ctrl_name)
        else:
            if MODE == 2:
                command_list = in_text.split()
            # else:
            #     print("pattern incorrect = ", in_text)

        return command_list

    def get_ctl_name(self, text):
        ctrl_name = ""
        text_list = text.split()
        pattern_text = r'.*ctl'
        pattern_regex = re.compile(pattern_text)
        for i in range(0, len(text_list)):
            pattern_match = pattern_regex.search(text_list[i])
            if pattern_match:
                ctrl_name = text_list[i]
        return ctrl_name

    # get_prj_name() -> command 명령줄에서 프로젝트 이름을 조회
    def get_prj_name(self, command_line_text):
        prj_name = ""
        # 1 명령줄 공백으로 리스트 변환
        command_list = command_line_text.split()

        # 2 리스트에서 "-PROJ" 항목 확인하여 프로젝트 이름 확인
        if "-PROJ" in command_list:
            prj_index = command_list.index("-PROJ") + 1
            if len(command_list) >= prj_index:
                prj_name = command_list[prj_index]

        return prj_name

    def exitThread(self):
        self._thread_flag = False
        self._thread.join()
