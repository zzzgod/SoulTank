from maingame import MainGame
import pygame,time
from constant import *
import music
import loading
from classic_menu import classic
from exit import game_exit
'''
冒险模式
    地图
经典模式
    训练模式
    单人模式
    双人模式
设置
关于 
退出
'''
BG_COLOR = pygame.Color(0, 0, 0)
class menu:
    window=None
    option=0
    image_menu_maoxian = pygame.image.load('img/menu_maoxian.gif')
    image_menu_jingdian = pygame.image.load('img/menu_jingdian.gif')
    image_menu_shezhi = pygame.image.load('img/menu_shezhi.gif')
    image_menu_guanyu = pygame.image.load('img/menu_guanyu.gif')
    image_menu_tuichu = pygame.image.load('img/menu_tuichu.gif')
    image_menu_exit = pygame.image.load('img/menu_exit.gif')
    def __init__(self):
        pass
    def openmenu(self):
        pygame.display.init()
        # 设置窗口的大小及显示
        menu.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        # 设置窗口的标题
        pygame.display.set_caption('Soul Tank')

        image_main_background = pygame.image.load('img/main_background.gif')
        while True:
            #刷新频率
            time.sleep(0.02)
            menu.window.fill(BG_COLOR)
            menu.window.blit(image_main_background, (0, 0))
            # 获取事件
            self.getEvent()
            pygame.display.update()
    def getEvent(self):
        # 获取所有事件
        eventList = pygame.event.get()
        # 遍历事件
        for event in eventList:
            # 判断按下的键是关闭还是键盘按下
            # 如果按的是退出，关闭窗口
            if event.type == pygame.QUIT:
                exit()
            # 如果是键盘的按下
            if event.type == pygame.KEYDOWN:
                # 回车选择
                if event.key == pygame.K_RETURN:
                    music.Music('img/fire2.wav')
                    if self.option==1:
                        classic().openmenu()
                    if self.option==4:
                        game_exit().openmenu()
                        #w s 上下选择
                elif event.key == pygame.K_s:
                    music.Music('img/choose.mp3')
                    self.option+=1
                    if self.option>4:
                        self.option=0
                elif event.key == pygame.K_w:
                    music.Music('img/choose.mp3')
                    self.option-=1
                    if self.option<0:
                        self.option=4
                print(self.option)
        o1,o2,o3,o4,o5=0,0,0,0,0
        if self.option==0:
            o1=100
        elif self.option==1:
            o2=100
        elif self.option==2:
            o3=100
        elif self.option==3:
            o4=100
        elif self.option==4:
            o5=100
        menu.window.blit(self.image_menu_maoxian, (900-o1, 20))
        menu.window.blit(self.image_menu_jingdian, (900-o2, 150))
        menu.window.blit(self.image_menu_shezhi, (900-o3, 280))
        menu.window.blit(self.image_menu_guanyu, (900-o4, 410))
        menu.window.blit(self.image_menu_tuichu, (900-o5, 540))

if __name__ == '__main__':
    # zzz yyds
    menu().openmenu()