import pygame
import maingame


# 一闪而过的文字
class FlashMessage(pygame.sprite.Sprite):
    def __init__(self, center_x: int, center_y: int, last_time_ms: int, s: str, *args, color: pygame.color.Color = None,
                 font_name: pygame.font.Font = None, font_size: int = None):
        if font_name is None:
            font_name = 'simhei'
        if font_size is None:
            font_size = 32
        if color is None:
            color = pygame.Color(255, 255, 255)
        # 初始化设定
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        # 设置字体及颜色
        self.font_name = font_name
        self.font_size = font_size
        self.font_color = color
        # 设置显示文字内容
        self.s = s
        self.args = args
        # 设置显示中心
        self.x = center_x
        self.y = center_y
        # 记录播放了多长时间
        # 当前时间
        self.start_time = pygame.time.get_ticks()
        self.time = last_time_ms
        # 帧速率
        self.framerate = 60

    def update(self, time_now, *args):
        # 目前显示到第几秒
        n = time_now - self.start_time
        if n > self.time:
            self.kill()
            return
        # 计算该帧文字的位置，大小，字体（居中显示）
        size = self.font_size * n // self.time
        font = pygame.font.SysFont(self.font_name, size,bold=True)
        self.image = get_message_surface(self.s, *self.args, color=self.font_color, font=font)
        self.rect = self.image.get_rect()
        x = self.x - self.rect.width // 2
        y = self.y - self.rect.height // 2
        self.rect.left = x
        self.rect.top = y


def get_message_surface(s: str, *args, color, font) -> pygame.Surface:
    pygame.font.init()
    if font is None:
        font = pygame.font.SysFont('kaiti', 12)
    if color is None:
        color = pygame.Color(255, 255, 255)
    surface = font.render(s % args, True, color)
    return surface


def printf(x: int, y: int, s: str, *args, color=None, font=None) -> None:
    surface = get_message_surface(s, *args, color=color, font=font)
    maingame.MainGame.window.blit(surface, (x, y))
    pygame.display.update()
