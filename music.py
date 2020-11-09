import pygame
def Music(load_music):
    # 初始化音乐混合器
    pygame.mixer.init()
    # 加载音乐
    pygame.mixer.music.load(load_music)
    # 播放音乐
    pygame.mixer.music.play()