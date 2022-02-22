from dialog_result import *
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget
from PyQt5.QtCore import Qt
import sys


class form(QWidget, Ui_dialog_ans):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.center()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.buton_ok.clicked.connect(self.close)

    def center(self):
        qr = self.frameGeometry()                           # 获取空间的集合内容
        cp = QDesktopWidget().availableGeometry().center()  # 计算显示器分辨率，然后得出中间点
        qr.moveCenter(cp)                                   # 移动矩阵中心到屏幕中心
        # 移动应用程序窗口的左上角到qr矩形的左上角，从而使应用程序窗口显示在屏幕的中心。
        self.move(qr.topLeft())


def show_dialog():
    app = QApplication(sys.argv)
    dialog = form()
    dialog.show()
    app.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = form()
    dialog.show()
    sys.exit(app.exec_())