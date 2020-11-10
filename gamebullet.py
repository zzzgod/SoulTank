import pygame
import music
from Base import BaseItem
from gameExplode import Explode
GAME_WIDTH=1140
GAME_HEIGHT=720

#子弹类
class Bullet(BaseItem):
    def __init__(self,tank):
        #加载图片
        self.image=pygame.image.load('img/enemymissile.gif')
        self.image_my=pygame.image.load('img/tankmissile.gif')
        #坦克的方向决定子弹的方向
        self.direction=tank.direction
        #获取区域
        self.rect=self.image.get_rect()
        #子弹的left和top与方向有关
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        #子弹的速度
        self.speed=6
        #子弹的状态，是否碰到墙壁，如果碰到墙壁，修改此状态
        self.live=True
    #移动
    def move(self):
        if self.direction == 'U':
            if self.rect.top>0:
                self.rect.top-=self.speed
            else:
                #修改子弹的状态
                self.live=False
        elif self.direction == 'R':
            if self.rect.left+self.rect.width<GAME_WIDTH:
                self.rect.left+=self.speed
            else:
                #修改子弹的状态
                self.live=False
        elif self.direction =='D':
            if self.rect.top+self.rect.height<GAME_HEIGHT:
                self.rect.top+=self.speed
            else:
                #修改子弹的状态
                self.live=False
        elif self.direction == 'L':
            if self.rect.left>0:
                self.rect.left-=self.speed
            else:
                #修改子弹的状态
                self.live=False
    #子弹是否碰撞墙壁
    def hitWall(self,MainGame,Explode):
        #循环遍历墙壁列表
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(self,wall):
                #修改子弹的生存状态，让子弹消失
                self.live=False
                #墙壁的生命值减小
                wall.hp-=1
                if wall.hp<=0:
                    #修改墙壁的生存状态
                    wall.live=False
                    # 产生爆炸对象
                    explode = Explode(wall)
                    # 将爆炸对象添加到爆炸列表中
                    MainGame.explodesmallList.append(explode)





    #展示子弹的方法
    def displayBullet(self,MainGame):
        #将图片surface加载到窗口
        MainGame.window.blit(self.image,self.rect)

    def display_my_Bullet(self,MainGame):
        #将图片surface加载到窗口
        MainGame.window.blit(self.image_my,self.rect)
    #我方子弹与敌方坦克的碰撞
    def myBullet_hit_enemyTank(self,MainGame,Explode):
        #循环遍历敌方坦克列表，判断是否发生碰撞
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(enemyTank,self):
                #修改敌方坦克和我方子弹的状态
                enemyTank.hp-=1
                if enemyTank.hp<=99:
                    enemyTank.live=False
                    music.Music('img/enemy1_explode.wav')
                self.live=False
                #创建爆炸对象
                explode=Explode(enemyTank)
                #将爆炸对象添加到爆炸列表中
                MainGame.explodeList.append(explode)
    #敌方子弹与我方坦克的碰撞
    def enemyBullet_hit_myTank(self,MainGame,Explode):
        if MainGame.my_tank and MainGame.my_tank.live:
            if pygame.sprite.collide_rect(MainGame.my_tank, self):
                # 修改敌方子弹与我方坦克的状态
                self.live = False
                MainGame.my_tank.hp-=1
                if MainGame.my_tank.hp<=0:
                    MainGame.my_tank.live=False
                    # 产生爆炸对象
                    explode = Explode(MainGame.my_tank)
                    # 将爆炸对象添加到爆炸列表中
                    MainGame.explodebigList.append(explode)
                else:
                    # 产生爆炸对象
                    explode = Explode(MainGame.my_tank)
                    # 将爆炸对象添加到爆炸列表中
                    MainGame.explodeList.append(explode)

#循环遍历我方子弹存储列表
def blitMyBullet(MainGame):
    for myBullet in MainGame.myBulletList:
        #判断当前的子弹是否是活着状态，如果是则进行显示及移动，
        if myBullet.live:
            myBullet.display_my_Bullet(MainGame)
            # 调用子弹的移动方法
            myBullet.move()
            #调用检测我方子弹是否与敌方坦克发生碰撞
            myBullet.myBullet_hit_enemyTank(MainGame,Explode)
            # 检测我方子弹是否与墙壁碰撞
            myBullet.hitWall(MainGame,Explode)
        # 否则在列表中删除
        else:
            MainGame.myBulletList.remove(myBullet)

# 循环遍历敌方子弹列表，展示敌方子弹
def blitEnemyBullet(MainGame):
    for enemyBullet in MainGame.enemyBulletList:
        if enemyBullet.live: #判断敌方子弹是否存活
            enemyBullet.displayBullet(MainGame)
            enemyBullet.move()
            #调用敌方子弹与我方坦克碰撞的方法
            enemyBullet.enemyBullet_hit_myTank(MainGame,Explode)
            #检测敌方子弹是否与墙壁碰撞
            enemyBullet.hitWall(MainGame,Explode)
        else:
            MainGame.enemyBulletList.remove(enemyBullet)