import pygame
class Wall():
    def __init__(self,left,top):
        #加载墙壁图片
        self.image=pygame.image.load('img/walls.gif')
        #获取墙壁的区域
        self.rect=self.image.get_rect()
        #设置位置left、top
        self.rect.left=left
        self.rect.top=top
        #是否存活
        self.live=True
        #设置生命值
        self.hp=3
def displayWall(Wall,MainGame):
    MainGame.window.blit(Wall.image,Wall.rect)
    # 循环遍历墙壁列表，展示墙壁
def blitWall(MainGame):
    for wall in MainGame.wallList:
        #判断墙壁是否存活
        if wall.live:
            #调用墙壁的显示方法
              displayWall(wall,MainGame)
        else:
                #从墙壁列表移出
              MainGame.wallList.remove(wall)
#初始化墙壁
def createWall(MainGame):
    with open('map.txt','r') as f:
        commands = f.readlines()
        for i in commands:
            eval(i.strip())
    for i in range(19):
        #初始化墙壁
        wall1=Wall(i*60,220)
        wall2=Wall(i*60,420)
        #将墙壁添加到列表中
        MainGame.wallList.append(wall1)
        MainGame.wallList.append(wall2)