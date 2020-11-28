import music
from gamebullet import MyBullet
import pygame, time
import gamewall
import gametank
import gameExplode
from gamebullet import Bullet
import gamebullet
import Text
from constant import *
import game_show_imformation
import gamemusic

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
last_time = 0
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
        game_show_imformation.show(MainGame)
        # 绘制文字
        MainGame.window.blit(Text.getTextSufaceRed('%d' % len(MainGame.enemyTankList)), (1220, 110))
        # 调用坦克显示的方法
        # 判断我方坦克是否是否存活
        if MainGame.my_tank and MainGame.my_tank.live:
            # 展示我方坦克
            MainGame.my_tank.displayTank(MainGame)
            if MainGame.my_tank.hp > 3:
                MainGame.window.blit(Text.getTextSufaceGreen('%d' % MainGame.my_tank.hp), (1220, 185))
            elif MainGame.my_tank.hp > 1:
                MainGame.window.blit(Text.getTextSufaceYellow('%d' % MainGame.my_tank.hp), (1220, 185))
            else:
                MainGame.window.blit(Text.getTextSufaceRed('%d' % MainGame.my_tank.hp), (1220, 185))
        else:
            # 删除我方坦克
            del MainGame.my_tank
            MainGame.window.blit(Text.getTextSufaceRed('0'), (1220, 185))
            MainGame.my_tank = None
        # 循环遍历墙壁列表，展示墙壁
        gamewall.blitWall(MainGame)
        # 循环遍历敌方坦克列表，展示敌方坦克
        gametank.blit_enemy_tank(MainGame, Bullet)
        # 循环遍历显示我方坦克的子弹
        gamebullet.blitMyBullet(MainGame)
        # 循环遍历敌方子弹列表，展示敌方子弹
        gamebullet.blitEnemyBullet(MainGame)
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
            # if not MainGame.my_tank:
                # 判断按下的是1键，让坦克重生
                # if event.key == pygame.K_1:
                #     # 让我方坦克重生及调用创建坦克的方法
                #     gametank.createMytank(MainGame, MainGame.map_info['Player'])
            if MainGame.my_tank and MainGame.my_tank.live:
                # 判断按下的是上、下、左、右
                if event.key == pygame.K_a:
                    # 切换方向
                    MainGame.my_tank.direction = 'L'
                    # 修改坦克的开关状态
                    MainGame.my_tank.stop = False
                    print('按下a键，坦克向左移动')
                elif event.key == pygame.K_d:
                    # 切换方向
                    MainGame.my_tank.direction = 'R'
                    # 修改坦克的开关状态
                    MainGame.my_tank.stop = False
                    print('按下d键，坦克向右移动')
                elif event.key == pygame.K_w:
                    # 切换方向
                    MainGame.my_tank.direction = 'U'
                    # 修改坦克的开关状态
                    MainGame.my_tank.stop = False
                elif event.key == pygame.K_s:
                    # 切换方向
                    MainGame.my_tank.direction = 'D'
                    # 修改坦克的开关状态
                    MainGame.my_tank.stop = False
                elif event.key == pygame.K_j:
                    # 射击间隔大于1才可以创建
                    now_time = pygame.time.get_ticks()
                    global last_time
                    time_differ = now_time - last_time
                    if time_differ > MainGame.my_tank.status.fire_rate:
                        # 判断的当前选中的是哪种炮弹
                        # 记录是否成功发射
                        flag = 0
                        my_bullet = None
                        # 当前是穿甲弹d
                        if MainGame.bullet_now == 0 and MainGame.AP_num > 0:
                            flag = 1
                            my_bullet = MyBullet(MainGame.my_tank, 'myAP75')
                            MainGame.my_tank.status.buff_bullet(my_bullet)
                            MainGame.AP_num -= 1
                        # 当前是高爆弹
                        if MainGame.bullet_now == 1 and MainGame.HE_num > 0:
                            flag = 1
                            my_bullet = MyBullet(MainGame.my_tank, 'myHE75')
                            MainGame.my_tank.status.buff_bullet(my_bullet)
                            MainGame.HE_num -= 1
                        # 当前是高爆穿甲弹
                        if MainGame.bullet_now == 2 and MainGame.APCR_num > 0:
                            flag = 1
                            my_bullet = MyBullet(MainGame.my_tank, 'myAPCR75')
                            MainGame.my_tank.status.buff_bullet(my_bullet)
                            MainGame.APCR_num -= 1
                        if flag:
                            # 创建我方坦克发射的子弹
                            MainGame.myBulletList.append(my_bullet)
                            # 我方坦克发射子弹添加音效
                            music.Music('img/fire1.wav')
                            last_time = now_time
                elif event.key == pygame.K_1:
                    # 切换至第一种炮弹
                    if MainGame.bullet_now != 0:
                        MainGame.bullet_now = 0
                        gamemusic.Music('music/change_bullet.mp3')
                elif event.key == pygame.K_2:
                    # 切换至第二种炮弹
                    if MainGame.bullet_now != 1:
                        MainGame.bullet_now = 1
                        gamemusic.Music('music/change_bullet.mp3')
                elif event.key == pygame.K_3:
                    # 切换至第三种炮弹
                    if MainGame.bullet_now != 2:
                        MainGame.bullet_now = 2
                        gamemusic.Music('music/change_bullet.mp3')
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
