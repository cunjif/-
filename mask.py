# -*- encoding: utf-8 -*-
'''定义蒙版模块'''

import numpy as np
from config import *


class Mask(object):
    def __init__(self, w: float, h: float, c_x: float, c_y: float, no=0):
        '''初始化蒙版参数
        
        @params:
            w: 长度
            h: 高度
            c_x: 中心点横坐标
            c_y: 中心点纵坐标
            no: 蒙版编号
        '''

        self.c_x = c_x
        self.c_y = c_y
        self.width = w
        self.height = h
        self.theta = np.pi / 2
        self.theta_type = 0
        self.no = no

    def __str__(self):
        return '--- <class %(name)s > --- \
        \n width: %(width).2f\
        \n height: %(height).2f \
        \n center x: %(cx).2f\
        \n center y: %(cy).2f\
        \n serial number: %(no)d' % {
            'name': Mask.__name__,
            'width': self.width,
            'height': self.height,
            'cx': self.c_x,
            'cy': self.c_y,
            'no': self.no
        }

    def change(self, cx, cy, w, h, t, ttype):
        self.c_x = cx if cx else self.c_x
        self.c_y = cy if cy else self.c_y
        self.width = w if w else self.width
        self.height = h if h else self.height
        self.theta = t if t else self.theta
        self.theta_type = ttype if ttype else self.theta_type


class MaskGroup(object):
    '''蒙版组类

    定义蒙版组，设定蒙版组的位置，大小和蒙版组内元素的个数、大小等信息'''

    def __init__(self, p_x: float, p_y: float, sc_w: float, counts: int,
                 theta: float):
        # TODO 定义蒙版组
        self.p_x = p_x
        self.p_y = p_y
        self.sc_w = sc_w
        self.m_w = sc_w  # maskgroup的总大小
        self.w = MASK_DEFAULT_WIDTH
        self.h = MASK_DEFAULT_HEIGHT
        self.counts = counts
        self.theta = theta
        self.default_theta = np.pi / 2
        self.masks = []
        # 设置需要修改倾角数值的蒙版，值为蒙版索引
        # 缺省为0，即所有蒙版同步修改倾角
        self.theta_index = 0
        # 设置蒙版倾角类型
        # 缺省为0，即同时修改两侧倾角，呈梯形
        # 为1时，修改左侧倾角
        # 为2时，修改右侧倾角
        self.theta_type = 0

    def create(self):
        # half of a single mask width
        sw = self.m_w / self.counts
        half_sw = sw / 2
        # offset width
        w = sw * (self.counts - 1)
        # a mask centra point y position
        c_y = self.p_y + self.h / 2
        if len(self.masks) == 0:
            for idx, dx in enumerate(
                    np.linspace(self.p_x, self.p_x + w, self.counts)):
                c_x = dx + half_sw
                _ = Mask(w=self.w, h=self.h, c_x=c_x, c_y=c_y, no=idx)
                self.masks.append(_)
        elif len(self.masks) < self.counts:
            temporal = self.masks.copy()
            self.masks.clear()
            templen = len(temporal)
            for idx, dx in enumerate(
                    np.linspace(self.p_x, self.p_x + w, self.counts)):
                c_x = dx + half_sw
                _ = Mask(self.w, self.h, c_x, c_y, no=idx)
                if templen > idx:
                    _.theta = temporal[idx].theta
                    _.theta_type = temporal[idx].theta_type
                else:
                    _.theta = self.default_theta
                self.masks.append(_)
        else:
            temporal = self.masks.copy()
            templen = len(temporal)
            self.masks.clear()
            for idx, dx in enumerate(
                    np.linspace(self.p_x, self.p_x + w, self.counts)):
                c_x = dx + half_sw
                _ = Mask(self.w, self.h, c_x, c_y, no=idx)
                _.theta = temporal[idx].theta
                _.theta_type = temporal[idx].theta_type
                self.masks.append(_)

    def on_theta_change(self, theta):
        '''倾角发生改变时处理函数'''
        self.theta = theta
        if self.theta_index == 0:
            for i in range(self.counts):
                self.masks[i].theta = theta
        else:
            self.masks[self.theta_index - 1].theta = theta

    def on_theta_type_change(self, ttype):
        '''设置倾角类型
        
        指定是“双侧”、“左侧”或者“右侧”类型倾角'''
        if self.theta_index == 0:
            for ix in range(self.counts):
                self.masks[ix].theta_type = ttype
        else:
            self.masks[self.theta_index - 1].theta_type = ttype

    def on_px_change(self, p_x):
        self.p_x = p_x
        self.create()

    def on_mask_counts_change(self, counts):
        self.counts = counts
        self.create()

    def on_mw_change(self, m_w):
        self.m_w = m_w
        self.create()

    def on_scw_change(self):
        # TODO 图像宽度发生改变
        pass

    def on_single_mask_width_change(self, val):
        '''修改单个蒙版的宽度'''
        self.w = val
        for i in range(self.counts):
            self.masks[i].width = val

    def on_single_mask_height_change(self, val):
        '''修改单个蒙版的高度'''
        self.h = val
        for i in range(self.counts):
            self.masks[i].height = val

    def on_py_change(self, p_y):
        '''纵坐标发生改变'''
        self.p_y = p_y
        c_y = p_y + self.h / 2
        for idx in range(self.counts):
            self.masks[idx].c_y = c_y

    @property
    def coordinates(self):
        cors = []
        for idx, e in enumerate(self.masks):
            if np.tan(self.theta) == 0:
                continue
            hw = e.width / 2
            hh = e.height / 2
            tl = [round(e.c_x - hw), round(e.c_y - hh)]
            tr = [round(e.c_x + hw), round(e.c_y - hh)]
            if e.theta != np.pi / 2:
                if e.theta_type == 0:
                    bl = [
                        round(e.c_x - hw - e.height / np.tan(e.theta)),
                        e.c_y + hh
                    ]
                    br = [
                        round(e.c_x + hw + e.height / np.tan(e.theta)),
                        e.c_y + hh
                    ]
                elif e.theta_type == 1:
                    bl = [
                        round(e.c_x - hw - e.height / np.tan(e.theta)),
                        e.c_y + hh
                    ]
                    br = [round(e.c_x + hw), round(e.c_y + hh)]
                else:
                    bl = [round(e.c_x - hw), round(e.c_y + hh)]
                    br = [
                        round(e.c_x + hw + e.height / np.tan(e.theta)),
                        e.c_y + hh
                    ]
            else:
                bl = [round(e.c_x - hw), round(e.c_y + hh)]
                br = [round(e.c_x + hw), round(e.c_y + hh)]
            cors.append([tl, tr, br, bl, [round(e.c_x), round(e.c_y)], e.no])
        return cors

    def __str__(self):
        return '--- <class %(name)s> ---\
            \n point x: %(px).2f\
            \n point y: %(py).2f\
            \n image width: %(scw).2f\
            \n width: %(width).2f\
            \n height: %(height).2f \
            \n counts: %(counts)d\
            \n masks: %(masks)a' % {
            'name': Mask.__name__,
            'px': self.p_x,
            'py': self.p_y,
            'scw': self.sc_w,
            'width': self.w,
            'height': self.h,
            'counts': self.counts,
            'masks': self.masks
        }


