import pygame
import sys
from pygame.locals import *
from itertools import cycle   #导入迭代工具

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

        pygame.display.update()  #更新整个窗体
        FPS_CLOCK.tick(FPS)

if __name__ == '__main__':
    main_game()