# -*- coding: utf-8 -*-
'''绘图模块'''

import cv2
import os.path as opath
from config import *
from mask import *

MASK_CONTAINER_PX_ADJ_NAME = 'MaskContainerPostionX: '
MASK_CONTAINER_PY_ADJ_NAME = 'MaskContainerPostionY: '
MASK_CONTAINER_WIDTH_ADJ_NAME = 'MaskContainerWidth: '
MASK_WIDTH_ADJ_NAME = 'MaskWidth: '
MASK_HEIGHT_ADJ_NAME = 'MaskHeight: '
MASK_THETA_ADJ_NAME = 'Theta: '
MASK_COUNTS_ADJ_NAME = 'MaskCounts: '
src = None
mcontainer = None

def on_px_change(val):
    '''调节蒙板框横坐标'''
    mcontainer.px = val
    paint()


def on_py_change(val):
    '''调节蒙板框纵坐标'''
    mcontainer.py = val
    paint()


def on_mp_width_change(val):
    '''设置蒙板组宽度'''
    mcontainer.mpwidth = val
    paint()

def on_mask_width_change(val):
    '''设置蒙版宽度'''
    mcontainer.mask_width = val
    paint()


def on_mask_height_change(val):
    '''设置蒙版高度'''
    mcontainer.mask_height = val
    paint()


def on_mask_theta_change(val):
    '''设置蒙板的倾角'''
    theta = val/180 * np.pi
    mcontainer.theta = theta
    paint()


def on_mask_counts_change(val):
    '''设置蒙版组内蒙版的数量'''
    if val == 0:
        return
    mcontainer.counts = val
    paint()


def paint():
    '''绘制函数'''
    csrc = src.copy()
    cors = mcontainer.coordinates
    for e in cors:
        cors = e[:-2]
        cors = np.array(cors, dtype=int)
        cors = cors.reshape((-1,1,2))
        cv2.polylines(csrc, [cors], True, (0,0,255), 3)
    cv2.imshow(PARKING_PART_WINDOW_NAME, csrc)


def draw(filename):
    assert isinstance(filename, str), '输入参数类型必须是"str"类型！'
    assert opath.exists(filename), '输入文件不存在！'
    assert opath.isfile(filename), '输入参数不是一个文件'
    assert filename.endswith(('jpeg', 'jpg', 'bmp', 'png')), '只接受图像文件'
    
    global src
    global mcontainer
    src = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    if src.ndim == 3:
        sch, scw, _ = src.shape
    else:
        sch, scw = src.shape
    mcontainer = MaskContainer(scw, sch)

    # 命名显示窗口
    cv2.namedWindow(PARKING_PART_WINDOW_NAME, 0)
    # 设置显示窗口大小
    cv2.resizeWindow(
        PARKING_PART_WINDOW_NAME,
        PARKING_PART_DEFAULT_WIDTH,
        PARKING_PART_DEFAULT_HEIGHT)
    
    # 蒙板框横坐标设置滑条
    cv2.createTrackbar(
        MASK_CONTAINER_PX_ADJ_NAME, 
        PARKING_PART_WINDOW_NAME, 
        MASK_POS_X, scw, on_px_change)
    # 蒙板框纵坐标设置滑条
    cv2.createTrackbar(
        MASK_CONTAINER_PY_ADJ_NAME,
        PARKING_PART_WINDOW_NAME,
        MASK_POS_Y,
        sch, on_py_change)
    # 蒙板组宽度设置滑条
    cv2.createTrackbar(
        MASK_CONTAINER_WIDTH_ADJ_NAME,
        PARKING_PART_WINDOW_NAME,
        sch, sch,
        on_mp_width_change)
    # 单个蒙板宽度设置滑条
    cv2.createTrackbar(
        MASK_WIDTH_ADJ_NAME,
        PARKING_PART_WINDOW_NAME,
        MASK_DEFAULT_WIDTH,
        round(scw/(MASK_COUNTS+1)),
        on_mask_width_change)
    # 单个蒙板高度设置滑条
    cv2.createTrackbar(
        MASK_HEIGHT_ADJ_NAME,
        PARKING_PART_WINDOW_NAME,
        MASK_DEFAULT_WIDTH,
        sch,
        on_mask_height_change)
    # 蒙板倾角
    cv2.createTrackbar(
        MASK_THETA_ADJ_NAME,
        PARKING_PART_WINDOW_NAME,
        90,
        90,
        on_mask_theta_change)
    # 蒙板数量设置滑条
    cv2.createTrackbar(
        MASK_COUNTS_ADJ_NAME,
        PARKING_PART_WINDOW_NAME,
        MASK_COUNTS,
        MASK_COUNTS,
        on_mask_counts_change)

    paint()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    exit()
    
if __name__ == '__main__':
    draw('2.jpg')