import gametank
import music
import json
import gametext
import pygame
from gameExplode import Explode
from constant import *


# 子弹类
class Bullet:
    def __init__(self, tank):
        self.image = pygame.image.load('img/bullet/AP75.gif')
        # 坦克的方向决定子弹的方向
        self.direction = tank.direction
        # 获取区域
        self.rect = self.image.get_rect()
        # 子弹的状态，是否碰到墙壁，如果碰到墙壁，修改此状态
        self.live = True
        # 子弹的速度
        self.speed = 0
        # 子弹的威力
        self.damage = 0
        # 子弹的穿透力
        self.penetration = 0
        # 子弹未击穿的伤害减益
        self.damage_reduction_rate = 0
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
def hit_wall(bullet, MainGame, Explode):
    # 循环遍历墙壁列表
    for wall in MainGame.wallList:
        if pygame.sprite.collide_rect(bullet, wall):
            # 修改子弹的生存状态，让子弹消失
            bullet.live = False
            # 墙壁的生命值减小
            wall.hp -= bullet.damage
            if wall.hp <= 0:
                # 修改墙壁的生存状态
                wall.live = False
                # 产生爆炸对象
                explode = Explode(wall)
                # 将爆炸对象添加到爆炸列表中
                MainGame.explodesmallList.append(explode)


# 子弹与坦克的碰撞
def bullet_hit_tank(bullet, MainGame, tank_type):
    if tank_type == 'EnemyTank':
        # 循环遍历敌方坦克列表，判断是否发生碰撞
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(enemyTank, bullet):
                # 修改敌方坦克和我方子弹的状态
                damage = gametank.calculate_bullet_damage(enemyTank, bullet)
                enemyTank.status.health -= damage
                if enemyTank.status.health <= 0:
                    enemyTank.live = False
                    music.Music('img/enemy1_explode.wav')
                bullet.live = False
                # 创建爆炸对象
                explode = Explode(enemyTank)
                # 将爆炸对象添加到爆炸列表中
                MainGame.explodeList.append(explode)
                # 添加伤害数字特效
                sprite = gametext.FlashMessage(bullet.rect.left, bullet.rect.top, 300, str(damage), font_size=54,
                                               color=pygame.color.Color(255, 109, 29))
                MainGame.sprite_group.add(sprite)
                break
    elif tank_type == 'PlayerTank':
        if MainGame.my_tank and MainGame.my_tank.live:
            if pygame.sprite.collide_rect(MainGame.my_tank, bullet):
                # 修改敌方子弹与我方坦克的状态
                bullet.live = False
                # 如果坦克正处于隐身状态，则不受伤害
                time_now = pygame.time.get_ticks()
                if MainGame.my_tank.status.immune_t >= time_now:
                    return
                # 若处于护盾下，免疫本次伤害
                elif MainGame.my_tank.status.immune_c > 0:
                    MainGame.my_tank.status.immune_c -= 1
                    return
                damage = gametank.calculate_bullet_damage(MainGame.my_tank, bullet)
                MainGame.my_tank.status.health -= damage
                if MainGame.my_tank.status.health <= 0:
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
                    # 添加伤害数字特效
                    sprite = gametext.FlashMessage(bullet.rect.left, bullet.rect.top, 300, str(damage),
                                                   font_size=54, color=pygame.color.Color(255, 109, 29))
                    MainGame.sprite_group.add(sprite)


class MyBullet(Bullet):
    def __init__(self, tank, bullet_type):
        super(MyBullet, self).__init__(tank)
        f = None
        if bullet_type == 'myAP75':
            f = open('entity/bullet/myAP75.json')
        elif bullet_type == 'myHE75':
            f = open('entity/bullet/myHE75.json')
        elif bullet_type == 'myAPCR75':
            f = open('entity/bullet/myAPCR75.json')
        else:
            raise ValueError('找不到指定的子弹种类。')
        if f is not None:
            bullet_info: dict = json.load(f)
            # 子弹的贴图
            self.image = pygame.image.load(bullet_info['img'])
            # 子弹的速度
            self.speed = bullet_info['Speed']
            # 子弹的威力
            self.damage = bullet_info['Damage']
            # 子弹的穿透力
            self.penetration = bullet_info['Penetration']
            # 子弹未击穿的伤害减益
            self.damage_reduction_rate = bullet_info['DamageReductionRate']
            f.close()
        else:
            raise TypeError('玩家子弹类型错误！')


class EnemyBullet(Bullet):
    def __init__(self, tank, bullet_type):
        super(EnemyBullet, self).__init__(tank)
        f = None
        if bullet_type == 'AP57':
            f = open('entity/bullet/AP57.json')
        elif bullet_type == 'AP75':
            f = open('entity/bullet/AP75.json')
        elif bullet_type == 'AP88':
            f = open('entity/bullet/AP88.json')
        elif bullet_type == 'AP122':
            f = open('entity/bullet/AP122.json')
        if f is not None:
            bullet_info: dict = json.load(f)
            # 子弹的贴图
            self.image = pygame.image.load(bullet_info['img'])
            # 子弹的速度
            self.speed = bullet_info['Speed']
            # 子弹的威力
            self.damage = bullet_info['Damage']
            # 子弹的穿透力
            self.penetration = bullet_info['Penetration']
            # 子弹未击穿的伤害减益
            self.damage_reduction_rate = bullet_info['DamageReductionRate']
            f.close()
        else:
            raise TypeError('敌方子弹类型错误！')


# 移动
def move(bullet):
    if bullet.direction == 'U':
        if bullet.rect.top > 0:
            bullet.rect.top -= bullet.speed
        else:
            # 修改子弹的状态
            bullet.live = False
    elif bullet.direction == 'R':
        if bullet.rect.left + bullet.rect.width < GAME_WIDTH:
            bullet.rect.left += bullet.speed
        else:
            # 修改子弹的状态
            bullet.live = False
    elif bullet.direction == 'D':
        if bullet.rect.top + bullet.rect.height < GAME_HEIGHT:
            bullet.rect.top += bullet.speed
        else:
            # 修改子弹的状态
            bullet.live = False
    elif bullet.direction == 'L':
        if bullet.rect.left > 0:
            bullet.rect.left -= bullet.speed
        else:
            # 修改子弹的状态
            bullet.live = False


# 展示子弹的方法
def display_bullet(Bullet, main_game):
    # 将图片surface加载到窗口
    main_game.window.blit(Bullet.image, Bullet.rect)


# 循环遍历我方子弹存储列表
def blitMyBullet(MainGame):
    for myBullet in MainGame.myBulletList:
        # 判断当前的子弹是否是活着状态，如果是则进行显示
        if myBullet.live:
            display_bullet(myBullet, MainGame)


# 循环遍历我方子弹存储列表
def checkMyBullet(MainGame):
    for myBullet in MainGame.myBulletList:
        # 判断当前的子弹是否是活着状态，如果是则进行移动，
        if myBullet.live:
            # 调用子弹的移动方法
            move(myBullet)
            # 调用检测我方子弹是否与敌方坦克发生碰撞
            bullet_hit_tank(myBullet, MainGame, 'EnemyTank')
            # 检测我方子弹是否与墙壁碰撞
            hit_wall(myBullet, MainGame, Explode)
        # 否则在列表中删除
        else:
            MainGame.myBulletList.remove(myBullet)


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
