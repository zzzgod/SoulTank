from maingame import MainGame
import pygame,time
from constant import *
import music
import loading
from classic_menu import classic

BG_COLOR = pygame.Color(0, 0, 0)
class game_exit:
    window=None
    option=0
    image_menu_maoxian = pygame.image.load('img/menu_maoxian.gif')
    image_menu_jingdian = pygame.image.load('img/menu_jingdian.gif')
    image_menu_shezhi = pygame.image.load('img/menu_shezhi.gif')
    image_menu_guanyu = pygame.image.load('img/menu_guanyu.gif')
    image_menu_tuichu = pygame.image.load('img/menu_tuichu.gif')
    image_menu_exit = pygame.image.load('img/menu_exit.gif')
    image_menu_yes = pygame.image.load('img/yes.gif')
    image_menu_no = pygame.image.load('img/no.gif')
    image_menu_yes_big = pygame.image.load('img/yes_big.gif')
    image_menu_no_big = pygame.image.load('img/no_big.gif')
    def __init__(self):
        pass
    def openmenu(self):
        pygame.display.init()
        # 设置窗口的大小及显示
        game_exit.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        # 设置窗口的标题
        pygame.display.set_caption('Soul Tank')

        image_main_background = pygame.image.load('img/main_background.gif')
        while True:
            #刷新频率
            time.sleep(0.02)
            game_exit.window.fill(BG_COLOR)
            game_exit.window.blit(image_main_background, (0, 0))
            game_exit.window.blit(self.image_menu_maoxian, (900, 20))
            game_exit.window.blit(self.image_menu_jingdian, (900, 150))
            game_exit.window.blit(self.image_menu_shezhi, (900, 280))
            game_exit.window.blit(self.image_menu_guanyu, (900, 410))
            game_exit.window.blit(self.image_menu_tuichu, (800, 540))
            game_exit.window.blit(self.image_menu_exit, (0, 0))
            # 获取事件
            flag = self.getEvent()
            if flag == 0:
                return
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
                #回车选择
                if event.key == pygame.K_RETURN:
                    music.Music('img/fire2.wav')
                    if self.option==0:
                        exit()
                    if self.option==1:
                        return 0
                    #a和d左右切换
                elif event.key == pygame.K_a:
                    music.Music('img/choose.mp3')
                    self.option-=1
                    if self.option<0:
                        self.option=1
                elif event.key == pygame.K_d:
                    music.Music('img/choose.mp3')
                    self.option+=1
                    if self.option>1:
                        self.option=0
                print(self.option)
        if self.option==0:
            game_exit.window.blit(self.image_menu_yes_big, (300, 410))
            game_exit.window.blit(self.image_menu_no, (920, 425))
        else:
            game_exit.window.blit(self.image_menu_yes, (300, 420))
            game_exit.window.blit(self.image_menu_no_big, (920, 415))