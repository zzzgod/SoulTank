import pygame
import gamemusic
import random


# 掉落物类
class Drop:
    def __init__(self, tank, drop_type):
        self.image = None
        self.drop_type = drop_type
        self.music = None
        if drop_type == 'AddBullet':
            self.image = pygame.image.load('img/drop/AddBullet.gif')
            self.music = gamemusic.Music('img/get_item.wav')
        elif drop_type == 'Clock':
            self.image = pygame.image.load('img/drop/Clock.png')
            self.music = gamemusic.Music('img/get_item.wav')
        elif drop_type == 'Gasoline':
            self.image = pygame.image.load('img/drop/Gasoline.png')
            self.music = gamemusic.Music('img/get_item.wav')
        elif drop_type == 'Kit':
            self.image = pygame.image.load('img/drop/Kit.png')
            self.music = gamemusic.Music('img/get_item.wav')
        elif drop_type == 'Net':
            self.image = pygame.image.load('img/drop/Net.png')
            self.music = gamemusic.Music('img/get_item.wav')
        elif drop_type == 'PurpleBullet':
            self.image = pygame.image.load('img/drop/PurpleBullet.png')
            self.music = gamemusic.Music('img/get_item.wav')
        elif drop_type == 'Rage':
            self.image = pygame.image.load('img/drop/Rage.png')
            self.music = gamemusic.Music('img/get_item.wav')
        elif drop_type == 'RedBullet':
            self.image = pygame.image.load('img/drop/RedBullet.png')
            self.music = gamemusic.Music('img/get_item.wav')
        elif drop_type == 'Shield':
            self.image = pygame.image.load('img/drop/Shield.png')
            self.music = gamemusic.Music('img/get_item.wav')
        elif drop_type == 'Snow':
            self.image = pygame.image.load('img/drop/Snow.png')
            self.music = gamemusic.Music('img/get_item.wav')
        elif drop_type == 'Star':
            self.image = pygame.image.load('img/drop/Star.png')
            self.music = gamemusic.Music('img/get_item.wav')
        else:
            raise ValueError('掉落物格式不匹配。')
        # 移动掉落物至坦克
        self.rect = self.image.get_rect().move(tank.rect.left, tank.rect.top)
        # 掉落物的状态，是否被拾取，如果被拾取，修改此状态
        self.live = True


# 掉落物与坦克的碰撞
def drop_hit_tank(drop, MainGame, tank_type):
    if tank_type == 'EnemyTank':
        pass
    elif tank_type == 'PlayerTank':
        if MainGame.my_tank and MainGame.my_tank.live:
            if pygame.sprite.collide_rect(MainGame.my_tank, drop):
                ran = random.randint(1, 100)
                # 修改掉落物与我方坦克的状态
                drop.live = False
                if drop.drop_type == 'AddBullet':
                    if ran < 50:
                        MainGame.AP_num += 5
                    elif ran<60:
                        MainGame.APCR_num+=5
                    else:
                        MainGame.HE_num+=5
                elif drop.drop_type == 'Kit':
                    pass
                elif drop.drop_type == 'Net':
                    pass
                elif drop.drop_type == 'PurpleBullet':
                    pass
                elif drop.drop_type == 'Rage':
                    pass
                elif drop.drop_type == 'RedBullet':
                    pass
                elif drop.drop_type == 'Shield':
                    pass
                elif drop.drop_type == 'Snow':
                    pass
                elif drop.drop_type == 'Star':
                    pass
                else:
                    raise ValueError('掉落物格式不匹配。')


# 展示掉落物的方法
def display_drop(drop, main_game):
    # 将图片surface加载到窗口
    main_game.window.blit(drop.image, drop.rect)


# 循环遍历敌方子弹列表，展示敌方子弹
def blit_drop(MainGame):
    for drop in MainGame.dropList:
        if drop.live:  # 判断掉落物是否存活
            display_drop(drop, MainGame)


# 循环遍历掉落物列表
def check_drop(MainGame):
    for drop in MainGame.dropList:
        if drop.live:  # 判断敌方子弹是否存活
            # 调用敌方子弹与我方坦克碰撞的方法
            drop_hit_tank(drop, MainGame, 'PlayerTank')
        else:
            drop.music.play()
            MainGame.dropList.remove(drop)
