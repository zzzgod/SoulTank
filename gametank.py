import pygame, random
import json
from constant import *
import music
import gamedrop
import gamebullet
import gamebuff


class Tank(pygame.sprite.Sprite):
    health_stick_bg_color = pygame.color.Color(79, 79, 79)
    health_stick_fg_color = pygame.color.Color(57, 229, 225)

    # 添加距离左边left 距离上边top
    def __init__(self):
        super().__init__()
        # 图片集
        self.images = None
        # 坦克的属性集
        self.status = None
        # 方向
        self.direction = 'L'
        # 根据当前图片的方向获取图片 surface
        self.image = None
        # 根据图片获取区域
        self.rect = None
        # 坐标，支持小数坐标
        self.x = 0
        self.y = 0
        # 坦克移动的开关
        self.stop = True
        # 是否活着
        self.live = True
        # 新增属性原来坐标
        self.oldLeft = 0
        self.oldTop = 0
        # 移动开关键
        self.flag = True
        # 血条框
        self.health_stick_full_rect = None
        # 是否触墙
        self.touch = 1

    # 移动
    def move(self):
        # 标记坦克是否接触边界
        self.touch = 1
        # 移动后记录原始的坐标
        self.oldLeft = self.x
        self.oldTop = self.y
        # 判断坦克的方向进行移动
        if self.direction == 'L':
            if self.x > 0:
                self.x -= self.status.tank_speed
            else:
                self.touch = 0
        elif self.direction == 'U':
            if self.y > 0:
                self.y -= self.status.tank_speed
            else:
                self.touch = 0
        elif self.direction == 'D':
            if self.y + self.rect.height < GAME_HEIGHT:
                self.y += self.status.tank_speed
            else:
                self.touch = 0
        elif self.direction == 'R':
            if self.x + self.rect.width < GAME_WIDTH:
                self.x += self.status.tank_speed
            else:
                self.touch = 0
        # 将小数坐标取整赋回
        self.rect.left = self.x
        self.rect.top = self.y
        # 更新血条框的位置
        self.health_stick_full_rect = pygame.Rect(self.x, self.y - 14, self.rect.width, 4)
        return self.touch

    # 射击
    def shot(self):
        pass

    # 停止
    def stay(self):
        self.x = self.oldLeft
        self.y = self.oldTop

    # 检测坦克是否与墙壁发生碰撞
    def hit_wall(self, MainGame):
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(self, wall):
                # 将坐标设置为移动之前的坐标
                self.stay()
        for water in MainGame.waterList:
            if pygame.sprite.collide_rect(self, water):
                # 将坐标设置为移动之前的坐标
                self.stay()
        # 和建筑的碰撞
        for arch in MainGame.enemyBatteryList:
            if pygame.sprite.collide_rect(self, arch):
                self.stay()

    # 展示坦克的方法
    def displayTank(self, MainGame):
        if self.status.health != self.status.max_health:
            # 显示血条
            pygame.draw.rect(MainGame.window, Tank.health_stick_bg_color, self.health_stick_full_rect)
            # 当前血量的比例显示血条
            health_stick_rect = self.health_stick_full_rect
            health_stick_rect.width = self.status.health / self.status.max_health * self.rect.width
            pygame.draw.rect(MainGame.window, Tank.health_stick_fg_color, health_stick_rect)
        # 获取展示的对象
        self.image = self.images[self.direction]
        # 调用blit方法展示
        MainGame.window.blit(self.image, self.rect)


