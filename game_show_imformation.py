import pygame

def show(MainGame):
    image_imformation = pygame.image.load('img/imformation.gif')
    MainGame.window.blit(image_imformation, (1140, 0))
    # 绘制图标
    image_enemy_tank_num = pygame.image.load('img/enemy_tank_num_black.gif')
    MainGame.window.blit(image_enemy_tank_num, (1170, 25))
    image_enemy_tank_num = pygame.image.load('img/my_tank_hp_black.gif')
    MainGame.window.blit(image_enemy_tank_num, (1170, 100))
    image_enemy_tank_num = pygame.image.load('img/AP_num.gif')
    MainGame.window.blit(image_enemy_tank_num, (1170, 175))
    image_enemy_tank_num = pygame.image.load('img/HE_num.gif')
    MainGame.window.blit(image_enemy_tank_num, (1170, 250))
    image_enemy_tank_num = pygame.image.load('img/APCR_num.gif')
    MainGame.window.blit(image_enemy_tank_num, (1170, 325))