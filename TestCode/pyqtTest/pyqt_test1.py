import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # QTableWidget 생성
        self.table = QTableWidget(self)
        self.table.setRowCount(4)
        self.table.setColumnCount(3)
        self.setCentralWidget(self.table)

        # 테이블 헤더 설정
        self.table.setHorizontalHeaderLabels(['Name', 'Age', 'ID'])

        # 샘플 데이터 추가
        data = [
            ('Alice', 25, 'A001'),
            ('Bob', 30, 'B002'),
            ('Charlie', 22, 'C003'),
            ('David', 28, 'D004')
        ]

        for row, (name, age, _id) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(str(age)))
            self.table.setItem(row, 2, QTableWidgetItem(_id))

        # 특정 문자를 포함한 셀을 빨간색으로 하이라이트
        self.highlight_cells('A')

    def highlight_cells(self, keyword):
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and keyword in item.text():
                    item.setBackground(QColor('red'))

# 애플리케이션 실행
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())