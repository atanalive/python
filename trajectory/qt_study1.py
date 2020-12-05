import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QPixmap


# 文本显示
class Mylabel(QWidget):
    def __init__(self):
        super(Mylabel, self).__init__()
        self.show_Text()

    def show_Text(self):
        label1 = QLabel(self)
        label1.setText("<font color=yellow> 这是一个文本标签.</font>")
        label1.setTextInteractionFlags(Qt.TextSelectableByMouse)  # 让文本可被鼠标选择，便于复制
        label1.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Window, Qt.lightGray)
        label1.setPalette(palette)
        label1.setAlignment(Qt.AlignCenter)

        label2 = QLabel(self)
        label2.setText("<a href='#'>欢迎使用python GUI程序</a>")

        label3 = QLabel(self)
        label3.setAlignment(Qt.AlignCenter)
        label3.setToolTip("这是一个图片标签")
        label3.setPixmap(QPixmap(".\\alive.jpg"))

        label4 = QLabel(self)
        label4.setText("<a href='https://www.bilibili.com/video/BV1kA41177Na?p=72'>百度</a>")
        label4.setOpenExternalLinks(True)
        label4.setAlignment(Qt.AlignRight)
        label4.setToolTip("这是一个超级链接")

        vbox = QVBoxLayout()
        vbox.addWidget(label1)
        vbox.addWidget(label2)
        vbox.addWidget(label3)
        vbox.addWidget(label4)

        label2.linkHovered.connect(self.linkHovered)
        label4.linkActivated.connect(self.linkClicked)

        self.setLayout(vbox)
        self.setWindowTitle("Qlabel 控件演示")

    def linkHovered(self):
        print("hua guo le")

    def linkClicked(self):
        print("click")


if __name__ == '__main__':
    # 创建QApplication的实例
    app = QApplication(sys.argv)
    label = Mylabel()
    label.show()
    # 进入程序的主循环，并通过exit函数确保主循环安全结束
    sys.exit(app.exec_())
