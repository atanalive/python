#!/usr/bin/python
# _*_ coding:utf-8 _*_

''' made by Alive V2.0  2020/11/14
'''

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QLabel, QApplication, QInputDialog, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPixmap, QPainter, QPen, QPalette
import numpy as np
import matplotlib.pyplot as plt


class Mywindow(QWidget):
    def __init__(self):
        super(Mywindow, self).__init__()
        # 变量区
        self.mode = 2
        # mode 1
        self.coordinate = []
        # mode 2
        self.coordinate_x = []
        self.coordinate_y = []
        # 方法区
        self.SetButton()
        self.Set_TextBox()
        self.Set_Image()
        self.show_author()

    # 设置按钮
    def SetButton(self):
        # 窗口
        self.resize(1200, 900)
        self.setWindowTitle("Trajectory_tool")
        # 设置窗口颜色
        self.palette = QPalette()
        self.palette.setColor(QPalette.Window, QColor(225, 255, 255))
        self.setPalette(self.palette)

        # 切换显示按钮
        self.button_change = QPushButton(self)
        self.button_change.setText("Mode")
        self.button_change.setGeometry(QtCore.QRect(920, 670, 120, 60))
        self.button_change.clicked.connect(self.set_mode)
        # 生成坐标按钮
        self.button_create = QPushButton(self)
        self.button_create.setText("Coordinate")
        self.button_create.setGeometry(QtCore.QRect(1060, 670, 120, 60))
        self.button_create.clicked.connect(self.get_coordinate)
        # 清除坐标按钮
        self.button_clear = QPushButton(self)
        self.button_clear.setText("Clear")
        self.button_clear.setGeometry(QtCore.QRect(920, 750, 120, 60))
        self.button_clear.clicked.connect(self.clear_the_box)
        # 分析轨迹规划按钮
        self.button_graph = QPushButton(self)
        self.button_graph.setText("Graph")
        self.button_graph.setGeometry(QtCore.QRect(1060, 750, 120, 60))
        self.button_graph.clicked.connect(self.graph)
        # 选择轨迹规划算法
        self.button_algorithm = QPushButton(self)
        self.button_algorithm.setText("algorithm")
        self.button_algorithm.setGeometry(QtCore.QRect(920, 830, 120, 60))
        self.button_algorithm.clicked.connect(self.select_algorithm)
        # 设置0点按钮
        self.button_setzero = QPushButton(self)
        self.button_setzero.setText("Set_Zero")
        self.button_setzero.setGeometry(QtCore.QRect(1060, 830, 120, 60))
        self.button_setzero.clicked.connect(self.set_zero)

    def get_coordinate(self):
        if self.mode == 1:
            self.textbox.setPlainText(f"\tmode1\nget the coordinate is:\n{self.coordinate}")
        if self.mode == 2:
            self.textbox.setPlainText(f"\tmode2\nget the coordiante_x is:\n{self.coordinate_x}\n"
                                      f"get the coordiante_y is:\n{self.coordinate_y}")
        self.update()

    def set_mode(self):
        if self.mode == 1:
            self.mode = 2
        elif self.mode == 2:
            self.mode = 1
        self.get_coordinate()

    def clear_the_box(self):
        self.textbox.setPlainText("")
        self.coordinate.clear()
        self.coordinate_x.clear()
        self.coordinate_y.clear()
        self.label.draw_coordinate.clear()
        self.label.draw_B_splines.clear()
        self.update()

    def graph(self):
        t_total, flag = QInputDialog.getDouble(self, "please input time", '请输入需要的时间(/s):', 1.0, decimals=2, min=0.01)
        if t_total != 0:
            self.B_splines(t_total)

    def set_zero(self):
        # 添加初始点
        self.add_point(450 / 12, 900 - 450 / 12)

    def select_algorithm(self):
        items = ["三次B样条", "贝塞尔"]
        item, ok = QInputDialog.getItem(self, "select used argorithm", "选择算法", items, 0)
        if item == items[0]:
            QMessageBox.information(self, "信息提示", "您已经使用了B_splines算法")
        elif item == items[1]:
            QMessageBox.information(self, "信息提示", "开发者有点懒，没有写Bezier算法")

    # 文本框
    def Set_TextBox(self):
        # 设置文本
        self.font = QFont()
        self.font.setPointSize(10)
        # 设置颜色
        self.text_color = QColor()
        self.text_color.setRgb(30, 144, 255)
        # 设置文本框
        self.textbox = QTextEdit(self)
        self.textbox.setFont(self.font)
        self.textbox.move(925, 150)
        self.textbox.resize(250, 500)
        # 设置样式
        self.textbox.setStyleSheet("background: #F0FFFF")
        self.textbox.setTextColor(self.text_color)

    def Set_Image(self):
        self.label = MyLabel(self)
        # 将鼠标变成十字
        self.label.setCursor(Qt.CrossCursor)
        # 显示图片
        self.label.setPixmap(QPixmap(".\\robocon.jpg"))

    def mousePressEvent(self, event):
        # self.setMouseTracking(True)
        if event.buttons() == Qt.LeftButton:
            self.pos = event.windowPos()
            # 只取图片上的点
            if self.pos.x() < 900 and self.pos.x() > 0 and self.pos.y() < 900 and self.pos.y() > 0:
                self.add_point(self.pos.x(), self.pos.y())

    def add_point(self, x_pic, y_pic):
        x = x_pic
        y = (900 - y_pic)
        x *= 12 / 9
        y *= 12 / 9
        x -= 50
        y -= 50
        x = round(x, 2)
        y = round(y, 2)
        # mode1
        self.coordinate.append((x, y))
        # mode2
        self.coordinate_x.append(x)
        self.coordinate_y.append(y)
        # 画图点保存
        self.label.draw_coordinate.append((x_pic, y_pic))
        self.update()

    def show_author(self):
        self.name = QLabel(self)
        self.name.setFont(QFont('swscrpc', 30))
        self.name.setText("<font color=#1E90FF>Alive V2.0</font>")
        self.name.move(940, 40)

    # 将实际坐标转换成图片坐标并绘制
    def draw_in_pic(self, *input):
        x = np.array(input[0]) * 100
        y = np.array(input[1]) * 100
        x += 50
        y += 50
        x *= 9 / 12
        y *= 9 / 12
        y = 900 - y
        x = x.tolist()
        y = y.tolist()
        self.label.draw_B_splines = [(m, n) for m, n in zip(x, y)]

    def B_splines(self, t_total):
        # 计算一个维度的数据
        x, x_v, x_a = self.cal_B_splines(t_total, self.coordinate_x)
        y, y_v, y_a = self.cal_B_splines(t_total, self.coordinate_y)
        # 合成速度和加速度
        car_v = self.composite_vector(x_v, y_v)
        car_a = self.composite_vector(x_a, y_a)
        # 把轨迹在图像上画出来
        self.draw_in_pic(x, y)
        # 函数图像绘制

        a = t_total / (len(self.coordinate_x) + 1)
        plt.style.use("ggplot")
        plt.figure()
        plt.suptitle("B_splines")

        plt.subplot(2, 2, 1)  # 1
        plt.ylabel("y(m)")
        plt.xlabel("x(m)")
        plt.plot(x, y, color="#00BFFF")  # x

        plt.subplot(2, 2, 2)  # 2
        plt.ylabel("velocity(m/s)")
        plt.plot(np.arange(0, t_total, a * 0.01), car_v, color="#00BFFF")  # v

        plt.subplot(2, 2, 3)  # 3
        plt.ylabel("acceleration(m/s^2)")
        plt.plot(np.arange(0, t_total, a * 0.01), car_a, color="#00BFFF")  # a

        plt.show()

    # 轨迹总时间 t_total ,input为轨迹坐标
    def cal_B_splines(self, t_total, *input):
        input = list(*input)
        # 得到基本属性
        length = len(input)
        a = t_total / (length + 1)
        p = input
        # p = input
        # 三次b样条曲线需要多两个点处理第一个点
        p.insert(0, input[0])
        p.insert(0, input[0])
        p.append(input[-1])
        p.append(input[-1])

        # x 坐标
        x = []
        x_v = []
        x_a = []
        for i in range(0, length + 1):
            for t in np.arange(1, step=0.01):
                x_pos = 1 / 6 * (1 - t) ** 3 * p[0 + i] + \
                        1 / 6 * (3 * t ** 3 - 6 * t ** 2 + 4) * p[1 + i] + \
                        1 / 6 * (-3 * t ** 3 + 3 * t ** 2 + 3 * t + 1) * p[2 + i] + \
                        1 / 6 * t ** 3 * p[3 + i]
                x.append(x_pos / 100)

                x_velocity = (-1 / 2 * (1 - t) ** 2 * p[0 + i] + \
                              1 / 2 * (3 * t ** 2 - 4 * t) * p[1 + i] + \
                              1 / 2 * (-3 * t ** 2 + 2 * t + 1) * p[2 + i] + \
                              1 / 2 * t ** 2 * p[3 + i]) * 1 / a
                x_v.append(x_velocity / 100)
                x_accelerated = ((1 - t) * p[0 + i] + \
                                 (3 * t - 2) * p[1 + i] + \
                                 (-3 * t + 1) * p[2 + i] + \
                                 t * p[3 + i]) * 1 / (a ** 2)
                x_a.append(x_accelerated / 100)
        return x, x_v, x_a

    # 合成x和y轴的向量
    def composite_vector(self, *input):
        x = np.array(input[0])
        y = np.array(input[1])
        vector = (np.sqrt(np.power(x, 2) + np.power(y, 2))).tolist()
        return vector


