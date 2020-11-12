import pygame, time
import gamewall
import gametank
import gameExplode
from gamebullet import Bullet
import gamebullet
import Text
import gamegetevent
from constant import *


BG_COLOR = pygame.Color(0, 0, 0)


class MainGame:
    window = None
    my_tank = None
    # 存储敌方坦克的列表
    enemyTankList = []
    # 定义敌方坦克的数量
    enemyTankCount = 15
    # 存储我方子弹的列表
    myBulletList = []
    # 存储敌方子弹的列表
    enemyBulletList = []
    # 存储爆炸效果的列表
    explodeList = []
    explodebigList = []
    explodesmallList = []
    # 存储墙壁的列表
    wallList = []
    waterList=[]
    grassList=[]

    def __init__(self):
        pass

    # 开始游戏
    def startGame(self):
        # 加载主窗口
        # 初始化窗口
        pygame.display.init()
        # 设置窗口的大小及显示
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        # 初始化我方坦克
        gametank.createMytank(MainGame)
        # 初始化敌方坦克，并将敌方坦克添加到列表中
        gametank.createEnemyTank(MainGame)
        # 初始化墙壁
        gamewall.createWall(MainGame)
        # 设置窗口的标题
        pygame.display.set_caption('Soul Tank')
        while True:
            # 使用坦克移动的速度慢一点
            time.sleep(0.02)
            # 给窗口设置填充色
            MainGame.window.fill(BG_COLOR)
            # 获取事件
            gamegetevent.getEvent(MainGame)
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
            # 循环遍历墙壁列表，展示墙壁
            gamewall.blitWall(MainGame)
            # 循环遍历敌方坦克列表，展示敌方坦克
            gametank.blitEnemyTank(MainGame, Bullet)
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
            # 调用移动方法
            # 如果坦克的开关是开启，才可以移动
            if MainGame.my_tank and MainGame.my_tank.live:
                if not MainGame.my_tank.stop:
                    MainGame.my_tank.move()
                    # 检测我方坦克是否与墙壁发生碰撞
                    MainGame.my_tank.hit_wall(MainGame)
                    # 检测我方坦克是否与敌方坦克发生碰撞
                    MainGame.my_tank.myTank_hit_enemyTank(MainGame)
            pygame.display.update()
