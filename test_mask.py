# -*- encoding: utf-8 -*-
'''车位蒙版提取测试模块'''

import random
from mask import *
from config import *


def test_mask():
    print('Begining to test Class "Mask"...')
    w = MASK_DEFAULT_WIDTH
    h = MASK_DEFAULT_HEIGHT
    c_x = random.random() * 100
    c_y = random.random() * 100
    m = Mask(w, h, c_x, c_y, no=1)
    print(m)
    print('Finished testing!')


def test_maskgroup():
    print('Begining to test Class "MaskGroup"...')
    p_x = random.random() * 100
    p_y = random.random() * 100
    scw = 1000
    theta = np.pi / 2
    mp = MaskGroup(p_x, p_y, scw, MASK_COUNTS, theta)
    mp.create()
    print(mp)
    print(mp.masks[2], '\n', mp.masks[1])
    print('Finished testing!')


if __name__ == '__main__':
    # test class Mask
    # test_mask()
    test_maskgroup()