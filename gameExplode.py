import pygame
from constant import *


class Explode():
    def __init__(self, tank):
        # 爆炸的位置由当前子弹打中的坦克位置决定
        self.rect = tank.rect
        self.images = [
            pygame.image.load('img/blast0.gif'),
            pygame.image.load('img/blast1.gif'),
            pygame.image.load('img/blast2.gif'),
            pygame.image.load('img/blast3.gif'),
            pygame.image.load('img/blast4.gif'),
            pygame.image.load('img/blast5.gif'),
            pygame.image.load('img/blast6.gif'),
            pygame.image.load('img/blast7.gif'),
        ]
        self.step = 0
        self.divstep = 0
        self.image = self.images[self.step]
        # 是否活着
        self.live = True

    # 展示小爆炸效果的方法
    def displaysmallExplode(self, MainGame):
        if self.step < 3:
            # 根据索引获取爆炸对象
            self.image = self.images[self.step]
            self.divstep += 1
            if self.divstep % 3 == 0:
                self.step += 1
            # 添加到主窗口
            MainGame.window.blit(self.image, (self.rect[0] - 30, self.rect[1] - 30))
        else:
            # 修改活着的状态
            self.live = False
            self.step = 0
            self.divstep = 0

    # 展示爆炸效果的方法
    def displayExplode(self, MainGame):
        if self.step < 5:
            # 根据索引获取爆炸对象
            self.image = self.images[self.step]
            self.divstep += 1
            if self.divstep % 3 == 0:
                self.step += 1
            # 添加到主窗口
            MainGame.window.blit(self.image, (self.rect[0] - 30, self.rect[1] - 30))
        else:
            # 修改活着的状态
            self.live = False
            self.step = 0
            self.divstep = 0

    # 展示大爆炸效果的方法
    def displaybigExplode(self, MainGame):
        if self.step < 8:
            # 根据索引获取爆炸对象
            self.image = self.images[self.step]
            self.divstep += 1
            if self.divstep % 5 == 0:
                self.step += 1
            # 添加到主窗口
            MainGame.window.blit(self.image, (self.rect[0] - 30, self.rect[1] - 30))
        else:
            # 修改活着的状态
            self.live = False
            self.step = 0
            self.divstep = 0


# 循环展示小爆炸效果
def blitsmallExplode(MainGame):
    for explode in MainGame.explodesmallList:
        # 判断是否活着
        if explode.live:
            # 展示
            explode.displaysmallExplode(MainGame)
        else:
            # 在爆炸列表中移除
            MainGame.explodesmallList.remove(explode)


# 循环展示爆炸效果
def blitExplode(MainGame):
    for explode in MainGame.explodeList:
        # 判断是否活着
        if explode.live:
            # 展示
            explode.displayExplode(MainGame)
        else:
            # 在爆炸列表中移除
            MainGame.explodeList.remove(explode)
    # 循环展示大爆炸效果


def blitbigExplode(MainGame):
    for explode in MainGame.explodebigList:
        # 判断是否活着
        if explode.live:
            # 展示
            explode.displaybigExplode(MainGame)
        else:
            # 在爆炸列表中移除
            MainGame.explodebigList.remove(explode)
