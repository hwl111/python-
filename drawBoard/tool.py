import math
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP  # 导入事件

class Brush:
    """
    画笔类
    """
    def __init__(self, screen):
        self.screen = screen  # 屏幕对象
        self.color = (0, 0, 0)  # 颜色
        self.size = 1  # 大小
        self.drawing = False  # 是否绘画
        self.last_pos = None  # 鼠标滑过最后的位置
        self.space = 1
        self.brush = pygame.image.load("img/pen.png").convert_alpha()  # 画笔图片
        self.brush_now = self.brush.subsurface((0, 0), (1, 1))  # 初始化画笔对象

    # 开始绘画
    def start_draw(self, pos):
        self.drawing = True
        self.last_pos = pos # 记录鼠标最后位置

    # 结束绘画
    def end_draw(self):
        self.drawing = False

    # 获取当前使用画笔
    def get_current_brush(self):
        return self.brush_now # 获取当前使用的画笔对象

    def set_size(self, size):  # 设置画笔大小
        if size < 0.5: # 判断画笔尺寸小于0.5
            size = 0.5 # 设置画笔最小尺寸为0.5
        elif size > 32: # 判断画笔尺寸大于32
            size = 32 # 设置画笔最大尺寸为32
        self.size = size # 设置画笔尺寸
        # 生成画笔对象
        self.brush_now = self.brush.subsurface((0, 0), (size * 2, size * 2))

    # 获取画笔大小
    def get_size(self):
        return self.size

    # 设置画笔颜色
    def set_color(self, color):
        self.color = color # 记录选择的颜色
        for i in range(self.brush.get_width()): # 获取画笔的宽度
            for j in range(self.brush.get_height()): #获取画笔的高度
                # 以指定颜色显示画笔
                self.brush.set_at((i, j), color + (self.brush.get_at((i, j)).a,))

    # 获取画笔颜色
    def get_color(self):
        return self.color

    # 绘制动作
    def draw(self, pos):
        if self.drawing: # 判断是否开始绘画
            for p in self._get_points(pos):
                # 在两点之间的每个点上都画上实心点
                pygame.draw.circle(self.screen, self.color, p, int(self.size))
            self.last_pos = pos # 记录画笔最后位置

    # 获取两点之间所有的点位，该函数通过对鼠标坐标前一次记录点与当前记录点之间进行线性插值
    # 从而获得一系列点的坐标，从而使得绘制出来的画笔痕迹更加平滑自然
    def _get_points(self, pos):
        points = [(self.last_pos[0], self.last_pos[1])]
        len_x = pos[0] - self.last_pos[0]
        len_y = pos[1] - self.last_pos[1]
        length = math.sqrt(len_x ** 2 + len_y ** 2)
        step_x = len_x / length
        step_y = len_y / length
        for i in range(int(length)):
            points.append(
                (points[-1][0] + step_x, points[-1][1] + step_y))
        # 对 points 中的点坐标进行四舍五入取整
        points = map(lambda x: (int(0.5 + x[0]), int(0.5 + x[1])), points)
        return list(set(points)) # 去除坐标相同的点

