import pygame


class Music:
    def __init__(self, path):
        # 初始化音乐混合器
        pygame.mixer.init()
        # 记录地址
        self.path = path

    def play(self):
        # 加载音乐
        pygame.mixer.music.load(self.path)
        # 播放音乐
        pygame.mixer.music.play()
