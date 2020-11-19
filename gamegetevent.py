import pygame, time
import music
import gametank
from gamebullet import MyBullet
from constant import *
import json
import pygame, time
import gamewall
import gametank
import gameExplode
from gamebullet import Bullet
import gamebullet
import Text
import gamegetevent
from constant import *
from gamevictory import victory

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
lasttime = 0
fullscreen = 0
BG_COLOR = pygame.Color(0, 0, 0)

def pause_menu(MainGame):
    # 加载图片
    pause_img = pygame.image.load('img/interface/PauseMenu.png')
    while True:
        # 使用坦克移动的速度慢一点
        time.sleep(0.02)
        # 给窗口设置填充色
        MainGame.window.fill(BG_COLOR)
        # 获取所有事件
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                return
        # 信息板
        image_imformation = pygame.image.load('img/imformation.gif')
        MainGame.window.blit(image_imformation, (1140, 0))
        # 绘制图标
        image_enemy_tank_num = pygame.image.load('img/enemy_tank_num_black.gif')
        MainGame.window.blit(image_enemy_tank_num, (1170, 25))
        image_enemy_tank_num = pygame.image.load('img/my_tank_hp_black.gif')
        MainGame.window.blit(image_enemy_tank_num, (1170, 100))
        # 绘制文字
        MainGame.window.blit(Text.getTextSufaceRed('%d' % len(MainGame.enemyTankList)), (1220, 35))
        # 调用坦克显示的方法
        # 判断我方坦克是否是否存活
        if MainGame.my_tank and MainGame.my_tank.live:
            # 展示我方坦克
            MainGame.my_tank.displayTank(MainGame)
            if MainGame.my_tank.hp > 3:
                MainGame.window.blit(Text.getTextSufaceGreen('%d' % MainGame.my_tank.hp), (1220, 110))
            elif MainGame.my_tank.hp > 1:
                MainGame.window.blit(Text.getTextSufaceYellow('%d' % MainGame.my_tank.hp), (1220, 110))
            else:
                MainGame.window.blit(Text.getTextSufaceRed('%d' % MainGame.my_tank.hp), (1220, 110))
        else:
            # 删除我方坦克
            del MainGame.my_tank
            MainGame.window.blit(Text.getTextSufaceRed('0'), (1220, 110))
            MainGame.my_tank = None
        # 循环遍历敌方坦克列表，展示敌方坦克
        gametank.blitEnemyTank(MainGame, Bullet)
        # 循环遍历显示我方坦克的子弹
        gamebullet.blitMyBullet(MainGame)
        # 循环遍历敌方子弹列表，展示敌方子弹
        gamebullet.blitEnemyBullet(MainGame)
        # 循环遍历墙壁列表，展示墙壁
        gamewall.blitWall(MainGame)
        # 循环遍历草列表，展示草
        gamewall.blitGrass(MainGame)
        # 循环遍历爆炸列表，展示爆炸效果
        gameExplode.blitExplode(MainGame)
        gameExplode.blitbigExplode(MainGame)
        gameExplode.blitsmallExplode(MainGame)
        MainGame.window.blit(pause_img, (0, 0))
        pygame.display.update()


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
        elif event.type == pygame.KEYDOWN:
            # 如果处于暂停状态
            if event.key == pygame.K_p:
                pause_menu(MainGame)
            # esc键切换全屏和窗口
            if event.key == pygame.K_ESCAPE:
                global fullscreen
                if fullscreen == 1:
                    pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
                    fullscreen = 0
                else:
                    pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.FULLSCREEN)
                    fullscreen = 1
            # 退出游戏
            elif event.key == pygame.K_BACKSPACE:
                MainGame.enemyTankList.clear()
                MainGame.myBulletList.clear()
                MainGame.enemyBulletList.clear()
                MainGame.explodeList.clear()
                MainGame.explodebigList.clear()
                MainGame.explodesmallList.clear()
                MainGame.wallList.clear()
                MainGame.waterList.clear()
                MainGame.grassList.clear()
                pygame.mixer.music.stop()
                return True
            # 当坦克不重在死亡
            if not MainGame.my_tank:
                # 判断按下的是1键，让坦克重生
                if event.key == pygame.K_1:
                    # 让我方坦克重生及调用创建坦克的方法
                    gametank.createMytank(MainGame, MainGame.map_info['Player'])
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
                        myBullet = MyBullet(MainGame.my_tank, 'myAP75')
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
    return False
