from maingame import MainGame
import pygame, time
from constant import *
import music
import loading
from gamedialogue import dialogue

BG_COLOR = pygame.Color(0, 0, 0)


class singleplay:
    window = None
    option = 0
    image_menu = pygame.image.load('img/singleplay.gif')
    image_select=pygame.image.load('img/select.gif')

    def __init__(self):
        pass

    def openmenu(self):
        pygame.display.init()
        # 设置窗口的大小及显示
        singleplay.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        # 设置窗口的标题
        pygame.display.set_caption('Soul Tank')
        while True:
            # 刷新频率
            time.sleep(0.02)
            singleplay.window.fill(BG_COLOR)
            singleplay.window.blit(self.image_menu, (0, 0))
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
                # esc键切换全屏和窗口
                if event.key == pygame.K_RETURN:
                    music.Music('img/fire2.wav')
                    if self.option == 0:
                        return 0
                    else:
                        loading.load()
                        dialogue().startGame(self.option)
                        MainGame().startGame(self.option)
                elif event.key == pygame.K_s:
                    music.Music('img/choose.mp3')
                    self.option += 5
                    if self.option > 24:
                        self.option = self.option -24-1
                elif event.key == pygame.K_w:
                    music.Music('img/choose.mp3')
                    self.option -= 5
                    if self.option < 0:
                        self.option = 24+self.option+1
                elif event.key == pygame.K_a:
                    music.Music('img/choose.mp3')
                    self.option -= 1
                    if self.option < 0:
                        self.option = 24
                elif event.key == pygame.K_d:
                    music.Music('img/choose.mp3')
                    self.option += 1
                    if self.option >24:
                        self.option = 0
                print(self.option)
        o=self.option//5
        p=self.option%5
        singleplay.window.blit(self.image_select, (180+p*180 , 110+o*100))