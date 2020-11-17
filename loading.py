import pygame, time
from constant import *
import Text

BG_COLOR = pygame.Color(0, 0, 0)


def load():
    window = None
    pygame.display.init()
    # 设置窗口的大小及显示
    window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    # 设置窗口的标题
    pygame.display.set_caption('Soul Tank')
    T = 0
    while True:
        # 刷新次数
        T += 1
        if T == 50:
            break
        # 刷新频率
        time.sleep(0.02)
        window.fill(BG_COLOR)
        # 获取事件
        image_main_background = pygame.image.load('img/main_background.gif')
        window.blit(image_main_background, (0, 0))
        window.blit(Text.getTextSufaceBlackbig("Loading..."), (550, 650))
        pygame.display.update()
