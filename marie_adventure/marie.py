import pygame
import sys
from pygame.locals import *
from itertools import cycle   #导入迭代工具
import random

SCREENWIDTH = 822   #窗口宽度
SCREENHEIGHT = 199  #窗口高度
FPS = 30


#定义一个移动地图类
class MyMap():

    def __init__(self,x, y):
        #加载背景图片
        self.bg = pygame.image.load("image/bg.png").convert_alpha()
        self.x = x
        self.y = y

    def map_rolling(self):
        if self.x < -790:
            self.x = 800
        else:
            self.x -= 5  #向左移动5
    #更新地图
    def map_updata(self):
        SCREEN.blit(self.bg, (self.x, self.y))

class Marie():
    def __init__(self):
        #初始化
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.jumpState = False  #判断是否跳跃
        self.jumpHeight = 130    #跳跃高度
        self.lowest_y = 140      #最低高度
        self.jumpValue = 0       #跳跃变量
        #玛丽动图索引
        self.marieIndex = 0
        self.marieIndexGen = cycle([0, 1, 2])
        #加载玛丽图片
        self.adventure_img = (
            pygame.image.load("image/adventure1.png").convert_alpha(),
            pygame.image.load("image/adventure2.png").convert_alpha(),
            pygame.image.load("image/adventure3.png").convert_alpha()
        )
        self.jump_audio = pygame.mixer.Sound("audio/jump.wav")  #加载跳跃音效
        self.rect.size = self.adventure_img[0].get_size()  #获取图片大小
        self.x = 50
        self.y = self.lowest_y
        self.rect.topleft = (self.x, self.y)
    def jump(self):
        self.jumpState = True
    def move(self):
        if self.jumpState:
            if self.rect.y >= self.lowest_y:
                self.jumpValue = -5
            if self.rect.y <= self.lowest_y - self.jumpHeight:
                self.jumpValue = 5
            self.rect.y += self.jumpValue
            if self.rect.y >= self.lowest_y:
                self.jumpState = False

    def draw(self):
        #匹配玛丽动图
        marieIndex = next(self.marieIndexGen)
        #绘制玛丽
        SCREEN.blit(self.adventure_img[marieIndex],
                    (self.x, self.rect.y))

#障碍物类
class Obstacle():
    score = 1    #分数
    move = 2     #移动距离
    obstacle_y = 150   #障碍物的y坐标
    def __init__(self):
        #初始化障碍物矩形
        self.rect = pygame.Rect(0, 0, 0, 0)
        #加载障碍物图片
        self.missile = pygame.image.load("image/missile.png")
        self.pipe = pygame.image.load("image/pipe.png")
        #加载分数图片
        self.numbers = (pygame.image.load("image/0.png").convert_alpha(),
                        pygame.image.load("image/1.png").convert_alpha(),
                        pygame.image.load("image/2.png").convert_alpha(),
                        pygame.image.load("image/3.png").convert_alpha(),
                        pygame.image.load("image/4.png").convert_alpha(),
                        pygame.image.load("image/5.png").convert_alpha(),
                        pygame.image.load("image/6.png").convert_alpha(),
                        pygame.image.load("image/7.png").convert_alpha(),
                        pygame.image.load("image/8.png").convert_alpha(),
                        pygame.image.load("image/9.png").convert_alpha())
        #加载加分音效
        self.score_audio = pygame.mixer.Sound("audio/score.wav")
        r = random.randint(0, 1)
        if r == 0:
            self.image = self.missile  #显示导弹障碍物
            self.move = 5
            self.obstacle_y = 100   #导弹在天上
        else:
            self.image = self.pipe  #显示管道障碍物
        #根据障碍物的宽高来设置矩阵
        self.rect.size = self.image.get_size()
        self.width, self.height = self.rect.size
        self.x = 800
        self.y = self.obstacle_y
        self.rect.center = (self.x, self.y)
    def obstacle_move(self):
        self.rect.x -= self.move
    def draw_obstacle(self):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

class Music_Button():
    is_open = True
    def __init__(self):
        self.open_img = pygame.image.load("image/btn_open.png").convert_alpha()
        self.close_img = pygame.image.load("image/btn_close.png").convert_alpha()
        self.bg_music = pygame.mixer.Sound("audio/bg_music.wav")
    #判断鼠标是否在按钮上
    def is_selcect(self):
        point_x, point_y = pygame.mouse.get_pos()
        w, h = self.open_img.get_size()
        int_x = point_x > 20 and point_x < 20 + w
        int_y = point_y > 20 and point_y < 20 + h
        return int_x and int_y


#计算障碍物的时间间隔
def add_obstacle(obstacle_list,add_obstacle_time):
    if add_obstacle_time >= 1500:
        r = random.randint(0, 100)
        if r > 40:
            obstacle = Obstacle()
            obstacle_list.append(obstacle)
            return True
    for i in range(len(obstacle_list)):
        obstacle_list[i].obstacle_move()
        obstacle_list[i].draw_obstacle()


def main_game():
    score = 0  #得分
    game_over= False  #游戏结束标志
    global SCREEN, FPS_CLOCK
    pygame.init()
    #用python时钟来控制循环
    FPS_CLOCK = pygame.time.Clock()
    #创建游戏窗口
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Marie Adventure')

    #创建地图对象
    bg1 = MyMap(0, 0)
    bg2 = MyMap(800, 0)
    #创建玛丽
    marie = Marie()
    #添加障碍物的时间
    add_obstacle_time = 0
    #障碍物对象列表
    obstacle_list = []
    #创建音乐按钮
    music_button = Music_Button()
    btn_img = music_button.open_img
    music_button.bg_music.play(-1)  #循环播放背景音乐

    while True:
        #获取单机事件
        for event in pygame.event.get():
            #如果单机关闭窗口就将窗口关闭
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #按空格跳跃
            if event.type == KEYDOWN and event.key == K_SPACE:
                if marie.rect.y >= marie.lowest_y:
                    marie.jump_audio.play()
                    marie.jump()
            if event.type == pygame.MOUSEBUTTONUP:
                if music_button.is_selcect():
                    if music_button.is_open:
                        btn_img = music_button.close_img
                        music_button.is_open = False
                        music_button.bg_music.stop()
                    else:
                        btn_img = music_button.open_img
                        music_button.is_open = True
                        music_button.bg_music.play(-1)

        #无限循环滚动地图
        if game_over == False:
            #绘制地图，起更新地图作用
            bg1.map_updata()
            #地图移动
            bg1.map_rolling()
            bg2.map_updata()
            bg2.map_rolling()

            #玛丽移动
            marie.move()
            #玛丽绘制
            marie.draw()

        add_obstacle(obstacle_list,add_obstacle_time)
        add_obstacle_time += 20
        if add_obstacle(obstacle_list,add_obstacle_time):
            add_obstacle_time = 0       #重置时间

        SCREEN.blit(btn_img, (20, 20))  #绘制音乐按钮

        pygame.display.update()  #更新整个窗体
        FPS_CLOCK.tick(FPS)

if __name__ == '__main__':
    main_game()