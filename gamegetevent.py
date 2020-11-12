import pygame, time
import music
import gametank
from gamebullet import AP_my_75
from constant import *

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
lasttime = 0
fullscreen = 0


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
            # esc键切换全屏和窗口
            if event.key == pygame.K_ESCAPE:
                global fullscreen
                if fullscreen == 1:
                    pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
                    fullscreen = 0
                else:
                    pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.FULLSCREEN)
                    fullscreen = 1
            # 当坦克不重在死亡
            if not MainGame.my_tank:
                # 判断按下的是1键，让坦克重生
                if event.key == pygame.K_1:
                    # 让我方坦克重生及调用创建坦克的方法
                    gametank.createMytank(MainGame)
            if MainGame.my_tank and MainGame.my_tank.live:
                # 判断按下的是上、下、左、右
                if event.key == pygame.K_a:
                    # 切换方向
                    MainGame.my_tank.direction = 'L'
                    # 修改坦克的开关状态
                    MainGame.my_tank.stop = False
                    # MainGame.my_tank.move()
                    print('按下a键，坦克向左移动')
                elif event.key == pygame.K_d:
                    # 切换方向
                    MainGame.my_tank.direction = 'R'
                    # 修改坦克的开关状态
                    MainGame.my_tank.stop = False
                    # MainGame.my_tank.move()
                    print('按下d键，坦克向右移动')
                elif event.key == pygame.K_w:
                    # 切换方向
                    MainGame.my_tank.direction = 'U'
                    # 修改坦克的开关状态
                    MainGame.my_tank.stop = False
                    # MainGame.my_tank.move()
                    print('按下w键，坦克向上移动')
                elif event.key == pygame.K_s:
                    # 切换方向
                    MainGame.my_tank.direction = 'D'
                    # 修改坦克的开关状态
                    MainGame.my_tank.stop = False
                    # MainGame.my_tank.move()
                    print('按下s键，坦克向下移动')
                elif event.key == pygame.K_j:
                    print('发射子弹')
                    # 如果当前我方子弹列表的大小 射击间隔大于1才可以创建
                    nowtime = time.perf_counter()
                    global lasttime
                    timediffer = nowtime - lasttime
                    print(nowtime)
                    print(lasttime)
                    print(timediffer)
                    if timediffer > 1:
                        # 创建我方坦克发射的子弹
                        myBullet = AP_my_75(MainGame.my_tank)
                        MainGame.myBulletList.append(myBullet)
                        # 我方坦克发射子弹添加音效
                        music.Music('img/fire1.wav')
                        lasttime = nowtime
        # 松开方向键，坦克停止移动，修改坦克的开关状态
        if event.type == pygame.KEYUP:
            # 判断松开的键是上、下、左、右时候才停止坦克移动
            if MainGame.my_tank and MainGame.my_tank.live:
                if (MainGame.my_tank.direction == 'U' and event.key == pygame.K_w) or (
                        MainGame.my_tank.direction == 'L' and event.key == pygame.K_a) or (
                        MainGame.my_tank.direction == 'D' and event.key == pygame.K_s) or (
                        MainGame.my_tank.direction == 'R' and event.key == pygame.K_d):
                    MainGame.my_tank.stop = True
