import pygame, random
from constant import *
import music


class Tank():
    # 添加距离左边left 距离上边top
    def __init__(self, left, top):
        # 保存加载的图片
        self.images = {
            'U': pygame.image.load('img/p1tankU.gif'),
            'D': pygame.image.load('img/p1tankD.gif'),
            'L': pygame.image.load('img/p1tankL.gif'),
            'R': pygame.image.load('img/p1tankR.gif'),
        }
        # 方向
        self.direction = 'L'
        # 根据当前图片的方向获取图片 surface
        self.image = self.images[self.direction]
        # 根据图片获取区域
        self.rect = self.image.get_rect()
        # 设置区域的left 和top
        self.rect.left = left
        self.rect.top = top
        # 速度  决定移动的快慢
        self.speed = 5
        # 坦克移动的开关
        self.stop = True
        # 是否活着
        self.live = True
        # 新增属性原来坐标
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top

    # 移动
    def move(self):
        # 标记坦克是否接触边界
        self.touch = 1
        # 移动后记录原始的坐标
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top
        # 判断坦克的方向进行移动
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.touch = 0
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.touch = 0
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < GAME_HEIGHT:
                self.rect.top += self.speed
            else:
                self.touch = 0
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < GAME_WIDTH:
                self.rect.left += self.speed
            else:
                self.touch = 0
        return self.touch

    # 射击
    def shot(self, Bullet):
        return Bullet(self)

    #
    def stay(self):
        self.rect.left = self.oldLeft
        self.rect.top = self.oldTop

    # 检测坦克是否与墙壁发生碰撞
    def hit_wall(self, MainGame):
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(self, wall):
                # 将坐标设置为移动之前的坐标
                self.stay()

    # 展示坦克的方法
    def displayTank(self, MainGame):
        # 获取展示的对象
        self.image = self.images[self.direction]
        # 调用blit方法展示
        MainGame.window.blit(self.image, self.rect)


# 我方坦克
class MyTank(Tank):
    def __init__(self, left, top):
        super(MyTank, self).__init__(left, top)
        # 坦克血量
        self.hp = 5

    # 检测我方坦克与敌方坦克发生碰撞
    def myTank_hit_enemyTank(self, MainGame):
        # 循环遍历敌方坦克列表
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(self, enemyTank):
                self.stay()


# 敌方坦克
class EnemyTank(Tank):
    def __init__(self, left, top, speed):
        # 调用父类的初始化方法
        super(EnemyTank, self).__init__(left, top)
        # 加载图片集
        self.images = {
            'U': pygame.image.load('img/enemy1U.gif'),
            'D': pygame.image.load('img/enemy1D.gif'),
            'L': pygame.image.load('img/enemy1L.gif'),
            'R': pygame.image.load('img/enemy1R.gif')
        }
        # 方向,随机生成敌方坦克的方向
        self.direction = self.randDirection()
        # 根据方向获取图片
        self.image = self.images[self.direction]
        # 区域
        self.rect = self.image.get_rect()
        # 对left和top进行赋值
        self.rect.left = left
        self.rect.top = top
        # 速度
        self.speed = speed
        # 移动开关键
        self.flag = True
        # 薪增加一个步数变量 step
        self.step = 60
        # 坦克血量
        self.hp = 100

    # 敌方坦克与我方坦克是否发生碰撞
    def enemyTank_hit_myTank(self, MainGame):
        if pygame.sprite.collide_rect(self, MainGame.my_tank):
            self.stay()

    # 随机生成敌方坦克的方向
    def randDirection(self):
        num = random.randint(1, 4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return "L"
        elif num == 4:
            return 'R'

    # 敌方坦克随机移动的方法
    def randMove(self):
        if self.step <= 0:
            # 修改方向
            self.direction = self.randDirection()
            # 让步数复位
            self.step = 60
        else:
            self.touch = self.move()
            # 让步数递减
            self.step -= 1
            # 如果接触墙壁就马上转向
            if self.touch == 0:
                self.step = -1

    # 重写shot()
    def shot(self, Bullet):
        # 随机生成100以内的数
        num = random.randint(1, 1000)
        if num < 30:
            return Bullet(self)


# 创建我方坦克的方法
def createMytank(MainGame):
    MainGame.my_tank = MyTank(350, 300)
    music.Music('img/start.wav')


# 初始化敌方坦克，并将敌方坦克添加到列表中
def createEnemyTank(MainGame):
    top = 100
    # 循环生成敌方坦克
    for i in range(MainGame.enemyTankCount):
        left = random.randint(0, 600)
        speed = random.randint(1, 4)
        enemy = EnemyTank(left, top, speed)
        MainGame.enemyTankList.append(enemy)


# 循环遍历敌方坦克列表，展示敌方坦克
def blitEnemyTank(MainGame, Bullet):
    for enemyTank in MainGame.enemyTankList:
        # 判断当前敌方坦克是否活着
        if enemyTank.live:
            enemyTank.displayTank(MainGame)
            enemyTank.randMove()
            # 调用检测是否与墙壁碰撞
            enemyTank.hit_wall(MainGame)
            # 检测敌方坦克是否与我方坦克发生碰撞
            if MainGame.my_tank and MainGame.my_tank.live:
                enemyTank.enemyTank_hit_myTank(MainGame)
            # 发射子弹
            enemyBullet = enemyTank.shot(Bullet)
            # 敌方子弹是否是None，如果不为None则添加到敌方子弹列表中
            if enemyBullet:
                # 将敌方子弹存储到敌方子弹列表中
                MainGame.enemyBulletList.append(enemyBullet)
        else:  # 不活着，从敌方坦克列表中移除
            MainGame.enemyTankList.remove(enemyTank)
