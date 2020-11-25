import pygame
import music
from gameExplode import Explode
from constant import *


# 子弹类
class drop:
    def __init__(self, tank):
        self.image = pygame.image.load('img/drop.gif')
        # 获取区域
        self.rect = self.image.get_rect()
        # 掉落物的状态，是否被拾取，如果被拾取，修改此状态
        self.live = True

# 子弹与坦克的碰撞
def bullet_hit_tank(bullet, MainGame, tank_type):
    if tank_type == 'EnemyTank':
        # 循环遍历敌方坦克列表，判断是否发生碰撞
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(enemyTank, bullet):
                # 修改敌方坦克和我方子弹的状态
                enemyTank.hp -= bullet.damage
                if enemyTank.hp <= 0:
                    enemyTank.live = False
                    music.Music('img/enemy1_explode.wav')
                bullet.live = False
                # 创建爆炸对象
                explode = Explode(enemyTank)
                # 将爆炸对象添加到爆炸列表中
                MainGame.explodeList.append(explode)
                break
    elif tank_type == 'PlayerTank':
        if MainGame.my_tank and MainGame.my_tank.live:
            if pygame.sprite.collide_rect(MainGame.my_tank, bullet):
                # 修改敌方子弹与我方坦克的状态
                bullet.live = False
                MainGame.my_tank.hp -= bullet.damage
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

# 展示子弹的方法
def display_bullet(Bullet, main_game):
    # 将图片surface加载到窗口
    main_game.window.blit(Bullet.image, Bullet.rect)


# 循环遍历敌方子弹列表，展示敌方子弹
def blitEnemyBullet(MainGame):
    for enemyBullet in MainGame.enemyBulletList:
        if enemyBullet.live:  # 判断敌方子弹是否存活
            display_bullet(enemyBullet, MainGame)

# 循环遍历敌方子弹列表
def checkEnemyBullet(MainGame):
    for enemyBullet in MainGame.enemyBulletList:
        if enemyBullet.live:  # 判断敌方子弹是否存活
            move(enemyBullet)
            # 调用敌方子弹与我方坦克碰撞的方法
            bullet_hit_tank(enemyBullet, MainGame, 'PlayerTank')
            # 检测敌方子弹是否与墙壁碰撞
            hit_wall(enemyBullet, MainGame, Explode)
        else:
            MainGame.enemyBulletList.remove(enemyBullet)