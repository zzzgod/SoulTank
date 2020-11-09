import pygame
def Stone_Wall(left,top):
        #加载墙壁图片
        image=pygame.image.load('img/walls.gif')
        #获取墙壁的区域
        rect=image.get_rect()
        #设置位置left、top
        rect.left=left
        rect.top=top
        #是否存活
        live=True
        #设置生命值
        hp=3
    #展示墙壁的方法
def displayWall(self):
    window.blit(image,rect)