#导入pygame模块
import pygame
from maingame import MainGame
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
SCREEN_WIDTH=1280
SCREEN_HEIGHT=720
BG_COLOR=pygame.Color(0,0,0)

if __name__=='__main__':
    # z yyds
    MainGame().startGame()
    # MainGame().getTextSuface()
