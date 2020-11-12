import pygame
import music
from gameExplode import Explode
from constant import *


# 子弹类
class Bullet:
    def __init__(self, tank):
        self.image = pygame.image.load('img/enemymissile.gif')
        # 坦克的方向决定子弹的方向
        self.direction = tank.direction
        # 获取区域
        self.rect = self.image.get_rect()
        # 子弹的状态，是否碰到墙壁，如果碰到墙壁，修改此状态
        self.live = True
        # 子弹的left和top与方向有关
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


    # 子弹是否碰撞墙壁
    def hit_wall(self, MainGame, Explode):
        # 循环遍历墙壁列表
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(self, wall):
                # 修改子弹的生存状态，让子弹消失
                self.live = False
                # 墙壁的生命值减小
                wall.hp -= 1
                if wall.hp <= 0:
                    # 修改墙壁的生存状态
                    wall.live = False
                    # 产生爆炸对象
                    explode = Explode(wall)
                    # 将爆炸对象添加到爆炸列表中
                    MainGame.explodesmallList.append(explode)



    # 子弹与坦克的碰撞
    def bullet_hit_tank(self, MainGame, tank_type):
        if tank_type == 'EnemyTank':
            # 循环遍历敌方坦克列表，判断是否发生碰撞
            for enemyTank in MainGame.enemyTankList:
                if pygame.sprite.collide_rect(enemyTank, self):
                    # 修改敌方坦克和我方子弹的状态
                    enemyTank.hp -= 1
                    if enemyTank.hp <= 99:
                        enemyTank.live = False
                        music.Music('img/enemy1_explode.wav')
                    self.live = False
                    # 创建爆炸对象
                    explode = Explode(enemyTank)
                    # 将爆炸对象添加到爆炸列表中
                    MainGame.explodeList.append(explode)
        elif tank_type == 'PlayerTank':
            if MainGame.my_tank and MainGame.my_tank.live:
                if pygame.sprite.collide_rect(MainGame.my_tank, self):
                    # 修改敌方子弹与我方坦克的状态
                    self.live = False
                    MainGame.my_tank.hp -= 1
                    if MainGame.my_tank.hp <= 0:
                        MainGame.my_tank.live = False
                        # 产生爆炸对象
                        explode = Explode(MainGame.my_tank)
                        # 将爆炸对象添加到爆炸列表中
                        MainGame.explodebigList.append(explode)
                    else:
                        # 产生爆炸对象
                        explode = Explode(MainGame.my_tank)
                        # 将爆炸对象添加到爆炸列表中
                        MainGame.explodeList.append(explode)
class AP_my_1(Bullet):
    def __init__(self,tank):
        super(AP_my_1, self).__init__(tank)
        #子弹的贴图
        self.image = pygame.image.load('img/tankmissile.gif')
        # 子弹的速度
        self.speed = 10
        #子弹的威力
        self.damage = 1
        #子弹的穿透力
        self.penetration = 10

class AP_enemy_1(Bullet):
    def __init__(self,tank):
        super(AP_enemy_1, self).__init__(tank)
        #子弹的贴图
        self.image = pygame.image.load('img/enemymissile.gif')
        # 子弹的速度
        self.speed = 6
        #子弹的威力
        self.damage = 1
        #子弹的穿透力
        self.penetration = 10




 # 移动
def move(Bullet):
        if Bullet.direction == 'U':
            if Bullet.rect.top > 0:
                Bullet.rect.top -= Bullet.speed
            else:
                # 修改子弹的状态
                Bullet.live = False
        elif Bullet.direction == 'R':
            if Bullet.rect.left + Bullet.rect.width < GAME_WIDTH:
                Bullet.rect.left += Bullet.speed
            else:
                # 修改子弹的状态
                Bullet.live = False
        elif Bullet.direction == 'D':
            if Bullet.rect.top + Bullet.rect.height < GAME_HEIGHT:
                Bullet.rect.top += Bullet.speed
            else:
                # 修改子弹的状态
                Bullet.live = False
        elif Bullet.direction == 'L':
            if Bullet.rect.left > 0:
                Bullet.rect.left -= Bullet.speed
            else:
                # 修改子弹的状态
                Bullet.live = False

# 展示子弹的方法
def display_bullet(Bullet, main_game):
        # 将图片surface加载到窗口
            main_game.window.blit(Bullet.image, Bullet.rect)

# 循环遍历我方子弹存储列表
def blitMyBullet(MainGame):
    for myBullet in MainGame.myBulletList:
        # 判断当前的子弹是否是活着状态，如果是则进行显示及移动，
        if myBullet.live:
            display_bullet(myBullet,MainGame)
            # 调用子弹的移动方法
            move(myBullet)
            # 调用检测我方子弹是否与敌方坦克发生碰撞
            myBullet.bullet_hit_tank(MainGame, 'EnemyTank')
            # 检测我方子弹是否与墙壁碰撞
            myBullet.hit_wall(MainGame, Explode)
        # 否则在列表中删除
        else:
            MainGame.myBulletList.remove(myBullet)


# 循环遍历敌方子弹列表，展示敌方子弹
def blitEnemyBullet(MainGame):
    for enemyBullet in MainGame.enemyBulletList:
        if enemyBullet.live:  # 判断敌方子弹是否存活
            display_bullet(enemyBullet,MainGame)
            move(enemyBullet)
            # 调用敌方子弹与我方坦克碰撞的方法
            enemyBullet.bullet_hit_tank(MainGame, 'PlayerTank')
            # 检测敌方子弹是否与墙壁碰撞
            enemyBullet.hit_wall(MainGame, Explode)
        else:
            MainGame.enemyBulletList.remove(enemyBullet)
