

#1) 라이브러리 import
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import os
from ConfigManager import ConfigClass
from CrawlManager import CrawlClass

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

#2) UI 파일 연결 -> 같은 경로에 위치
form = resource_path("NaverCrawlUI.ui")
form_class = uic.loadUiType(form)[0]


#3) 화면을 띄우는 클래스 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        
        #1. UI 이벤트 초기화
        self.setupUi(self)
        self.pushButton_Connect.clicked.connect(self.btn_Login)
        self.pushButton_Search.clicked.connect(self.btn_Search)
        self.pushButton_Move.clicked.connect(self.btn_Move)

        #2. 클래스 초기화
        self._config = ConfigClass()
        self._crawl = CrawlClass()
        self.loadConfig()

    def loadConfig(self):
        try:
            config_site = self._config.GetConfigData(self._config.section_main, self._config.key_site)
            config_id = self._config.GetConfigData(self._config.section_main, self._config.key_id)
            config_pw = self._config.GetConfigData(self._config.section_main, self._config.key_pw)
            config_move_url = self._config.GetConfigData(self._config.section_main, self._config.key_move_url)

            self.lineEdit_SITE.setText(config_site)
            self.lineEdit_ID.setText(config_id)
            self.lineEdit_PW.setText(config_pw)
            self.lineEdit_URL.setText(config_move_url)

            print(config_site, config_id, config_pw, config_move_url)




        except Exception as e:
            print("loadConfig()", e)

    def btn_Login(self):
        # 로그인 버튼 선택
        try :
            site = self.lineEdit_SITE.text()
            id_text = self.lineEdit_ID.text()
            pw = self.lineEdit_PW.text()
            msg_info = "site = {0}, id = {1}, pw = xxxx".format(site, id_text, pw)
            QMessageBox.about(self, "message", msg_info)

            self._config.SaveConfig(self._config.section_main, self._config.key_site, site)
            self._config.SaveConfig(self._config.section_main, self._config.key_id, id_text)
            self._config.SaveConfig(self._config.section_main, self._config.key_pw, pw)

            self._config.WriteConfig()

            self._crawl.initialize(site, id_text, pw)
        except Exception as e:
            print("btn_Login()", e)

    def btn_Search(self):
        try:

            news_url = "https://media.naver.com/press/015?sid=101"

            url_list, title_list = self._crawl.search(news_url)
            crawl_cnt = len(url_list)
            print("url_list", url_list)
            print("title_list", title_list)
            self.tableWidget.setRowCount(crawl_cnt)
            # self.tableWidget.setColumnCount(2)

            for i in range(crawl_cnt):
                self.tableWidget.setItem(i, 0, QTableWidgetItem(title_list[i]))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(url_list[i]))

        except Exception as e:
            print("btn_Search()", e)

    def btn_Move(self):
        try:
            input_url = self.lineEdit_URL.text()
            self._crawl.move(input_url)
            self._config.SaveConfig(self._config.section_main, self._config.key_move_url, input_url)

            self._config.WriteConfig()

        except Exception as e:
            print("btn_Search()", e)
#4) 위에서 선언한 클래스를 실행 : QMainWindow 부모 클래스의 show 함수 실행
if __name__ == '__main__':
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

