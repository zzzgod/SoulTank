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


# def ashing_img(img, ratio) -> None:
#     width, height = img.get_size()
#     ratio = 1 - ratio
#     for i in range(width):
#         for j in range(height):
#             color = img.get_at((i, j))
#             color.r = int(color.r * ratio)
#             color.g = int(color.g * ratio)
#             color.b = int(color.b * ratio)
#             img.set_at((i, j), color)


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
            talk = json.load(f)['Dialogue']
        flag = 0
        left_img = pygame.image.load(talk[flag]['Characters']['Left']['img']).convert_alpha()
        right_img = pygame.image.load(talk[flag]['Characters']['Right']['img']).convert_alpha()
        while True:
            # 使用坦克移动的速度慢一点
            time.sleep(0.02)
            # 给窗口设置填充色
            dialogue.window.fill(BG_COLOR)
            # 获取事件
            rtv = dialogue_getevent.getEvent(dialogue)
            # 如果挑过了剧情
            if rtv == -1:
                return
            elif rtv == 1:
                flag += 1
                if flag == len(talk):
                    return
                left_img = pygame.image.load(talk[flag]['Characters']['Left']['img']).convert_alpha()
                right_img = pygame.image.load(talk[flag]['Characters']['Right']['img']).convert_alpha()
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
            # 显示人物图片
            dialogue.window.blit(left_img, (-200, 0))
            dialogue.window.blit(right_img, (780, 0))
            # 绘制对话框
            dialogue.window.blit(image_dialogue, (0, 0))
            for i, line in enumerate(talk[flag]['Content']):
                dialogue.window.blit(Text.getTextSufaceBlacksmall(line), (200, 500 + 60 * i))
            pygame.display.update()