class MyLabel(QLabel):
    def __init__(self, parent=None):
        super(MyLabel, self).__init__(parent)
        self.draw_coordinate = []
        self.draw_B_splines = []
        self.old_x = -1
        self.old_y = -1

    def paintEvent(self, event):
        super(MyLabel, self).paintEvent(event)
        self.pen = QPainter(self)
        self.pen.begin(self)

        # 画点
        self.pen.setPen(QPen(QColor(0, 191, 255), 3))
        for x, y in self.draw_coordinate:
            self.pen.drawEllipse(x - 3, y - 3, 6, 6)
            # 画线
            if self.old_x != -1:
                self.pen.drawLine(x, y, self.old_x, self.old_y)
            self.old_x = x
            self.old_y = y
        self.old_x = -1

        # 画点
        self.pen.setPen(QPen(QColor(240, 230, 140), 2))
        for x, y in self.draw_B_splines:
            self.pen.drawEllipse(x - 1, y - 1, 2, 2)
            # 画线
            if self.old_x != -1:
                self.pen.drawLine(x, y, self.old_x, self.old_y)
            self.old_x = x
            self.old_y = y
        self.old_x = -1

        self.pen.end()

    def set_point(self, draw_coordinate):
        self.draw_coordinate = draw_coordinate


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建进程

    window = Mywindow()  # 设置按钮

    window.show()
    sys.exit(app.exec_())  # 退出程序
