import pygame

TEXT_COLOR_RED = pygame.Color(255, 0, 0)
TEXT_COLOR_GREEN = pygame.Color(50, 205, 50)
TEXT_COLOR_YELLOW = pygame.Color(255, 255, 0)
TEXT_COLOR_BLACK = pygame.Color(0, 0, 0)


def getTextSufaceGreen(text):
    # 初始化字体模块
    pygame.font.init()
    # 查看所有的字体名称
    # print(pygame.font.get_fonts())
    # 获取字体Font对象
    font = pygame.font.SysFont('heiti', 36)
    # 绘制文字信息
    textSurface = font.render(text, True, TEXT_COLOR_GREEN)
    return textSurface


def getTextSufaceYellow(text):
    # 初始化字体模块
    pygame.font.init()
    # 查看所有的字体名称
    # print(pygame.font.get_fonts())
    # 获取字体Font对象
    font = pygame.font.SysFont('heiti', 36)
    # 绘制文字信息
    textSurface = font.render(text, True, TEXT_COLOR_YELLOW)
    return textSurface


def getTextSufaceRed(text):
    # 初始化字体模块
    pygame.font.init()
    # 查看所有的字体名称
    # print(pygame.font.get_fonts())
    # 获取字体Font对象
    font = pygame.font.SysFont('heiti', 36)
    # 绘制文字信息
    textSurface = font.render(text, True, TEXT_COLOR_RED)
    return textSurface

def getTextSufaceBlack(text):
    # 初始化字体模块
    pygame.font.init()
    # 查看所有的字体名称
    # print(pygame.font.get_fonts())
    # 获取字体Font对象
    font = pygame.font.SysFont('heiti', 72)
    # 绘制文字信息
    textSurface = font.render(text, True, TEXT_COLOR_BLACK)
    return textSurface
