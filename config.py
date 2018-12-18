# -*- encoding: utf-8 -*-
'''车位初始化检测模块

模板法配置'''

# 蒙版位置标志
# 可选值为None, TOP, MID, BOT
# 如果不为None，则蒙版初始位置参数失效
# 如果为None，则此参数失效，蒙版初始位置由 `蒙版初始位置` 参数决定
POS_ID = None
# 蒙版初始位置
MASK_POS_X = 0
MASK_POS_Y = 0

# 蒙版初始大小
MASK_DEFAULT_HEIGHT = 10
MASK_DEFAULT_WIDTH = 10

# 蒙版数量
MASK_MAX_COUNTS = 5
MASK_DEFAULT_COUNTS = 4

# 缩放参数
# 对原图进行的大小等比例缩放参数
# 取值范围在0~1之间的浮点数
SCALE_FAC = 1.0

# 设置默认车位截取窗口大小
# 窗口大小会影响车位坐标信息
#   ，必须与系统其他部分设置一致
PARKING_PART_DEFAULT_WIDTH = 500
PARKING_PART_DEFAULT_HEIGHT = 600

# 默认图像显示宽度和高度
# 仅在使用Qt的模块中有效
PIC_DEFAULT_WIDTH = PARKING_PART_DEFAULT_WIDTH - 10
PIC_DEFAULT_HEIGHT = round(PARKING_PART_DEFAULT_HEIGHT / 2)

# 窗口名称
PARKING_PART_WINDOW_NAME = '车位截取'