class Menu:
    """
    菜单类
    """
    def __init__(self, screen):
        self.screen = screen  # 初始化窗口
        self.brush = None
        self.colors = [  # 颜色表
            (0xff, 0x00, 0xff), (0x80, 0x00, 0x80),
            (0x00, 0x00, 0xff), (0x00, 0x00, 0x80),
            (0x00, 0xff, 0xff), (0x00, 0x80, 0x80),
            (0x00, 0xff, 0x00), (0x00, 0x80, 0x00),
            (0xff, 0xff, 0x00), (0x80, 0x80, 0x00),
            (0xff, 0x00, 0x00), (0x80, 0x00, 0x00),
            (0xc0, 0xc0, 0xc0), (0x00, 0x00, 0x00),
            (0x80, 0x80, 0x80), (0x00, 0xc0, 0x80),
        ]
        self.eraser_color = (0xff, 0xff, 0xff) # 初始颜色
        # 计算每个色块在画板中的坐标值，便于绘制
        self.colors_rect = []
        for (i, rgb) in enumerate(self.colors):  # 方块颜色表
            rect = pygame.Rect(10 + i % 2 * 32, 254 + i / 2 * 32, 32, 32)
            self.colors_rect.append(rect)

        self.pens = [  # 画笔图片
            pygame.image.load("img/pen.png").convert_alpha(),
        ]
        self.erasers = [  # 橡皮图片
            pygame.image.load("img/eraser.png").convert_alpha(),
        ]
        self.erasers_rect = []
        for (i, img) in enumerate(self.erasers):  # 橡皮列表
            rect = pygame.Rect(10, 10 + (i + 1) * 64, 64, 64)
            self.erasers_rect.append(rect)

        self.pens_rect = []
        for (i, img) in enumerate(self.pens):  # 画笔列表
            rect = pygame.Rect(10, 10 + i * 64, 64, 64)
            self.pens_rect.append(rect)

        self.sizes = [  # 加减号图片
            pygame.image.load("img/plus.png").convert_alpha(),
            pygame.image.load("img/minus.png").convert_alpha()
        ]

        # 计算坐标，便于绘制
        self.sizes_rect = []
        for (i, img) in enumerate(self.sizes):
            rect = pygame.Rect(10 + i * 32, 138, 32, 32)
            self.sizes_rect.append(rect)

    def set_brush(self, brush):  # 设置画笔对象
        self.brush = brush

    def draw(self):  # 绘制菜单栏
        for (i, img) in enumerate(self.pens): # 绘制画笔样式按钮
            self.screen.blit(img, self.pens_rect[i].topleft)
        for (i, img) in enumerate(self.erasers): # 绘制橡皮按钮
            self.screen.blit(img, self.erasers_rect[i].topleft)
        for (i, img) in enumerate(self.sizes): # 绘制 + - 按钮
            self.screen.blit(img, self.sizes_rect[i].topleft)
        # 绘制用于实时展示画笔的小窗口
        self.screen.fill((255, 255, 255), (10, 180, 64, 64))
        pygame.draw.rect(self.screen, (0, 0, 0), (10, 180, 64, 64), 1)
        size = self.brush.get_size()
        x = 10 + 32
        y = 180 + 32
        # 在窗口中展示画笔
        pygame.draw.circle(self.screen, self.brush.get_color(), (x, y), int(size))
        for (i, rgb) in enumerate(self.colors): # 绘制色块
            pygame.draw.rect(self.screen, rgb, self.colors_rect[i])

    def click_button(self, pos):
        # 点击加减号事件
        for (i, rect) in enumerate(self.sizes_rect):
            if rect.collidepoint(pos):
                if i:  # i == 1, size down
                    self.brush.set_size(self.brush.get_size() - 0.5)
                else:
                    self.brush.set_size(self.brush.get_size() + 0.5)
                return True
        # 点击颜色按钮事件
        for (i, rect) in enumerate(self.colors_rect):
            if rect.collidepoint(pos):
                self.brush.set_color(self.colors[i])
                return True
        # 点击橡皮按钮事件
        for (i, rect) in enumerate(self.erasers_rect):
            if rect.collidepoint(pos):
                self.brush.set_color(self.eraser_color)
                return True
        return False

class Paint:
    """
    窗口绘制类
    """
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600)) # 显示窗口
        pygame.display.set_caption("超级画板") # 设置窗口标题
        self.clock = pygame.time.Clock() # 控制速率
        self.brush = Brush(self.screen) # 创建画刷对象
        self.menu = Menu(self.screen) # 创建窗口菜单
        self.menu.set_brush(self.brush) # 设置默认画刷

    def clear_screen(self):
        self.screen.fill((255, 255, 255))  # 填充空白

    def run(self):
        self.clear_screen() # 清除屏幕
        while True:
            # 设置fps，表示每秒执行30次（注意：30不是毫秒数）
            self.clock.tick(30)
            for event in pygame.event.get(): # 遍历所有事件
                if event.type == QUIT:  # 退出事件
                    return
                elif event.type == KEYDOWN:  # 按键事件
                    # 按ESC键清空画板
                    if event.key == K_ESCAPE:  # ESC按键事件
                        self.clear_screen()
                elif event.type == MOUSEBUTTONDOWN:  # ；鼠标左键按下事件
                    if ((event.pos)[0] <= 74 and self.menu.click_button(event.pos)):  # 未点击画板按钮
                        pass
                    else:
                        self.brush.start_draw(event.pos)  # 开始绘画
                elif event.type == MOUSEMOTION:  # 鼠标移动事件
                    self.brush.draw(event.pos)  # 绘画动作
                elif event.type == MOUSEBUTTONUP:  # 鼠标左键松开事件
                    self.brush.end_draw()  # 停止绘画
            self.menu.draw()
            pygame.display.update()  # 更新画板
