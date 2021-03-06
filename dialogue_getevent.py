import pygame, time
import music
import gametank
from constant import *

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
last_time = 0


def getEvent(MainGame):
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
            if event.key == pygame.K_RETURN:
                music.Music('img/press.mp3')
                return 1
            #退出游戏
            elif event.key == pygame.K_SPACE:
                MainGame.wallList.clear()
                MainGame.waterList.clear()
                MainGame.grassList.clear()
                pygame.mixer.music.stop()
                return -1
    return 0
