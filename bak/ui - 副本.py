# -*-coding:utf-8-*-

'''QT重绘draw模块'''

import sys
import os
import cv2
from PyQt5.QtCore import (
    Qt,
    QRect,
)
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QDesktopWidget,
    QLabel,
    QSlider,
    QHBoxLayout,
    QVBoxLayout,
    QRadioButton,
    QComboBox,
    QPushButton
)
from PyQt5.QtGui import (
    QIcon,
    QPixmap,
    QImage,
    QFont,
)
import numpy as np
from mask import MaskContainer
from config import *

MASK_CONTAINER_PX_ADJ_NAME      = '蒙版组横坐标：'
MASK_CONTAINER_PY_ADJ_NAME      = '蒙版组纵坐标：'
MASK_CONTAINER_WIDTH_ADJ_NAME   = '蒙版组长度：  '
MASK_WIDTH_ADJ_NAME             = '蒙版长度：    '
MASK_HEIGHT_ADJ_NAME            = '蒙版高度：    '
MASK_THETA_ADJ_NAME             = '蒙版倾角：    '
MASK_COUNTS_ADJ_NAME            = '蒙版数量：    '


class UI(QWidget):
    def __init__(self):
        super(UI, self).__init__()
        self.oncreate()

    def oncreate(self):
        self.setGeometry(300,300, 
        PARKING_PART_DEFAULT_WIDTH, 
        PARKING_PART_DEFAULT_HEIGHT)

        self.tocenter()
        self.setWindowTitle(PARKING_PART_WINDOW_NAME)
        mainhbox = QVBoxLayout(self)
        
        self.imgLabel = QLabel(self)
        self.imgLabel.setFixedSize(
            PIC_DEFAULT_WIDTH, 
            PIC_DEFAULT_HEIGHT)
        self.imgLabel.move(5,5)
        self.imgLabel.setStyleSheet('QLabel{background:white;}')
        filename = str(input('图像名称: '))
        self.loadlocalimg(filename)
        
        # 创建滑动条
        # 创建蒙版组横坐标设置滑动条
        px_change_h_layout = QHBoxLayout()
        px_change_label = QLabel(self)
        px_change_label.setFont(QFont('宋体', 11))
        px_change_label.setText(MASK_CONTAINER_PX_ADJ_NAME)
        mask_container_px_slider = QSlider(Qt.Horizontal, self)
        mask_container_px_slider.setRange(0, self.imgsrc_w)
        mask_container_px_slider.setStyleSheet(
            f'QSlider{{max-width: {round(PIC_DEFAULT_WIDTH/2)}; min-width: {round(PIC_DEFAULT_WIDTH/2)};}}')
        mask_container_px_slider.valueChanged.connect(self.on_px_change)
        self.px_change_val = QLabel(self)
        self.px_change_val.setFont(QFont('宋体', 11))
        self.px_change_val.setAlignment(Qt.AlignLeft)
        self.px_change_val.setText(str('%-4d' % MASK_POS_X))
        px_change_h_layout.addWidget(px_change_label)
        px_change_h_layout.addStretch(1)
        px_change_h_layout.addWidget(mask_container_px_slider)
        px_change_h_layout.addStretch(1)
        px_change_h_layout.addWidget(self.px_change_val)
        px_change_h_layout.setGeometry(QRect(5, round(PIC_DEFAULT_HEIGHT)+30, PIC_DEFAULT_WIDTH, 20))
        
        # 蒙版组纵坐标设置滑动条
        py_change_h_layout = QHBoxLayout()
        py_change_label = QLabel(self)
        py_change_label.setFont(QFont('宋体', 11))
        py_change_label.setText(MASK_CONTAINER_PY_ADJ_NAME)
        mask_container_py_slider = QSlider(Qt.Horizontal, self)
        mask_container_py_slider.setRange(0, self.imgsrc_h)
        mask_container_py_slider.setStyleSheet(
            f'QSlider{{max-width: {round(PIC_DEFAULT_WIDTH/2)}; min-width: {round(PIC_DEFAULT_WIDTH/2)};}}')
        mask_container_py_slider.valueChanged.connect(self.on_py_change)
        self.py_change_val = QLabel(self)
        self.py_change_val.setFont(QFont('宋体', 11))
        self.py_change_val.setAlignment(Qt.AlignLeft)
        self.py_change_val.setText(str('%-4d' % MASK_POS_X))
        py_change_h_layout.addWidget(py_change_label)
        py_change_h_layout.addStretch(1)
        py_change_h_layout.addWidget(mask_container_py_slider)
        py_change_h_layout.addStretch(1)
        py_change_h_layout.addWidget(self.py_change_val)
        py_change_h_layout.setGeometry(QRect(5, round(PIC_DEFAULT_HEIGHT)+60, PIC_DEFAULT_WIDTH, 20))

        # 蒙版组宽度设置滑动条
        mp_width_change_h_layout = QHBoxLayout()
        mp_width_change_label = QLabel(self)
        mp_width_change_label.setFont(QFont('宋体', 11))
        mp_width_change_label.setText(MASK_CONTAINER_WIDTH_ADJ_NAME)
        mask_container_mp_width_slider = QSlider(Qt.Horizontal, self)
        mask_container_mp_width_slider.setRange(0, self.imgsrc_w)
        mask_container_mp_width_slider.setValue(self.imgsrc_w)
        mask_container_mp_width_slider.setStyleSheet(
            f'QSlider{{max-width: {round(PIC_DEFAULT_WIDTH/2)}; min-width: {round(PIC_DEFAULT_WIDTH/2)};}}')
        mask_container_mp_width_slider.valueChanged.connect(self.on_mp_width_change)
        self.mp_width_change_val = QLabel(self)
        self.mp_width_change_val.setFont(QFont('宋体', 11))
        self.mp_width_change_val.setAlignment(Qt.AlignLeft)
        self.mp_width_change_val.setText(str('%-4d' % 0))
        mp_width_change_h_layout.addWidget(mp_width_change_label)
        mp_width_change_h_layout.addStretch(1)
        mp_width_change_h_layout.addWidget(mask_container_mp_width_slider)
        mp_width_change_h_layout.addStretch(1)
        mp_width_change_h_layout.addWidget(self.mp_width_change_val)
        mp_width_change_h_layout.setGeometry(QRect(5, round(PIC_DEFAULT_HEIGHT)+90, PIC_DEFAULT_WIDTH, 20))

        # 蒙版宽度设置滑动条
        mask_width_change_h_layout = QHBoxLayout()
        mask_width_change_label = QLabel(self)
        mask_width_change_label.setFont(QFont('宋体', 11))
        mask_width_change_label.setText(MASK_WIDTH_ADJ_NAME)
        mask_container_mask_width_slider = QSlider(Qt.Horizontal, self)
        mask_container_mask_width_slider.setRange(MASK_DEFAULT_WIDTH, round(self.mcontainer.mpwidth/2))
        mask_container_mask_width_slider.setValue(MASK_DEFAULT_WIDTH)
        mask_container_mask_width_slider.setStyleSheet(
            f'QSlider{{max-width: {round(PIC_DEFAULT_WIDTH/2)}; min-width: {round(PIC_DEFAULT_WIDTH/2)};}}')
        mask_container_mask_width_slider.valueChanged.connect(self.on_mask_width_change)
        self.mask_width_change_val = QLabel(self)
        self.mask_width_change_val.setFont(QFont('宋体', 11))
        self.mask_width_change_val.setAlignment(Qt.AlignLeft)
        self.mask_width_change_val.setText(str('%-4d' % MASK_DEFAULT_WIDTH))
        mask_width_change_h_layout.addWidget(mask_width_change_label)
        mask_width_change_h_layout.addStretch(1)
        mask_width_change_h_layout.addWidget(mask_container_mask_width_slider)
        mask_width_change_h_layout.addStretch(1)
        mask_width_change_h_layout.addWidget(self.mask_width_change_val)
        mask_width_change_h_layout.setGeometry(QRect(5, round(PIC_DEFAULT_HEIGHT)+120, PIC_DEFAULT_WIDTH, 20))

        # 蒙版高度设置滑动条
        mask_height_change_h_layout = QHBoxLayout()
        mask_height_change_label = QLabel(self)
        mask_height_change_label.setFont(QFont('宋体', 11))
        mask_height_change_label.setText(MASK_HEIGHT_ADJ_NAME)
        mask_container_mask_height_slider = QSlider(Qt.Horizontal, self)
        mask_container_mask_height_slider.setRange(MASK_DEFAULT_HEIGHT, self.imgsrc_h)
        mask_container_mask_height_slider.setValue(MASK_DEFAULT_HEIGHT)
        mask_container_mask_height_slider.setStyleSheet(
            f'QSlider{{max-width: {round(PIC_DEFAULT_WIDTH/2)}; min-width: {round(PIC_DEFAULT_WIDTH/2)};}}')
        mask_container_mask_height_slider.valueChanged.connect(self.on_mask_height_change)
        self.mask_height_change_val = QLabel(self)
        self.mask_height_change_val.setFont(QFont('宋体', 11))
        self.mask_height_change_val.setAlignment(Qt.AlignLeft)
        self.mask_height_change_val.setText(str('%-4d' % MASK_DEFAULT_WIDTH))
        mask_height_change_h_layout.addWidget(mask_height_change_label)
        mask_height_change_h_layout.addStretch(1)
        mask_height_change_h_layout.addWidget(mask_container_mask_height_slider)
        mask_height_change_h_layout.addStretch(1)
        mask_height_change_h_layout.addWidget(self.mask_height_change_val)
        mask_height_change_h_layout.setGeometry(QRect(5, round(PIC_DEFAULT_HEIGHT)+150, PIC_DEFAULT_WIDTH, 20))

        # 蒙版组内设置滑动条
        mask_counts_change_h_layout = QHBoxLayout()
        mask_counts_change_label = QLabel(self)
        mask_counts_change_label.setFont(QFont('宋体', 11))
        mask_counts_change_label.setText(MASK_COUNTS_ADJ_NAME)
        mask_container_mask_counts_slider = QSlider(Qt.Horizontal, self)
        mask_container_mask_counts_slider.setRange(1, MASK_COUNTS)
        mask_container_mask_counts_slider.setValue(MASK_COUNTS)
        mask_container_mask_counts_slider.setStyleSheet(
            f'QSlider{{max-width: {round(PIC_DEFAULT_WIDTH/2)}; min-width: {round(PIC_DEFAULT_WIDTH/2)};}}')
        mask_container_mask_counts_slider.valueChanged.connect(self.on_mask_counts_change)
        self.mask_counts_change_val = QLabel(self)
        self.mask_counts_change_val.setFont(QFont('宋体', 11))
        self.mask_counts_change_val.setAlignment(Qt.AlignLeft)
        self.mask_counts_change_val.setText(str('%-4d' % MASK_COUNTS))
        mask_counts_change_h_layout.addWidget(mask_counts_change_label)
        mask_counts_change_h_layout.addStretch(1)
        mask_counts_change_h_layout.addWidget(mask_container_mask_counts_slider)
        mask_counts_change_h_layout.addStretch(1)
        mask_counts_change_h_layout.addWidget(self.mask_counts_change_val)
        mask_counts_change_h_layout.setGeometry(QRect(5, round(PIC_DEFAULT_HEIGHT)+180, PIC_DEFAULT_WIDTH, 20))

        # 蒙版倾角设置滑动条
        mask_theta_change_h_layout = QHBoxLayout()
        mask_theta_change_label = QLabel(self)
        mask_theta_change_label.setFont(QFont('宋体', 11))
        mask_theta_change_label.setText(MASK_THETA_ADJ_NAME)
        mask_container_mask_theta_slider = QSlider(Qt.Horizontal, self)
        mask_container_mask_theta_slider.setRange(45, 90)
        mask_container_mask_theta_slider.setValue(90)
        mask_container_mask_theta_slider.setStyleSheet(
            f'QSlider{{max-width: {round(PIC_DEFAULT_WIDTH/2)}; min-width: {round(PIC_DEFAULT_WIDTH/2)};}}')
        mask_container_mask_theta_slider.valueChanged.connect(self.on_mask_theta_change)
        self.mask_theta_change_val = QLabel(self)
        self.mask_theta_change_val.setFont(QFont('宋体', 11))
        self.mask_theta_change_val.setAlignment(Qt.AlignLeft)
        self.mask_theta_change_val.setText(str('%-4d' % 90))
        mask_theta_change_h_layout.addWidget(mask_theta_change_label)
        mask_theta_change_h_layout.addStretch(1)
        mask_theta_change_h_layout.addWidget(mask_container_mask_theta_slider)
        mask_theta_change_h_layout.addStretch(1)
        mask_theta_change_h_layout.addWidget(self.mask_theta_change_val)
        mask_theta_change_h_layout.setGeometry(QRect(5, round(PIC_DEFAULT_HEIGHT)+210, PIC_DEFAULT_WIDTH, 20))
        # 蒙版倾角类型设置
        fontsize = 8
        mask_theta_type_change_h_layout = QHBoxLayout()
        mask_theta_type_change_label = QLabel(self)
        mask_theta_type_change_label.setFont(QFont('黑体', fontsize))
        mask_theta_type_change_label.setText('蒙版倾角类型：')
        mask_theta_type_change_h_layout.addWidget(mask_theta_type_change_label)
        mask_theta_type_change_h_layout.addStretch(1)
        both = QRadioButton(self)
        both.setFont(QFont('黑体', fontsize))
        both.setText('两侧')
        both.setChecked(True)
        both.toggled.connect(lambda: self.on_mask_theta_type_change(both))
        mask_theta_type_change_h_layout.addWidget(both)
        left_side = QRadioButton(self)
        left_side.setFont(QFont('黑体', fontsize))
        left_side.setText('左侧')
        left_side.toggled.connect(lambda: self.on_mask_theta_type_change(left_side))
        mask_theta_type_change_h_layout.addWidget(left_side)
        right_side = QRadioButton(self)
        right_side.setFont(QFont('黑体', fontsize))
        right_side.setText('右侧')
        right_side.toggled.connect(lambda: self.on_mask_theta_type_change(right_side))
        mask_theta_type_change_h_layout.addWidget(right_side)
        mask_theta_type_change_h_layout.addStretch(1)
        # 需要调整的蒙版索引设置
        combox_label = QLabel(self)
        combox_label.setFont(QFont('黑体', fontsize))
        combox_label.setText(f'需要调整的蒙版[0-{self.mcontainer.counts-1}]：')
        combox = QComboBox(self)
        combox.setFont(QFont('黑体', fontsize))
        combox.addItem('全部')
        for i in range(self.mcontainer.counts):
            combox.addItem(f'蒙版{i}')
        # TODO combox connect function 
        mask_theta_type_change_h_layout.addWidget(combox_label)
        mask_theta_type_change_h_layout.addWidget(combox)
        mask_theta_type_change_h_layout.addStretch(1)
        mask_theta_type_change_h_layout.setGeometry(QRect(15, round(PIC_DEFAULT_HEIGHT)+230, round(PIC_DEFAULT_WIDTH-10), 20))

        # 确认按钮和退出按钮
        returnbtn = QPushButton('返回', self)    
        returnbtn.setFont(QFont('宋体', 11))
        returnbtn.setToolTip('返回选定车位区域的坐标')
        returnbtn.move(200, round(PIC_DEFAULT_HEIGHT)+270)
        returnbtn.clicked.connect(self.on_return_parking_coordinates)
        exitbtn = QPushButton('退出', self)
        exitbtn.setFont(QFont('宋体', 11))
        exitbtn.setToolTip('退出程序(建议在所有车位坐标获取之后)')
        exitbtn.move(240, round(PIC_DEFAULT_HEIGHT)+270)
        exitbtn.clicked.connect(self.on_exit)

    def tocenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def loadlocalimg(self, filename):
        assert isinstance(filename, str), '只接受"str"类型参数'
        assert os.path.exists(filename) and os.path.isfile(filename), '文件不存在或者是一个目录'
        assert filename.endswith(('jpg', 'jpeg', 'png', 'bmp')), '只接受常规图像数据'
        imgsrc = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
        self.do_something_2_img(imgsrc)

    def do_something_2_img(self, origin_image):
        self.imgsrc = origin_image
        if self.imgsrc.ndim == 3:
            height, width, dim = self.imgsrc.shape
        else:
            height, width = self.imgsrc.shape
        self.imgsrc_w = width
        self.imgsrc_h = height
        self.mcontainer = MaskContainer(width, height)
        # 创建显示副本
        imgcsrc = self.toPixmap(self.imgsrc, height, width, dim)
        imgcsrc = imgcsrc.scaled(self.imgLabel.width(), self.imgLabel.height())
        self.img_w_scale = width/imgcsrc.width()
        self.img_h_scale = height/imgcsrc.height()
        self.imgLabel.setPixmap(imgcsrc)

    def paint(self):
        img = self.imgsrc.copy()
        
    def toPixmap(self, img, height, width, dim):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        bytesPerLine = 3*width
        img = QImage(img.data, width, height, bytesPerLine,QImage.Format_RGB888)
        img = QPixmap.fromImage(img)
        return img 

    def on_px_change(self, val):
        '''调节蒙版框横坐标'''
        self.mcontainer.px = val
        self.px_change_val.setText(str(val))
        self.paint()

    def on_py_change(self, val):
        '''调节蒙版框纵坐标'''
        self.mcontainer.py = val
        self.py_change_val.setText(str(val))
        self.paint()

    def on_mp_width_change(self, val):
        '''设置蒙版组宽度'''
        self.mcontainer.mpwidth = val
        self.mp_width_change_val.setText(str(val))
        self.paint()

    def on_mask_width_change(self, val):
        '''设置蒙版宽度'''
        self.mcontainer.mask_width = val
        self.mask_width_change_val.setText(str(val))
        self.paint()

    def on_mask_height_change(self, val):
        '''设置蒙版高度'''
        self.mcontainer.mask_height = val
        self.mask_height_change_val.setText(str(val))
        self.paint()

    def on_mask_theta_change(self, val):
        '''设置蒙版的倾角'''
        theta = val/180 * np.pi
        self.mcontainer.theta = theta
        self.paint()

    def on_mask_counts_change(self, val):
        '''设置蒙版组内蒙版的数量'''
        if val == 0:
            return
        self.mcontainer.counts = val
        self.mask_counts_change_val.setText(str(val))
        self.paint()

    def on_mask_theta_type_change(self, btn:QRadioButton):
        '''设置蒙版倾角类型'''
        # TODO 蒙版倾角类型
        pass

    def on_return_parking_coordinates(self):
        '''返回车位区域坐标'''
        # TODO 车位坐标
        pass

    def on_exit(self):
        exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())
