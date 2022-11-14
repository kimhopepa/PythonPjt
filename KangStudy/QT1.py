# pyi-makespec --noconsole --onefile QT.py
# pyinstaller QT.spec
# 실행파일 만들기 : Python 파일이 있는 폴더로 이동한 다음, 아래 명령어를 입력하면 해당 폴더에 실행파일이 만들어집니다.
# pyinstaller QT.py
# 콘솔창 없이 실행파일 하나만
# pyinstaller -w -F QT.py
# pyinstaller -w --onefile QT.py
# 수정된 스팩파일 빌드 pyinstaller QT.spec

#1) 라이브러리 import
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtWidgets
import sys
import os
import NaverCrawling as crawler

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

#2) UI 파일 연결 -> 같은 경로에 위치
form = resource_path("NaverCrawling.ui")
form_class = uic.loadUiType(form)[0]


#3) 화면을 띄우는 클래스 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.lineEdit_ID.setPlaceholderText("Enter ID Here")
        self.lineEdit_PWD.setPlaceholderText("Enter Password Here")
        self.lineEdit_PWD.setEchoMode(QtWidgets.QLineEdit.Password)

    # 버튼 이벤트
        self.btn_login.clicked.connect(self.button2Function)
        self.btn_hankuk.clicked.connect(self.button1Function)
        self.btn_meil.clicked.connect(self.button1Function)

    # LineEdit과 관련된 버튼에 기능 연결
        id = self.lineEdit_ID.text()
        pwd = self.lineEdit_PWD.text()

    # TableWidget에 크롤링 내용 연동하기

        for row,title,url in zip(range(10), crawler.title_list, crawler.url_list):
            self.tableWidget_contents.setItem(row, 0, QTableWidgetItem(title))
            self.tableWidget_contents.setItem(row, 1, QTableWidgetItem(url))


#btn_1이 눌리면 작동할 함수
    def button1Function(self) :
        print("btn Clicked")
#btn_2가 눌리면 작동할 함수
    def button2Function(self) :
        print("btn Clicked")
        print(self.lineEdit_ID.text()) # Lineedit에 있는 글자를 가져오는 메서드
        print(self.lineEdit_PWD.text())




#4) 위에서 선언한 클래스를 실행 : QMainWindow 부모 클래스의 show 함수 실행
if __name__ == '__main__':
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    # pw = QtGui.QLineEdit()
    # pw.setEchoMode(QtGui.QLineEdit.Password)
    # pw.show()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    # QtWidgets모듈에 QApplication클래스가 정의되어 있음
    app.exec_()