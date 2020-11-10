#导入pygame模块
import pygame,time,random
import music
import gamewall
from Base import BaseItem
import gametank
from gametank import MyTank,EnemyTank
import gameExplode
from gameExplode import Explode
from gamebullet import Bullet
import gamebullet
import Text
'''
单人模式
    剧情模式
        关卡一
        二...
    小游戏
        我的坦克不能开炮
        夺旗
    生存模式
        谁笑到最后？
双人模式
    
仓库
    养成？
图鉴
    
退出
'''
SCREEN_WIDTH=1280
SCREEN_HEIGHT=720
GAME_WIDTH=1140
GAME_HEIGHT=720
BG_COLOR=pygame.Color(0,0,0)
lasttime=0
fullscreen=0

class MainGame():
    window=None
    my_tank=None
    #存储敌方坦克的列表
    enemyTankList=[]
    #定义敌方坦克的数量
    enemyTankCount=10
    #存储我方子弹的列表
    myBulletList=[]
    #存储敌方子弹的列表
    enemyBulletList=[]
    #存储爆炸效果的列表
    explodeList=[]
    explodebigList=[]
    explodesmallList=[]
    #存储墙壁的列表
    wallList=[]
    def __init__(self):
        pass
    #开始游戏
    def startGame(self):
        #加载主窗口
        #初始化窗口
        pygame.display.init()
        #设置窗口的大小及显示
        MainGame.window=pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
        #初始化我方坦克
        gametank.createMytank(MainGame)
        #初始化敌方坦克，并将敌方坦克添加到列表中
        gametank.createEnemyTank(MainGame)
        #初始化墙壁
        gamewall.createWall(MainGame)
        #设置窗口的标题
        pygame.display.set_caption('Soul Tank')
        while True:
            #使用坦克移动的速度慢一点
            time.sleep(0.02)
            #给窗口设置填充色
            MainGame.window.fill(BG_COLOR)
            #获取事件
            self.getEvent()
            #信息板
            image_imformation=pygame.image.load('img/imformation.gif')
            MainGame.window.blit(image_imformation,(1140,0))
            #绘制图标
            image_enemy_tank_num=pygame.image.load('img/enemy_tank_num_black.gif')
            MainGame.window.blit(image_enemy_tank_num,(1170,25))
            image_enemy_tank_num=pygame.image.load('img/my_tank_hp_black.gif')
            MainGame.window.blit(image_enemy_tank_num,(1170,100))
            #绘制文字
            MainGame.window.blit(Text.getTextSufaceRed('%d'%len(MainGame.enemyTankList)),(1220,35))
            #调用坦克显示的方法
            #判断我方坦克是否是否存活
            if MainGame.my_tank and MainGame.my_tank.live:
                MainGame.my_tank.displayTank(MainGame)
                if MainGame.my_tank.hp>3:
                    MainGame.window.blit(Text.getTextSufaceGreen('%d'%MainGame.my_tank.hp),(1220,110))
                elif MainGame.my_tank.hp>1:
                    MainGame.window.blit(Text.getTextSufaceYellow('%d'%MainGame.my_tank.hp),(1220,110))
                else :
                    MainGame.window.blit(Text.getTextSufaceRed('%d'%MainGame.my_tank.hp),(1220,110))
            else:
                #删除我方坦克
                del MainGame.my_tank
                MainGame.window.blit(Text.getTextSufaceRed('0'),(1220,110))
                MainGame.my_tank=None
            #循环遍历敌方坦克列表，展示敌方坦克
            gametank.blitEnemyTank(MainGame,Bullet)
            #循环遍历显示我方坦克的子弹
            gamebullet.blitMyBullet(MainGame)
            #循环遍历敌方子弹列表，展示敌方子弹
            gamebullet.blitEnemyBullet(MainGame)
            #循环遍历墙壁列表，展示墙壁
            gamewall.blitWall(MainGame)
            #循环遍历爆炸列表，展示爆炸效果
            gameExplode.blitExplode(MainGame)
            gameExplode.blitbigExplode(MainGame)
            gameExplode.blitsmallExplode(MainGame)
            #调用移动方法
            #如果坦克的开关是开启，才可以移动
            if MainGame.my_tank and MainGame.my_tank.live:
                if not MainGame.my_tank.stop:
                    MainGame.my_tank.move()
                    #检测我方坦克是否与墙壁发生碰撞
                    MainGame.my_tank.hitWall(MainGame)
                    #检测我方坦克是否与敌方坦克发生碰撞
                    MainGame.my_tank.myTank_hit_enemyTank(MainGame)

            pygame.display.update()
    #结束游戏
    def endGame(self):
        print('谢谢使用，欢迎再次使用')
        exit()
    #左上角文字的绘制

    #获取事件
    def getEvent(self):
        #获取所有事件
        eventList= pygame.event.get()
        #遍历事件
        for event in eventList:
            #判断按下的键是关闭还是键盘按下
            #如果按的是退出，关闭窗口
            if event.type == pygame.QUIT:
                self.endGame()
            #如果是键盘的按下
            if event.type == pygame.KEYDOWN:
                #esc键切换全屏和窗口
                if event.key == pygame.K_ESCAPE:
                    global fullscreen
                    if fullscreen==1:
                       pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
                       fullscreen=0
                    else:
                       pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT],pygame.FULLSCREEN)
                       fullscreen=1
                #当坦克不重在死亡
                if not MainGame.my_tank:
                   #判断按下的是1键，让坦克重生
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
                       nowtime=time.perf_counter()
                       global lasttime
                       timediffer=nowtime-lasttime
                       print(nowtime)
                       print(lasttime)
                       print(timediffer)
                       if timediffer > 1:
                           # 创建我方坦克发射的子弹
                           myBullet = Bullet(MainGame.my_tank)
                           MainGame.myBulletList.append(myBullet)
                           #我方坦克发射子弹添加音效
                           music.Music('img/fire1.wav')
                           lasttime=nowtime
            #松开方向键，坦克停止移动，修改坦克的开关状态
            if event.type == pygame.KEYUP:
                #判断松开的键是上、下、左、右时候才停止坦克移动
                if  MainGame.my_tank and MainGame.my_tank.live:
                    if (MainGame.my_tank.direction == 'U' and event.key==pygame.K_w) or(MainGame.my_tank.direction == 'L' and event.key==pygame.K_a) or(MainGame.my_tank.direction == 'D' and event.key==pygame.K_s) or(MainGame.my_tank.direction == 'R' and event.key==pygame.K_d) :
                        MainGame.my_tank.stop = True

if __name__=='__main__':
    # z yyds
    MainGame().startGame()
    # MainGame().getTextSuface()
