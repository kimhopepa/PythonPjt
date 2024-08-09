import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class TableView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Table with Scroll Example')
        self.setGeometry(100, 100, 600, 400)

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(100)  # 행의 수를 설정합니다
        self.table_widget.setColumnCount(5)  # 열의 수를 설정합니다

        # 데이터를 테이블에 추가합니다
        for row in range(100):
            for column in range(5):
                item = QTableWidgetItem(f'Cell {row+1}, {column+1}')
                self.table_widget.setItem(row, column, item)

        # QMainWindow의 중앙 위젯으로 설정
        self.setCentralWidget(self.table_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TableView()
    window.show()
    sys.exit(app.exec_())