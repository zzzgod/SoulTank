import pygame, random
import json
from constant import *
import music
import gamedrop
import gamebullet


class Tank:
    health_stick_bg_color = pygame.color.Color(79, 79, 79)
    health_stick_fg_color = pygame.color.Color(57, 229, 225)

    # 添加距离左边left 距离上边top
    def __init__(self):
        # 图片集
        self.images = None
        # 血量
        self.max_hp = 1
        self.hp = 0
        # 护甲
        self.armor = 0
        # 速度
        self.speed = 0
        # 子弹的射速
        self.fire_rate = 1
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
                self.x -= self.speed
            else:
                self.touch = 0
        elif self.direction == 'U':
            if self.y > 0:
                self.y -= self.speed
            else:
                self.touch = 0
        elif self.direction == 'D':
            if self.y + self.rect.height < GAME_HEIGHT:
                self.y += self.speed
            else:
                self.touch = 0
        elif self.direction == 'R':
            if self.x + self.rect.width < GAME_WIDTH:
                self.x += self.speed
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
        return gamebullet.Bullet(self)

    #
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

    # 展示坦克的方法
    def displayTank(self, MainGame):
        if self.hp != self.max_hp:
            # 显示血条
            pygame.draw.rect(MainGame.window, Tank.health_stick_bg_color, self.health_stick_full_rect)
            # 当前血量的比例显示血条
            health_stick_rect = self.health_stick_full_rect
            health_stick_rect.width = self.hp / self.max_hp * self.rect.width
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
        self.hp = tank_info['Health']
        self.max_hp = self.hp
        # 护甲
        self.armor = tank_info['Armor']
        # 速度 决定移动的快慢
        self.speed = tank_info['Speed']
        # 子弹的射速
        self.fire_rate = tank_info['FireRate']
        # 根据方向获取图片
        self.image = self.images[self.direction]
        # 区域
        self.rect = self.image.get_rect()
        # 对left和top进行赋值
        self.rect.left = position['x']
        self.rect.top = position['y']
        # 坐标，支持小数坐标
        self.x = position['x']
        self.y = position['y']
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
            self.hp = tank_info['Health']
            self.max_hp = self.hp
            # 护甲
            self.armor = tank_info['Armor']
            # 速度  决定移动的快慢
            self.speed = tank_info['Speed']
            # 子弹的射速
            self.fire_rate = tank_info['FireRate']
            # 下一次开炮的时间
            self.next_fire = self.fire_rate * random.randint(7, 13) / 10
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
            self.step = random.randint(1, 60)
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
            self.next_fire = self.fire_rate * (random.random() * 0.6 + 0.7)
            return gamebullet.EnemyBullet(self, self.info['Bullet'])


# 敌方坦克与我方坦克是否发生碰撞
def enemyTank_hit_myTank(enemyTank, MainGame):
    if pygame.sprite.collide_rect(enemyTank, MainGame.my_tank):
        enemyTank.stay()


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


# 创建我方坦克的方法
def createMytank(MainGame, tank_info: dict):
    MainGame.my_tank = MyTank(tank_info)
    music.Music('img/start.wav')


# 初始化敌方坦克，并将敌方坦克添加到列表中
def createEnemyTank(MainGame, tank_info: dict):
    for tank in tank_info:
        if tank['EnemyType'] == "Light":
            enemy = EnemyTank('LightTank', tank['x'], tank['y'])
            MainGame.enemyTankList.append(enemy)
        elif tank['EnemyType'] == "Middle":
            enemy = EnemyTank('MediumTank', tank['x'], tank['y'])
            MainGame.enemyTankList.append(enemy)
        elif tank['EnemyType'] == "Heavy":
            enemy = EnemyTank('HeavyTank', tank['x'], tank['y'])
            MainGame.enemyTankList.append(enemy)
        elif tank['EnemyType'] == "Heavy2":
            enemy = EnemyTank('HeavyTank2', tank['x'], tank['y'])
            MainGame.enemyTankList.append(enemy)


# 循环遍历敌方坦克列表，展示敌方坦克
def blitEnemyTank(MainGame, Bullet):
    for enemyTank in MainGame.enemyTankList:
        # 判断当前敌方坦克是否活着
        if enemyTank.live:
            enemyTank.displayTank(MainGame)


# 循环遍历敌方坦克列表，检查敌方坦克
def checkEnemyTank(MainGame, Bullet):
    for enemyTank in MainGame.enemyTankList:
        # 判断当前敌方坦克是否活着
        if enemyTank.live:
            enemyTank.randMove()
            # 调用检测是否与墙壁碰撞
            enemyTank.hit_wall(MainGame)
            # 检测敌方坦克是否与我方坦克发生碰撞
            if MainGame.my_tank and MainGame.my_tank.live:
                enemyTank_hit_myTank(enemyTank, MainGame)
            # 发射子弹
            enemyBullet = enemyTank.shot()
            # 敌方子弹是否是None，如果不为None则添加到敌方子弹列表中
            if enemyBullet:
                # 将敌方子弹存储到敌方子弹列表中
                MainGame.enemyBulletList.append(enemyBullet)
        else:  # 不活着，从敌方坦克列表中移除
            # 添加掉落物
            MainGame.dropList.append(gamedrop.Drop(enemyTank, 'AddBullet'))
            MainGame.enemyTankList.remove(enemyTank)


# 计算子弹伤害
def calculate_bullet_damage(tank: Tank, bullet: gamebullet.Bullet):
    # 子弹穿透力
    penetration = bullet.penetration * (random.random() * 0.4 + 0.8)
    # 基础伤害
    damage = bullet.damage * (random.random() * 0.4 + 0.8)
    # 未击穿的伤害减益
    if penetration < tank.armor:
        damage *= bullet.damage_reduction_rate
    # 对伤害取整
    damage = int(damage)
    return damage