# 我方坦克
class MyTank(Tank):
    def __init__(self, position):
        super(MyTank, self).__init__()
        # 读取配置文件
        f = open('entity/player/PlayerTank.json')
        tank_info = json.load(f)
        # 加载图片集
        self.images = {
            'U': pygame.image.load(tank_info['img']['Up']),
            'D': pygame.image.load(tank_info['img']['Down']),
            'L': pygame.image.load(tank_info['img']['Left']),
            'R': pygame.image.load(tank_info['img']['Right'])
        }
        # 坦克血量
        base_health = tank_info['Health']
        # 护甲
        base_armor = tank_info['Armor']
        # 速度 决定移动的快慢
        base_speed = tank_info['Speed']
        # 子弹的射速
        base_fire_rate = tank_info['FireRate']
        # 属性集
        self.status = gamebuff.Status(base_health, base_fire_rate, base_armor, base_speed)
        # 根据方向获取图片
        self.image = self.images[self.direction]
        # 区域
        self.rect = self.image.get_rect()
        # 对left和top进行赋值
        self.rect.left = position['x'] * 60
        self.rect.top = position['y'] * 60
        # 坐标，支持小数坐标
        self.x = position['x'] * 60
        self.y = position['y'] * 60
        # 血条框
        self.health_stick_full_rect = pygame.Rect(self.rect.left, self.rect.top - 14, self.rect.width, 4)
        f.close()

    # 检测我方坦克与敌方坦克发生碰撞
    def myTank_hit_enemyTank(self, MainGame):
        # 循环遍历敌方坦克列表
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(self, enemyTank):
                self.stay()


# 敌方坦克
class EnemyTank(Tank):
    def __init__(self, tank_type, left, top):
        # 调用父类的初始化方法
        super(EnemyTank, self).__init__()
        # 从文件中读取指定类型坦克的信息
        f = None
        if tank_type == 'LightTank':
            f = open('entity/enemies/LightTank.json', 'r')
        elif tank_type == 'MediumTank':
            f = open('entity/enemies/MediumTank.json', 'r')
        elif tank_type == 'HeavyTank':
            f = open('entity/enemies/HeavyTank.json', 'r')
        elif tank_type == 'HeavyTank2':
            f = open('entity/enemies/HeavyTank2.json', 'r')
        if f is not None:
            tank_info: dict = json.load(f)
            # 加载图片集
            self.images = {
                'U': pygame.image.load(tank_info['img']['Up']),
                'D': pygame.image.load(tank_info['img']['Down']),
                'L': pygame.image.load(tank_info['img']['Left']),
                'R': pygame.image.load(tank_info['img']['Right'])
            }
            # 方向,随机生成敌方坦克的方向
            self.direction = randDirection()
            # 根据方向获取图片
            self.image = self.images[self.direction]
            # 区域
            self.rect = self.image.get_rect()
            # 对left和top进行赋值
            self.rect.left = left
            self.rect.top = top
            # 坐标，支持小数坐标
            self.x = left
            self.y = top
            # 坦克血量
            base_health = tank_info['Health']
            # 护甲
            base_armor = tank_info['Armor']
            # 速度  决定移动的快慢
            base_speed = tank_info['Speed']
            # 子弹的射速
            base_fire_rate = tank_info['FireRate']
            # 属性集
            self.status = gamebuff.Status(base_health, base_fire_rate, base_armor, base_speed)
            # 下一次开炮的时间
            self.next_fire = self.status.fire_rate * random.randint(7, 13) / 10
            # 记录初始时间
            self.time = pygame.time.get_ticks()
            # 新增加一个步数变量 step
            self.step = 60
            # 保存坦克信息
            self.info = tank_info
            # 血条框
            self.health_stick_full_rect = pygame.Rect(self.rect.left, self.rect.top - 14, self.rect.width, 4)
        else:
            raise ValueError('敌方坦克类型错误！')

    # 敌方坦克随机移动的方法
    def randMove(self):
        if self.step <= 0:
            # 修改方向
            self.direction = randDirection()
            # 让步数复位
            self.step = random.randint(40, 60)
        else:
            self.touch = self.move()
            # 让步数递减
            self.step -= 1
            # 如果接触墙壁就马上转向
            if self.touch == 0:
                self.step = -1

    # 重写shot()
    def shot(self):
        now_time = pygame.time.get_ticks()
        # 如果过了开炮时间，立刻开炮
        if now_time - self.time >= self.next_fire:
            # 记录当前时间
            self.time = now_time
            # 确定下次开炮时间
            self.next_fire = self.status.fire_rate * (random.random() * 0.6 + 0.7)
            return gamebullet.EnemyTankBullet(self, self.info['Bullet'])


# 随机生成敌方坦克的方向
def randDirection():
    num = random.randint(1, 4)
    if num == 1:
        return 'U'
    elif num == 2:
        return 'D'
    elif num == 3:
        return "L"
    elif num == 4:
        return 'R'
