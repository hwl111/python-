import pygame
import sys
import random
from pygame.locals import *
from itertools import cycle

# 游戏窗口的宽度和高度
SCREENWIDTH = 822
SCREENHEIGHT = 199
FPS = 30

# 背景图片滚动类
class MyMap:
    def __init__(self, x, y):
        # 加载背景图片
        self.bg = pygame.image.load("image/bg.png").convert_alpha()
        self.x = x
        self.y = y

    def map_rolling(self):
        """控制背景图滚动"""
        if self.x < -790:
            self.x = 800
        else:
            self.x -= 5

    def map_update(self):
        """更新背景图"""
        SCREEN.blit(self.bg, (self.x, self.y))

# 玛丽角色类
class Marie:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.jumpState = False  # 是否正在跳跃
        self.jumpHeight = 130   # 跳跃高度
        self.lowest_y = 140     # 最低位置
        self.jumpValue = 0      # 跳跃值

        # 玛丽的动画
        self.marieIndex = 0
        self.marieIndexGen = cycle([0, 1, 2])

        # 加载玛丽的图片
        self.adventure_img = (
            pygame.image.load("image/adventure1.png").convert_alpha(),
            pygame.image.load("image/adventure2.png").convert_alpha(),
            pygame.image.load("image/adventure3.png").convert_alpha()
        )
        self.jump_audio = pygame.mixer.Sound("audio/jump.wav")

        self.rect.size = self.adventure_img[0].get_size()
        self.x = 50
        self.y = self.lowest_y
        self.rect.topleft = (self.x, self.y)

    def jump(self):
        """触发跳跃"""
        self.jumpState = True

    def move(self):
        """控制玛丽的跳跃与移动"""
        if self.jumpState:
            if self.rect.y >= self.lowest_y:
                self.jumpValue = -5  # 向上跳跃
            if self.rect.y <= self.lowest_y - self.jumpHeight:
                self.jumpValue = 5  # 向下回落
            self.rect.y += self.jumpValue
            if self.rect.y >= self.lowest_y:
                self.jumpState = False

    def draw(self):
        """绘制玛丽角色"""
        marieIndex = next(self.marieIndexGen)
        SCREEN.blit(self.adventure_img[marieIndex], (self.x, self.rect.y))
# 音乐控制按钮类
class MusicButton:
    def __init__(self):
        self.open_img = pygame.image.load("image/btn_open.png").convert_alpha()
        self.close_img = pygame.image.load("image/btn_close.png").convert_alpha()
        self.bg_music = pygame.mixer.Sound("audio/bg_music.wav")
        self.is_open = True

    def toggle_music(self):
        """控制音乐开关"""
        if self.is_open:
            self.bg_music.stop()
        else:
            self.bg_music.play(-1)
        self.is_open = not self.is_open

    def is_hover(self):
        """检查鼠标是否悬停在按钮上"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.open_img.get_rect(topleft=(20, 20)).collidepoint(mouse_x, mouse_y)

# 游戏结束处理
def game_over():
    bump_audio = pygame.mixer.Sound("audio/bump.wav")
    bump_audio.play()
    game_over_img = pygame.image.load("image/gameover.png").convert_alpha()
    screen_w, screen_h = pygame.display.Info().current_w, pygame.display.Info().current_h
    SCREEN.blit(game_over_img, ((screen_w - game_over_img.get_width()) / 2, (screen_h - game_over_img.get_height()) / 2))
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()


class Obstacle:
    def __init__(self):
        # 初始化障碍物
        self.missile = pygame.image.load("image/missile.png")
        self.pipe = pygame.image.load("image/pipe.png")
        self.numbers = [pygame.image.load(f"image/{i}.png").convert_alpha() for i in range(10)]
        self.score_audio = pygame.mixer.Sound("audio/score.wav")

        # 随机选择障碍物类型
        r = random.randint(0, 1)
        if r == 0:
            self.image = self.missile  # 导弹
            self.move_speed = 5
            self.obstacle_y = 100  # 导弹位置
        else:
            self.image = self.pipe  # 管道
            self.move_speed = 2
            self.obstacle_y = 150  # 管道位置

        self.rect = self.image.get_rect()
        self.rect.center = (800, self.obstacle_y)
        self.passed = False  # 是否已通过玛丽

    def move(self):
        """障碍物向左移动"""
        self.rect.x -= self.move_speed

    def draw(self):
        """绘制障碍物"""
        SCREEN.blit(self.image, self.rect.topleft)

    def get_score(self):
        """获取分数"""
        return 1

    def show_score(self, score):
        """显示当前分数"""
        score_digits = [int(x) for x in str(score)]
        total_width = sum(self.numbers[digit].get_width() for digit in score_digits)
        x_offset = SCREENWIDTH - total_width - 30

        for digit in score_digits:
            SCREEN.blit(self.numbers[digit], (x_offset, SCREENHEIGHT * 0.1))
            x_offset += self.numbers[digit].get_width()


def add_obstacle(obstacle_list, add_obstacle_time, marie, music_button, score):
    if add_obstacle_time >= 1500:
        r = random.randint(0, 100)
        if r > 40:
            obstacle = Obstacle()
            obstacle_list.append(obstacle)
            return True

    for obstacle in obstacle_list:
        obstacle.move()
        obstacle.draw()

        # 碰撞检测
        if pygame.sprite.collide_rect(marie, obstacle):
            game_over()

        # 如果障碍物完全通过玛丽，并且尚未标记为已通过，才增加分数
        if obstacle.rect.right < marie.rect.left and not obstacle.passed:
            score += obstacle.get_score()
            obstacle.passed = True  # 标记该障碍物已经通过，防止分数重复增加

        obstacle.show_score(score)


# 主游戏逻辑
def main_game():
    score = 0
    over = False
    global SCREEN, FPS_CLOCK

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Marie Adventure')

    # 创建地图、角色、障碍物等对象
    bg1 = MyMap(0, 0)
    bg2 = MyMap(800, 0)
    marie = Marie()
    music_button = MusicButton()
    obstacle_list = []

    music_button.bg_music.play(-1)

    add_obstacle_time = 0

    while not over:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE and marie.rect.y >= marie.lowest_y:
                marie.jump_audio.play()
                marie.jump()
            if event.type == pygame.MOUSEBUTTONUP and music_button.is_hover():
                music_button.toggle_music()

        # 地图滚动
        bg1.map_update()
        bg1.map_rolling()
        bg2.map_update()
        bg2.map_rolling()

        # 玛丽跳跃与绘制
        marie.move()
        marie.draw()

        # 生成障碍物
        if add_obstacle_time >= 1500:
            if random.randint(0, 100) > 40:
                obstacle = Obstacle()
                obstacle_list.append(obstacle)
            add_obstacle_time = 0

        # 更新障碍物和分数
        for obstacle in obstacle_list:
            obstacle.move()
            obstacle.draw()

            if pygame.sprite.collide_rect(marie, obstacle):
                game_over()

            if obstacle.rect.right < marie.rect.left and not obstacle.passed:
                score += obstacle.get_score()
                obstacle.passed = True

            obstacle.show_score(score)

        add_obstacle_time += 20
        SCREEN.blit(music_button.open_img if music_button.is_open else music_button.close_img, (20, 20))
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


if __name__ == '__main__':
    main_game()
