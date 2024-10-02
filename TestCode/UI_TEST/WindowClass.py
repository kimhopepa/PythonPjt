from PyQt6.QtWidgets import QApplication, QTableWidget, QMainWindow, QTableWidgetItem
from PyQt6.QtGui import QColor, QFontDatabase  # QFontDatabase를 추가로 불러옵니다.
from PyQt6.QtCore import Qt
import sys
from qt_material import apply_stylesheet  # PyQt6을 불러온 후에 import 합니다.

class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Table Example")
        self.setGeometry(100, 100, 600, 400)

        # QTableWidget 생성
        self.tableWidget = QTableWidget(5, 3, self)
        self.tableWidget.setGeometry(50, 50, 500, 300)

        # 테이블에 데이터 추가
        self.load_data()

    def load_data(self):
        data = [["ok", "ng", "ok"], ["ng", "ok", "ng"], ["ok", "ng", "ok"], ["ok", "ok", "ng"], ["ng", "ok", "ok"]]
        for row in range(len(data)):
            for col in range(len(data[row])):
                item = QTableWidgetItem(data[row][col])

                # "ng" 텍스트일 경우 배경색 변경
                if "ng" in item.text():
                    item.setData(Qt.ItemDataRole.BackgroundRole, QColor('#FF5B36'))  # 수동으로 배경색 설정
                else:
                    item.setData(Qt.ItemDataRole.BackgroundRole, QColor('#4097ED'))

                self.tableWidget.setItem(row, col, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # qt_material 테마 적용 전에 PyQt6 모듈을 불러옵니다.
    QFontDatabase.addApplicationFont(':/fonts/Roboto-Regular.ttf')  # 원하는 폰트를 불러옵니다.

    # qt_material 테마 적용
    apply_stylesheet(app, theme='light_pink_500.xml')

    # 추가 스타일 설정 (예시)
    # app.setStyleSheet("""
    #     QTableWidget::item {
    #         background-color: transparent;
    #     }
    # """)

    # WindowClass의 인스턴스 생성 및 보여주기
    myWindow = WindowClass()
    myWindow.show()

    # 프로그램을 이벤트 루프로 진입시키는 코드
    app.exec()
