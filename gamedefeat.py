import json
import pygame, time
import gamewall
from constant import *
import music

BG_COLOR = pygame.Color(0, 0, 0)


class defeat:
    window = None
    # 存储墙壁的列表
    wallList = []
    waterList = []
    grassList = []
    map_info = None

    def __init__(self):
        pass

    # 开始游戏
    def startGame(self, n):
        map_index = n
        # 获取地图路经
        map_path = 'maps/map' + str(map_index) + '.json'
        # 加载主窗口
        # 初始化窗口
        pygame.display.init()
        # 设置窗口的大小及显示
        defeat.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        # 读入地图信息
        with open(map_path, 'r', encoding='utf-8') as f:
            defeat.map_info = json.load(f)
            # 初始化墙壁
            gamewall.createWall(defeat, defeat.map_info['MapBlocks'])
        # 设置窗口的标题
        pygame.display.set_caption('Soul Tank')
        image_imformation = pygame.image.load('img/imformation.gif')
        image_defeat = pygame.image.load('img/defeat.gif')
        image_shadow = pygame.image.load('img/shadow.png')
        pygame.mixer.music.stop()
        music.Music('img/defeat.mp3')
        while True:
            # 使用坦克移动的速度慢一点
            time.sleep(0.02)
            # 给窗口设置填充色
            defeat.window.fill(BG_COLOR)
            # 信息板
            defeat.window.blit(image_imformation, (1140, 0))
            # 绘制图标
            image_enemy_tank_num = pygame.image.load('img/enemy_tank_num_black.gif')
            defeat.window.blit(image_enemy_tank_num, (1170, 25))
            image_enemy_tank_num = pygame.image.load('img/my_tank_hp_black.gif')
            defeat.window.blit(image_enemy_tank_num, (1170, 100))
            image_enemy_tank_num = pygame.image.load('img/AP_num.gif')
            defeat.window.blit(image_enemy_tank_num, (1170, 175))
            image_enemy_tank_num = pygame.image.load('img/APCR_num.gif')
            defeat.window.blit(image_enemy_tank_num, (1170, 250))
            image_enemy_tank_num = pygame.image.load('img/HE_num.gif')
            defeat.window.blit(image_enemy_tank_num, (1170, 325))
            image_enemy_tank_num = pygame.image.load('img/HEAT_num.gif')
            defeat.window.blit(image_enemy_tank_num, (1170, 400))
            # 循环遍历墙壁列表，展示墙壁
            gamewall.blitWall(defeat)
            # 循环遍历草列表，展示草
            gamewall.blitGrass(defeat)
            defeat.window.blit(image_shadow, (0, 0))
            defeat.window.blit(image_defeat, (0, 0))
            eventList = pygame.event.get()
            # 遍历事件
            for event in eventList:
                # 判断按下的键是关闭还是键盘按下
                # 如果按的是退出，关闭窗口
                if event.type == pygame.QUIT:
                    exit()
                # 如果是键盘的按下
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return True
            pygame.display.update()