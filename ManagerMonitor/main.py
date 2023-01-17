import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from WinCommand import *

form_class = uic.loadUiType("ManagerMonitor.ui")[0]

class WindowClass(QMainWindow, form_class):
    _win_commnad = WinCommand()

    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        model = QStandardItemModel()
        model.appendRow(QStandardItem("test1"))
        model.appendRow(QStandardItem("test1"))
        model.appendRow(QStandardItem("test3"))
        model.appendRow(QStandardItem("test4"))
        # self.listView_Pjt = QListView(self)
        self.listView_Pjt.setModel(model)

    def closeEvent(self, e):
        print("close event")
        self._win_commnad.exitThread()



if __name__ == '__main__':
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
    # sys.exit()