from maingame import MainGame
import pygame,time
from constant import *
import music
import loading

'''
单人模式
    剧情模式
        关卡一
        二...
    小游戏
        我的坦克不能开炮
        夺旗
    生存模式
        谁笑到最后？
双人模式
    
仓库
    养成？
图鉴
    
退出
'''
BG_COLOR = pygame.Color(0, 0, 0)
class menu:
    window=None
    option=0
    def __init__(self):
        pass
    def openmenu(self):
        pygame.display.init()
        # 设置窗口的大小及显示
        menu.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        # 设置窗口的标题
        pygame.display.set_caption('Soul Tank')
        while True:
            #刷新频率
            time.sleep(0.02)
            menu.window.fill(BG_COLOR)
            # 获取事件
            self.getEvent()
            image_main_background = pygame.image.load('img/main_background.gif')
            menu.window.blit(image_main_background, (0, 0))
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
                    if self.option==0:
                        loading.load()
                        MainGame().startGame()
                elif event.key == pygame.K_s:
                    music.Music('img/choose.mp3')
                    self.option+=1
                    if self.option>5:
                        self.option=0
                elif event.key == pygame.K_w:
                    music.Music('img/choose.mp3')
                    self.option-=1
                    if self.option<0:
                        self.option=5
                print(self.option)

if __name__ == '__main__':
    # zzz yyds
    menu().openmenu()