import gametank
import music
import json
import gametext
import math
import pygame
from gameExplode import Explode
from constant import *


# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = None
        # 子弹的方向
        self.direction = None
        # rect
        self.rect = None
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
        # 子弹是否能穿墙
        self.cross_wall = False

    def move(self):
        pass


class MyBullet(Bullet):
    def __init__(self, tank, bullet_type):
        super(MyBullet, self).__init__()
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
        # 获取区域
        self.rect = self.image.get_rect()
        # 获取方向
        self.direction = tank.direction
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

    # 移动
    def move(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                # 修改子弹的状态
                self.live = False
        elif self.direction == 'R':
            if self.rect.left + self.rect.width < GAME_WIDTH:
                self.rect.left += self.speed
            else:
                # 修改子弹的状态
                self.live = False
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < GAME_HEIGHT:
                self.rect.top += self.speed
            else:
                # 修改子弹的状态
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                # 修改子弹的状态
                self.live = False


class EnemyTankBullet(Bullet):
    def __init__(self, tank, bullet_type):
        super(EnemyTankBullet, self).__init__()
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
        # 获取区域
        self.rect = self.image.get_rect()
        # 获取方向
        self.direction = tank.direction
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

    # 移动
    def move(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                # 修改子弹的状态
                self.live = False
        elif self.direction == 'R':
            if self.rect.left + self.rect.width < GAME_WIDTH:
                self.rect.left += self.speed
            else:
                # 修改子弹的状态
                self.live = False
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < GAME_HEIGHT:
                self.rect.top += self.speed
            else:
                # 修改子弹的状态
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                # 修改子弹的状态
                self.live = False
