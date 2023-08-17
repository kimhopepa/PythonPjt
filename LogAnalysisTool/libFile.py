import configparser
# from time import strftime
import os
import pandas as pd
import datetime


# ConfigParser 클래스
# from attr import _config


class FileManager:
    def __init__(self):
        print("FileManager Start")

    def GetFileList(self, file_path):
        fileinfo_dict = {}

        try:
            # print("o_path", file_path)
            for path, dir, files in os.walk(file_path):
                for file in files :
                    if "progs" == file :
                        path = path.replace('\\', '/')
                        server_name = self.getServerName (path)
                        fileinfo_dict[server_name] = path + "/" + file

        except Exception as e:
            print("GetFileList()", e)

        return fileinfo_dict

    def getServerName(self, path):
        try:
            svr_name = ""
            filter_name = "SVR"
            folder_list = path.split('/')

            for name in folder_list :
                index = name.find(filter_name)
                if index >= 0 :
                    svr_name = name
                    break

        except Exception as e:
            print("getServerName()", e)

        return svr_name

    def progs_save(self, file_info, folder_path):
        try:
            col_Server = "Server"
            col_Script = "Script"
            columns = [col_Server, col_Script]
            df = pd.DataFrame(columns=columns)

            for server_name, progs_path in file_info.items():
                with open(progs_path, 'r') as file :
                    file_text = file.readlines()

                for line in file_text :
                    if line.find("WCCOActrl") >= 0 and line.find(".ctl") >= 0 :
                        text_list = line.split(" ")
                        script_name = text_list[len(text_list) - 1].replace("\n", "")
                        new_row = {col_Server : server_name, col_Script : script_name}

                        df = df._append(new_row, ignore_index = True)
            csv_file_name = folder_path + "/output_summery_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")+ ".csv"
            df.to_csv(csv_file_name)
        except Exception as e:
            print("progs_save()", e)

