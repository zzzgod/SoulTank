import json
import pygame, time
import gamewall
import gametank
from gamebullet import Bullet
import Text
from constant import *
import dialogue_getevent
import gamebullet
from maingame import MainGame

BG_COLOR = pygame.Color(0, 0, 0)


class dialogue:
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
        dialogue.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        # 读入地图信息
        with open(map_path, 'r', encoding='utf-8') as f:
            dialogue.map_info = json.load(f)
            # 初始化墙壁
            gamewall.createWall(dialogue, dialogue.map_info['MapBlocks'])
        # 设置窗口的标题
        pygame.display.set_caption('Soul Tank')
        image_enemy_tank_hp = pygame.image.load('img/my_tank_hp_black.gif')
        image_enemy_tank_num = pygame.image.load('img/enemy_tank_num_black.gif')
        image_imformation = pygame.image.load('img/imformation.gif')
        image_dialogue = pygame.image.load('img/tips.gif')
        image_shadow = pygame.image.load('img/shadow.png')
        pygame.mixer.music.stop()
        with open(map_path, 'r', encoding='utf-8') as f:
            text = json.load(f)['Dialog']
        flag = 0
        while True:
            # 使用坦克移动的速度慢一点
            time.sleep(0.02)
            # 给窗口设置填充色
            dialogue.window.fill(BG_COLOR)
            # 获取事件
            flag = dialogue_getevent.getEvent(dialogue, flag)
            if flag == -1:
                return
            # 信息板
            dialogue.window.blit(image_imformation, (1140, 0))
            # 绘制图标
            dialogue.window.blit(image_enemy_tank_num, (1170, 25))
            dialogue.window.blit(image_enemy_tank_hp, (1170, 100))
            # 循环遍历墙壁列表，展示墙壁
            gamewall.blitWall(dialogue)
            # 循环遍历草列表，展示草
            gamewall.blitGrass(dialogue)
            dialogue.window.blit(image_shadow, (0, 0))
            # 绘制对话框
            dialogue.window.blit(image_dialogue, (0, 0))
            if flag == len(text):
                return
            for i, line in enumerate(text[flag]):
                dialogue.window.blit(Text.getTextSufaceBlacksmall(line), (200, 500 + 60 * i))
            pygame.display.update()
