# -*-coding:utf-8-*-
'''QT重绘draw模块'''

import sys
import os
import cv2
from PyQt5.QtCore import (
    Qt,
    QRect,
)
from PyQt5.QtWidgets import (QApplication, QWidget, QDesktopWidget, QLabel,
                             QSlider, QHBoxLayout, QVBoxLayout, QRadioButton,
                             QComboBox, QPushButton, QFileDialog, QButtonGroup,
                             QMessageBox)
from PyQt5.QtGui import (
    QIcon,
    QPixmap,
    QImage,
    QFont,
)
import numpy as np
from mask import MaskContainer
from config import *

MASK_CONTAINER_PX_ADJ_NAME = '蒙版组横坐标：'
MASK_CONTAINER_PY_ADJ_NAME = '蒙版组纵坐标：'
MASK_CONTAINER_WIDTH_ADJ_NAME = '蒙版组长度：  '
MASK_WIDTH_ADJ_NAME = '蒙版长度：    '
MASK_HEIGHT_ADJ_NAME = '蒙版高度：    '
MASK_THETA_ADJ_NAME = '蒙版倾角：    '
MASK_COUNTS_ADJ_NAME = '蒙版数量：    '


class UI(QWidget):
    def __init__(self):
        super(UI, self).__init__()
        desktop = QApplication.desktop()
        rect = desktop.screenGeometry()
        self.screen_w = rect.width()
        self.screen_h = rect.height()
        global PARKING_PART_DEFAULT_HEIGHT
        global PARKING_PART_DEFAULT_WIDTH
        global PIC_DEFAULT_HEIGHT
        global PIC_DEFAULT_WIDTH
        PARKING_PART_DEFAULT_WIDTH = round(
            self.screen_w * .4
        ) if self.screen_w > PARKING_PART_DEFAULT_WIDTH else PARKING_PART_DEFAULT_WIDTH
        PARKING_PART_DEFAULT_HEIGHT = round(
            self.screen_h * .8
        ) if self.screen_h > PARKING_PART_DEFAULT_HEIGHT else PARKING_PART_DEFAULT_HEIGHT
        PIC_DEFAULT_WIDTH = PARKING_PART_DEFAULT_WIDTH - 10
        PIC_DEFAULT_HEIGHT = round(PARKING_PART_DEFAULT_HEIGHT / 2)
        self.gap = round(PARKING_PART_DEFAULT_HEIGHT / 100)
        self.totoalWidth = PARKING_PART_DEFAULT_WIDTH
        self.oncreate()

    def oncreate(self):
        self.setGeometry(300, 300, PARKING_PART_DEFAULT_WIDTH,
                         PARKING_PART_DEFAULT_HEIGHT)

        self.tocenter()
        self.setWindowTitle(PARKING_PART_WINDOW_NAME)
        mainhbox = QVBoxLayout(self)

        self.imgLabel = QLabel(self)
        self.imgLabel.setFixedSize(PIC_DEFAULT_WIDTH, PIC_DEFAULT_HEIGHT)
        self.imgLabel.move(5, 5)
        self.imgLabel.setStyleSheet('QLabel{background:white;}')

        # 创建滑动条
        # 创建蒙版组横坐标设置滑动条
        mfontsize = self.gap * 1.4
        px_change_h_layout = QHBoxLayout()
        px_change_label = QLabel(self)
        px_change_label.setFont(QFont('宋体', mfontsize))
        px_change_label.setText(MASK_CONTAINER_PX_ADJ_NAME)
        self.mask_container_px_slider = mask_container_px_slider = QSlider(
            Qt.Horizontal, self)
        mask_container_px_slider.setStyleSheet(
            f'QSlider{{max-width: {round(PIC_DEFAULT_WIDTH/2)}; min-width: {round(PIC_DEFAULT_WIDTH/2)};}}'
        )
        mask_container_px_slider.valueChanged.connect(self.on_px_change)
        self.px_change_val = QLabel(self)
        self.px_change_val.setFont(QFont('宋体', mfontsize))
        self.px_change_val.setAlignment(Qt.AlignLeft)
        self.px_change_val.setText(str('%-4d' % MASK_POS_X))
        px_change_h_layout.addWidget(px_change_label)
        px_change_h_layout.addStretch(1)
        px_change_h_layout.addWidget(mask_container_px_slider)
        px_change_h_layout.addStretch(1)
        px_change_h_layout.addWidget(self.px_change_val)
        px_change_h_layout.setGeometry(
            QRect(5, round(PIC_DEFAULT_HEIGHT + self.gap * 5),
                  PIC_DEFAULT_WIDTH, self.gap * 2))

        # 蒙版组纵坐标设置滑动条
        py_change_h_layout = QHBoxLayout()
        py_change_label = QLabel(self)
        py_change_label.setFont(QFont('宋体', mfontsize))
        py_change_label.setText(MASK_CONTAINER_PY_ADJ_NAME)
        self.mask_container_py_slider = mask_container_py_slider = QSlider(
            Qt.Horizontal, self)
        mask_container_py_slider.setStyleSheet(
            f'QSlider{{max-width: {round(PIC_DEFAULT_WIDTH/2)}; min-width: {round(PIC_DEFAULT_WIDTH/2)};}}'
        )
        mask_container_py_slider.valueChanged.connect(self.on_py_change)
        self.py_change_val = QLabel(self)
        self.py_change_val.setFont(QFont('宋体', mfontsize))
        self.py_change_val.setAlignment(Qt.AlignLeft)
        self.py_change_val.setText(str('%-4d' % MASK_POS_X))
        py_change_h_layout.addWidget(py_change_label)
        py_change_h_layout.addStretch(1)
        py_change_h_layout.addWidget(mask_container_py_slider)
        py_change_h_layout.addStretch(1)
        py_change_h_layout.addWidget(self.py_change_val)
        py_change_h_layout.setGeometry(
            QRect(5, round(PIC_DEFAULT_HEIGHT + self.gap * 10),
                  PIC_DEFAULT_WIDTH, self.gap * 2))

        # 蒙版组宽度设置滑动条
        mp_width_change_h_layout = QHBoxLayout()
        mp_width_change_label = QLabel(self)
        mp_width_change_label.setFont(QFont('宋体', mfontsize))
        mp_width_change_label.setText(MASK_CONTAINER_WIDTH_ADJ_NAME)
        self.mask_container_mp_width_slider = mask_container_mp_width_slider = QSlider(
            Qt.Horizontal, self)
        mask_container_mp_width_slider.setValue(0)
        mask_container_mp_width_slider.setStyleSheet(
            f'QSlider{{max-width: {round(PIC_DEFAULT_WIDTH/2)}; min-width: {round(PIC_DEFAULT_WIDTH/2)};}}'
        )
        mask_container_mp_width_slider.valueChanged.connect(
            self.on_mp_width_change)
        self.mp_width_change_val = QLabel(self)
        self.mp_width_change_val.setFont(QFont('宋体', mfontsize))
        self.mp_width_change_val.setAlignment(Qt.AlignLeft)
        self.mp_width_change_val.setText(str('%-4d' % 0))
        mp_width_change_h_layout.addWidget(mp_width_change_label)
        mp_width_change_h_layout.addStretch(1)
        mp_width_change_h_layout.addWidget(mask_container_mp_width_slider)
        mp_width_change_h_layout.addStretch(1)
        mp_width_change_h_layout.addWidget(self.mp_width_change_val)
        mp_width_change_h_layout.setGeometry(
            QRect(5, round(PIC_DEFAULT_HEIGHT + self.gap * 15),
                  PIC_DEFAULT_WIDTH, self.gap * 2))

        # 蒙版宽度设置滑动条
        mask_width_change_h_layout = QHBoxLayout()
        mask_width_change_label = QLabel(self)
        mask_width_change_label.setFont(QFont('宋体', mfontsize))
        mask_width_change_label.setText(MASK_WIDTH_ADJ_NAME)
        self.mask_container_mask_width_slider = mask_container_mask_width_slider = QSlider(
            Qt.Horizontal, self)

        mask_container_mask_width_slider.setValue(0)
        mask_container_mask_width_slider.setStyleSheet(
            f'QSlider{{max-width: {round(PIC_DEFAULT_WIDTH/2)}; min-width: {round(PIC_DEFAULT_WIDTH/2)};}}'
        )
        mask_container_mask_width_slider.valueChanged.connect(
            self.on_mask_width_change)
        self.mask_width_change_val = QLabel(self)
        self.mask_width_change_val.setFont(QFont('宋体', mfontsize))
        self.mask_width_change_val.setText(str('%-4d' % 0))
        mask_width_change_h_layout.addWidget(mask_width_change_label)
        mask_width_change_h_layout.addStretch(1)
        mask_width_change_h_layout.addWidget(mask_container_mask_width_slider)
        mask_width_change_h_layout.addStretch(1)
        mask_width_change_h_layout.addWidget(self.mask_width_change_val)
        mask_width_change_h_layout.setGeometry(
            QRect(5, round(PIC_DEFAULT_HEIGHT + self.gap * 20),
                  PIC_DEFAULT_WIDTH, self.gap * 2))

        # 蒙版高度设置滑动条
        mask_height_change_h_layout = QHBoxLayout()
        mask_height_change_label = QLabel(self)
        mask_height_change_label.setFont(QFont('宋体', mfontsize))
        mask_height_change_label.setText(MASK_HEIGHT_ADJ_NAME)
        self.mask_container_mask_height_slider = mask_container_mask_height_slider = QSlider(
            Qt.Horizontal, self)
        mask_container_mask_height_slider.setValue(0)
        mask_container_mask_height_slider.setStyleSheet(
            f'QSlider{{max-width: {round(PIC_DEFAULT_WIDTH/2)}; min-width: {round(PIC_DEFAULT_WIDTH/2)};}}'
        )
        mask_container_mask_height_slider.valueChanged.connect(
            self.on_mask_height_change)
        self.mask_height_change_val = QLabel(self)
        self.mask_height_change_val.setFont(QFont('宋体', mfontsize))
        self.mask_height_change_val.setText(str('%-4d' % 0))
        mask_height_change_h_layout.addWidget(mask_height_change_label)
        mask_height_change_h_layout.addStretch(1)
        mask_height_change_h_layout.addWidget(
            mask_container_mask_height_slider)
        mask_height_change_h_layout.addStretch(1)
        mask_height_change_h_layout.addWidget(self.mask_height_change_val)
        mask_height_change_h_layout.setGeometry(
            QRect(5, round(PIC_DEFAULT_HEIGHT + self.gap * 25),
                  PIC_DEFAULT_WIDTH, self.gap * 2))

        # 蒙版组内设置滑动条
        mask_counts_change_h_layout = QHBoxLayout()
        mask_counts_change_label = QLabel(self)
        mask_counts_change_label.setFont(QFont('宋体', mfontsize))
        mask_counts_change_label.setText(MASK_COUNTS_ADJ_NAME)
        self.mask_container_mask_counts_slider = mask_container_mask_counts_slider = QSlider(
            Qt.Horizontal, self)
        mask_container_mask_counts_slider.setRange(1, MASK_MAX_COUNTS)
        mask_container_mask_counts_slider.setValue(0)
        mask_container_mask_counts_slider.setStyleSheet(
            f'QSlider{{max-width: {round(PIC_DEFAULT_WIDTH/2)}; min-width: {round(PIC_DEFAULT_WIDTH/2)};}}'
        )
        mask_container_mask_counts_slider.valueChanged.connect(
            self.on_mask_counts_change)
        self.mask_counts_change_val = QLabel(self)
        self.mask_counts_change_val.setFont(QFont('宋体', mfontsize))
        self.mask_counts_change_val.setAlignment(Qt.AlignLeft)
        self.mask_counts_change_val.setText(str('%-4d' % 0))
        mask_counts_change_h_layout.addWidget(mask_counts_change_label)
        mask_counts_change_h_layout.addStretch(1)
        mask_counts_change_h_layout.addWidget(
            mask_container_mask_counts_slider)
        mask_counts_change_h_layout.addStretch(1)
        mask_counts_change_h_layout.addWidget(self.mask_counts_change_val)
        mask_counts_change_h_layout.setGeometry(
            QRect(5, round(PIC_DEFAULT_HEIGHT + self.gap * 30),
                  PIC_DEFAULT_WIDTH, self.gap * 2))

        # 蒙版倾角设置滑动条
        mask_theta_change_h_layout = QHBoxLayout()
        mask_theta_change_label = QLabel(self)
        mask_theta_change_label.setFont(QFont('宋体', mfontsize))
        mask_theta_change_label.setText(MASK_THETA_ADJ_NAME)
        self.mask_container_mask_theta_slider = mask_container_mask_theta_slider = QSlider(
            Qt.Horizontal, self)
        mask_container_mask_theta_slider.setRange(15, 90)
        mask_container_mask_theta_slider.setValue(0)
        mask_container_mask_theta_slider.setStyleSheet(
            f'QSlider{{max-width: {round(PIC_DEFAULT_WIDTH/2)}; min-width: {round(PIC_DEFAULT_WIDTH/2)};}}'
        )
        mask_container_mask_theta_slider.valueChanged.connect(
            self.on_mask_theta_change)
        self.mask_theta_change_val = QLabel(self)
        self.mask_theta_change_val.setFont(QFont('宋体', mfontsize))
        self.mask_theta_change_val.setAlignment(Qt.AlignLeft)
        self.mask_theta_change_val.setText(str('%-4d' % 0))
        mask_theta_change_h_layout.addWidget(mask_theta_change_label)
        mask_theta_change_h_layout.addStretch(1)
        mask_theta_change_h_layout.addWidget(mask_container_mask_theta_slider)
        mask_theta_change_h_layout.addStretch(1)
        mask_theta_change_h_layout.addWidget(self.mask_theta_change_val)
        mask_theta_change_h_layout.setGeometry(
            QRect(5, round(PIC_DEFAULT_HEIGHT + self.gap * 35),
                  PIC_DEFAULT_WIDTH, self.gap * 2))

        # 蒙版倾角类型设置
        fontsize = 9
        mask_theta_type_change_h_layout = QHBoxLayout()
        mask_theta_type_change_label = QLabel(self)
        mask_theta_type_change_label.setFont(QFont('黑体', fontsize))
        mask_theta_type_change_label.setText('蒙版倾角类型：')
        mask_theta_type_change_h_layout.addWidget(mask_theta_type_change_label)
        mask_theta_type_change_h_layout.addStretch(1)
        self.both = both = QRadioButton(self)
        both.setFont(QFont('黑体', fontsize))
        both.setText('两侧')
        both.setChecked(True)
        both.toggled.connect(lambda: self.on_mask_theta_type_change(both))
        mask_theta_type_change_h_layout.addWidget(both)
        self.left_side = left_side = QRadioButton(self)
        left_side.setFont(QFont('黑体', fontsize))
        left_side.setText('左侧')
        left_side.toggled.connect(
            lambda: self.on_mask_theta_type_change(left_side))
        mask_theta_type_change_h_layout.addWidget(left_side)
        self.right_side = right_side = QRadioButton(self)
        right_side.setFont(QFont('黑体', fontsize))
        right_side.setText('右侧')
        right_side.toggled.connect(
            lambda: self.on_mask_theta_type_change(right_side))
        mask_theta_type_change_h_layout.addWidget(right_side)
        mask_theta_type_change_h_layout.addStretch(1)
        # 需要调整的蒙版索引设置
        combox_label = QLabel(self)
        combox_label.setFont(QFont('黑体', fontsize))
        combox_label.setText(f'需要调整的蒙版[0-{MASK_MAX_COUNTS-1}]：')
        self.combox = combox = QComboBox(self)
        combox.setFont(QFont('黑体', fontsize))
        combox.addItem('全部')
        # for i in range(self.mcontainer.counts):
        #     combox.addItem(f'蒙版{i}')
        combox.currentIndexChanged.connect(self.on_mask_theta_index_change)
        mask_theta_type_change_h_layout.addWidget(combox_label)
        mask_theta_type_change_h_layout.addWidget(combox)
        mask_theta_type_change_h_layout.addStretch(1)
        mask_theta_type_change_h_layout.setGeometry(
            QRect(15, round(PIC_DEFAULT_HEIGHT + self.gap * 38.5),
                  round(PIC_DEFAULT_WIDTH - 10), self.gap * 2))

        # 文件夹或者文件获取按钮
        bg1 = QButtonGroup(self)
        opendirbtn = QPushButton('目录', self)
        opendirbtn.setFont(QFont('宋体', mfontsize))
        opendirbtn.setToolTip('打开要处理的图像的目录')
        opendirbtn.move(
            round(self.totoalWidth * .05),
            round(PIC_DEFAULT_HEIGHT + self.gap * 42.5))
        opendirbtn.clicked.connect(self.on_open_directory)
        openfilebtn = QPushButton('文件', self)
        openfilebtn.setFont(QFont('宋体', mfontsize))
        openfilebtn.setToolTip('打开要处理的单个文件')
        openfilebtn.move(
            round(self.totoalWidth * .18),
            round(PIC_DEFAULT_HEIGHT + self.gap * 42.5))
        openfilebtn.clicked.connect(self.on_open_file)
        bg1.addButton(opendirbtn, 0)
        bg1.addButton(openfilebtn, 1)

        # 确认按钮
        self.returnbtn = returnbtn = QPushButton('车位坐标', self)
        returnbtn.setFont(QFont('宋体', mfontsize))
        returnbtn.setToolTip('返回选定车位区域的坐标')
        returnbtn.move(
            round(self.totoalWidth * .31),
            round(PIC_DEFAULT_HEIGHT + self.gap * 42.5))
        returnbtn.clicked.connect(self.on_return_parking_coordinates)
        bg1.addButton(returnbtn, 2)
        # 上一张和下一张按钮
        self.prevbtn = prevbtn = QPushButton('上一张', self)
        prevbtn.setFont(QFont('宋体', mfontsize))
        prevbtn.move(
            round(self.totoalWidth * .44),
            round(PIC_DEFAULT_HEIGHT + self.gap * 42.5))
        prevbtn.clicked.connect(self.on_previous_photo)
        self.nextbtn = nextbtn = QPushButton('下一张', self)
        nextbtn.setFont(QFont('宋体', mfontsize))
        nextbtn.move(
            round(self.totoalWidth * .57),
            round(PIC_DEFAULT_HEIGHT + self.gap * 42.5))
        nextbtn.clicked.connect(self.on_next_photo)
        bg1.addButton(prevbtn, 3)
        bg1.addButton(nextbtn, 3)
        # 退出按钮
        exitbtn = QPushButton('退出', self)
        exitbtn.setFont(QFont('宋体', mfontsize))
        exitbtn.setToolTip('退出程序(建议在所有车位坐标获取之后)')
        exitbtn.move(
            round(self.totoalWidth * .75),
            round(PIC_DEFAULT_HEIGHT + self.gap * 42.5))
        exitbtn.clicked.connect(self.on_exit)

        self.widget_disabled()
        self.kingkong_disabled()
        self.show()

    def widget_disabled(self):
        '''组件挂起'''
        self.mask_container_px_slider.setDisabled(True)
        self.mask_container_py_slider.setDisabled(True)
        self.mask_container_mp_width_slider.setDisabled(True)
        self.mask_container_mask_width_slider.setDisabled(True)
        self.mask_container_mask_height_slider.setDisabled(True)
        self.mask_container_mask_counts_slider.setDisabled(True)
        self.mask_container_mask_theta_slider.setDisabled(True)
        self.both.setDisabled(True)
        self.left_side.setDisabled(True)
        self.right_side.setDisabled(True)
        self.combox.setDisabled(True)
        self.is_widget_disabled = True

    def widget_abled(self):
        '''contrast with "widget_disabled" function'''
        self.mask_container_px_slider.setDisabled(False)
        self.mask_container_py_slider.setDisabled(False)
        self.mask_container_mp_width_slider.setDisabled(False)
        self.mask_container_mask_width_slider.setDisabled(False)
        self.mask_container_mask_height_slider.setDisabled(False)
        self.mask_container_mask_counts_slider.setDisabled(False)
        self.mask_container_mask_theta_slider.setDisabled(False)
        self.both.setDisabled(False)
        self.left_side.setDisabled(False)
        self.right_side.setDisabled(False)
        self.combox.setDisabled(False)
        self.is_widget_disabled = False

    def kingkong_disabled(self):
        '''禁用返回坐标、上一张、下一张 三大金刚按钮'''
        self.returnbtn.setDisabled(True)
        self.prevbtn.setDisabled(True)
        self.nextbtn.setDisabled(True)

    def widget_init(self):
        '''组件值初始化'''
        self.mask_container_px_slider.setRange(0, self.imgsrc_w)
        self.mask_container_py_slider.setRange(0, self.imgsrc_h)
        self.mask_container_mp_width_slider.setRange(0, self.imgsrc_w)
        self.mask_container_mp_width_slider.setValue(self.imgsrc_w)
        self.mask_container_mask_width_slider.setRange(
            MASK_DEFAULT_WIDTH, round(self.mcontainer.mpwidth / 2))
        self.mask_container_mask_width_slider.setValue(MASK_DEFAULT_WIDTH)
        self.mask_width_change_val.setText(str('%-4d' % MASK_DEFAULT_WIDTH))
        self.mask_container_mask_height_slider.setRange(
            MASK_DEFAULT_HEIGHT, self.imgsrc_h)
        self.mask_height_change_val.setText(str('%-4d' % MASK_DEFAULT_HEIGHT))
        self.mask_container_mask_counts_slider.setValue(MASK_DEFAULT_COUNTS)
        self.mask_counts_change_val.setText(str('%-4d' % MASK_DEFAULT_COUNTS))
        self.mask_container_mask_theta_slider.setValue(90)
        self.mask_theta_change_val.setText(str('%-4d' % 90))

    def tocenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def loadlocalimg(self, filename):
        if not filename.endswith(('jpg', 'jpeg', 'png', 'bmp')):
            QMessageBox.question(self, 'critical',
                                 self.tr('只接受jpg、jpeg、png、bmp类型的图片'),
                                 QMessageBox.Close)

            return
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
        if self.is_widget_disabled:
            self.widget_abled()
            self.widget_init()
        self.paint()

    def paint(self):
        cimg = self.imgsrc.copy()
        cors = self.mcontainer.coordinates
        for e in cors:
            c = e[:-2]
            c = np.array(c, dtype=np.int32)
            c = c.reshape((-1, 1, 2))
            cv2.polylines(cimg, [c], True, (0, 0, 255), 3)
        cimg = self.toPixmap(cimg, self.imgsrc_h, self.imgsrc_w)
        cimg = cimg.scaled(self.imgLabel.width(), self.imgLabel.height())
        self.imgLabel.setPixmap(cimg)

    def toPixmap(self, img, height, width):
        '''将opencv图像转换成能在Qt控件中显示的格式
        
        Params:
        =====
            @img        opencv的格式图像 
            @height     图像的高度
            @width      图像的宽度
        '''
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        bytesPerLine = 3 * width
        img = QImage(img.data, width, height, bytesPerLine,
                     QImage.Format_RGB888)
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
        theta = val / 180 * np.pi
        self.mcontainer.theta = theta
        self.mask_theta_change_val.setText(str(val))
        self.paint()

    def on_mask_counts_change(self, val):
        '''设置蒙版组内蒙版的数量'''
        if val == 0:
            return
        self.mcontainer.counts = val
        self.mask_counts_change_val.setText(str(val))
        self.paint()

    def on_mask_theta_type_change(self, btn: QRadioButton):
        '''设置蒙版倾角类型'''
        rsl = btn.text()
        if rsl == '两侧':
            self.mcontainer.theta_type = 0
        elif rsl == '左侧':
            self.mcontainer.theta_type = 1
        elif rsl == '右侧':
            self.mcontainer.theta_type = 2
        else:
            self.mcontainer.theta_type = 0

    def on_mask_theta_index_change(self, idx):
        '''设置需要修改倾角的蒙版'''
        self.mcontainer.theta_index = idx

    def on_open_directory(self):
        '''获取文件所在目录或单个文件路径'''
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹", './')
        # TODO 获取文件目录所有图像文件并作车位截取

    def on_open_file(self):
        '''获取单个文件路径'''
        self.kingkong_disabled()
        fileurl = QFileDialog.getOpenFileName(self, "选取文件*.jpg|.jpeg|png|bmp",
                                              './')
        self.is_only_one_file = True
        try:
            filepathname = str(fileurl[0])
            if len(filepathname):
                self.loadlocalimg(filepathname)
                self.returnbtn.setDisabled(False)
        except Exception as e:
            QMessageBox.question(self, 'critical', self.tr('发生错误'))

    def on_previous_photo(self):
        '''切换到上一张图像'''
        # TODO
        pass

    def on_next_photo(self):
        '''切换到下一张图像'''
        pass

    def on_return_parking_coordinates(self):
        '''返回车位区域坐标'''
        # TODO 车位坐标
        pass

    def on_exit(self):
        '''退出程序功能'''
        exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())
