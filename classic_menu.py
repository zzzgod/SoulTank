from maingame import MainGame
import pygame, time
from constant import *
import music
import loading

BG_COLOR = pygame.Color(0, 0, 0)


class classic:
    window = None
    option = 0
    image_menu_xunlian = pygame.image.load('img/menu_xunlian.gif')
    image_menu_danren = pygame.image.load('img/menu_danren.gif')
    image_menu_shuangren = pygame.image.load('img/menu_shuangren.gif')
    image_menu_fanhui = pygame.image.load('img/menu_fanhui.gif')

    def __init__(self):
        pass

    def openmenu(self):
        pygame.display.init()
        # 设置窗口的大小及显示
        classic.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        # 设置窗口的标题
        pygame.display.set_caption('Soul Tank')

        image_main_background = pygame.image.load('img/main_background.gif')
        while True:
            # 刷新频率
            time.sleep(0.02)
            classic.window.fill(BG_COLOR)
            classic.window.blit(image_main_background, (0, 0))
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
                        loading.load()
                        MainGame().startGame()
                    if self.option == 3:
                        return 0
                elif event.key == pygame.K_s:
                    music.Music('img/choose.mp3')
                    self.option += 1
                    if self.option > 3:
                        self.option = 0
                elif event.key == pygame.K_w:
                    music.Music('img/choose.mp3')
                    self.option -= 1
                    if self.option < 0:
                        self.option = 3
                print(self.option)
        o1, o2, o3, o4 = 0, 0, 0, 0
        if self.option == 0:
            o1 = 100
        elif self.option == 1:
            o2 = 100
        elif self.option == 2:
            o3 = 100
        elif self.option == 3:
            o4 = 100
        classic.window.blit(self.image_menu_xunlian, (900 - o1, 20))
        classic.window.blit(self.image_menu_danren, (900 - o2, 150))
        classic.window.blit(self.image_menu_shuangren, (900 - o3, 280))
        classic.window.blit(self.image_menu_fanhui, (900 - o4, 410))