class MaskContainer(object):
    '''创建蒙板组边框

    蒙版组边框用于包裹蒙版组，限定蒙版组大小和位置调节'''

    def __init__(self, sc_w, sc_h, theta=np.pi / 2):
        counts = MASK_DEFAULT_COUNTS
        p_x = sc_w * MASK_POS_X
        p_y = sc_h * MASK_POS_Y
        self.mp = MaskGroup(p_x, p_y, sc_w, counts, np.pi / 2)
        self.mp.create()

    @property
    def px(self):
        return self.mp.p_x

    @px.setter
    def px(self, val):
        self.mp.on_px_change(val)

    @property
    def py(self):
        return self.mp.py

    @py.setter
    def py(self, val):
        self.mp.on_py_change(val)

    @property
    def mpwidth(self):
        return self.mp.m_w

    @mpwidth.setter
    def mpwidth(self, val):
        self.mp.on_mw_change(val)

    @property
    def mask_width(self):
        return self.mp.w

    @mask_width.setter
    def mask_width(self, val):
        self.mp.on_single_mask_width_change(val)

    @property
    def mask_height(self):
        return self.mp.h

    @mask_height.setter
    def mask_height(self, val):
        self.mp.on_single_mask_height_change(val)

    @property
    def theta(self):
        return self.mp.theta

    @theta.setter
    def theta(self, val):
        self.mp.on_theta_change(val)

    @property
    def counts(self):
        return self.mp.counts

    @counts.setter
    def counts(self, val):
        self.mp.on_mask_counts_change(val)

    # @property
    # def theta_side(self):
    #     return self.mp.theta_side

    # @theta_side.setter
    # def theta_side(self, val):
    #     self.mp.theta_side = val

    @property
    def theta_index(self):
        return self.mp.theta_index

    @theta_index.setter
    def theta_index(self, val):
        self.mp.theta_index = val

    @property
    def theta_type(self):
        return self.mp.theta_type

    @theta_type.setter
    def theta_type(self, val):
        return self.mp.on_theta_type_change(val)

    @property
    def coordinates(self):
        return self.mp.coordinates
