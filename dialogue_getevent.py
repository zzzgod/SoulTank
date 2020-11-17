import pygame, time
import music
import gametank
from constant import *

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
lasttime = 0
fullscreen = 0


def getEvent(MainGame,f):
    # 获取所有事件
    eventList = pygame.event.get()
    # 遍历事件
    for event in eventList:
        # 判断按下的键是关闭还是键盘按下
        # 如果按的是退出，关闭窗口
        if event.type == pygame.QUIT:
            exit()
        # 如果是键盘的按下
        if event.type == pygame.KEYDOWN:
            # esc键切换全屏和窗口
            if event.key == pygame.K_ESCAPE:
                global fullscreen
                if fullscreen == 1:
                    pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
                    fullscreen = 0
                else:
                    pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.FULLSCREEN)
                    fullscreen = 1
            if event.key == pygame.K_RETURN:
                return f+1
            #退出游戏
            elif event.key == pygame.K_SPACE:
                MainGame.wallList.clear()
                MainGame.waterList.clear()
                MainGame.grassList.clear()
                pygame.mixer.music.stop()
                return 0
    return f
