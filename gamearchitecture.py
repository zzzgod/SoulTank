import json
import math
import gametank
import pygame
import gamebullet
import random
import gametext
import music
from constant import health_stick_fg_color, health_stick_bg_color


class Architecture(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 生命值
        self.health = 0
        self.max_health = 1
        # 图片
        self.image = None
        # 碰撞框
        self.rect =None
        # 坐标
        self.x = 0
        self.y = 0
        # 长度，宽度
        self.width = 0
        self.height = 0
        # 血条背景
        self.health_stick_full_rect = None
        # 宽度
        self.width = 0
        # 高度
        self.height = 0
        # 护甲
        self.armor = 0
        # 图片
        self.image = None
        # 活着
        self.live = True


class Battery(Architecture):
    def __init__(self, arch_type, left, top):
        super(Battery, self).__init__()
        # 设置位置坐标
        self.x = left
        self.y = top
        # 角度，逆时针，竖直向上为0度
        self.angle = 0
        f = None
        # 读取配置信息
        if arch_type == 'Battery':
            f = open('entity/architecture/battery.json')
        if f is not None:
            self.info = json.load(f)
            self.width = self.info['Width'] * 60
            self.height = self.info['Height'] * 60
            self.health = self.info['Health']
            self.max_health = self.health
            self.bullet = self.info['Bullet']
            self.fire_rate = self.info['FireRate']
            self.armor = self.info['Armor']
            self.initial_image = pygame.image.load(self.info['img'])
            self.image = self.initial_image
        else:
            raise ValueError('不合法的建筑名。')
        # 记录初始时间
        self.time = pygame.time.get_ticks()
        # 初始化下次开火的时间
        self.next_fire = self.fire_rate * (random.random() * 0.6 + 0.7)
        # 碰撞框
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
        # 初始中心
        self.center = self.rect.center
        # 更新血条框的位置
        self.health_stick_full_rect = pygame.Rect(self.x, self.y - 14, self.width, 4)

    def aim(self, tank: gametank.Tank):
        # 计算坦克中心位置
        tank_center_x = tank.rect.left + tank.rect.width / 2
        tank_center_y = tank.rect.top + tank.rect.height / 2
        # 计算x轴，y轴上的距离
        delta_x = tank_center_x - self.center[0]
        delta_y = tank_center_y - self.center[1]
        # 计算偏转角度的弧度值
        angle = math.atan2(delta_x, delta_y)
        # 转换成角度
        self.angle = (angle * 180 / math.pi + 360) % 360 + 180
        self.image = pygame.transform.rotate(self.initial_image, self.angle)
        rect = self.image.get_rect(center=self.center)
        return rect

    def display(self, MainGame):
        if self.health != self.max_health:
            # 显示血条
            pygame.draw.rect(MainGame.window, health_stick_bg_color, self.health_stick_full_rect)
            # 当前血量的比例显示血条
            health_stick_rect = self.health_stick_full_rect
            health_stick_rect.width = self.health / self.max_health * self.width
            pygame.draw.rect(MainGame.window, health_stick_fg_color, health_stick_rect)
        # 瞄准，获得当前图片位置
        rect = self.aim(MainGame.my_tank)
        # 调用blit方法展示
        MainGame.window.blit(self.image, (rect.left, rect.top))

    def shot(self):
        now_time = pygame.time.get_ticks()
        # 如果过了开炮时间，立刻开炮
        if now_time - self.time >= self.next_fire:
            # 记录当前时间
            self.time = now_time
            # 确定下次开炮时间
            self.next_fire = self.fire_rate * (random.random() * 0.6 + 0.7)
            return EnemyBatteryBullet(self, self.bullet)


class EnemyBatteryBullet(gamebullet.Bullet):
    def __init__(self, arch: Battery, bullet_type):
        super(EnemyBatteryBullet, self).__init__()
        f = None
        if bullet_type == 'AP203':
            f = open('entity/bullet/AP203.json')
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
        # 获取方向(弧度)
        self.angle = arch.angle * math.pi / 180
        # 设置初始位置
        self.rect.left = arch.center[0] - math.sin(self.angle) * 60
        self.rect.top = arch.center[1] - math.cos(self.angle) * 60
        # 获取速度分量
        self.speed_x = -math.sin(self.angle) * self.speed
        self.speed_y = -math.cos(self.angle) * self.speed
        # 可以穿墙
        self.cross_wall = True

    # 移动
    def move(self):
        self.rect.left += self.speed_x
        self.rect.top += self.speed_y

