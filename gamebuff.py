import pygame


# 单个buff
class Buff:
    def __init__(self, var, var_t, var_p, var_pt):
        self.var = var
        self.var_p = var_p
        self.time = var_t
        self.time_p = var_pt


# 单项状态值
class BaseStatus:
    def __init__(self, base_value):
        self.base = base_value
        self.vars = []

    def add(self, var, var_t, var_p, var_pt):
        # 获取当前时间
        time = pygame.time.get_ticks()
        var_t += time
        var_pt += time
        buff = Buff(var, var_t, var_p)


# 集中了坦克状态的基础值及所有的buff
class Status:
    def __init__(self):
        # 初始化各类buff，_p是百分比变化，_t是对应的持续时长
        # 速度buff
        self.speed = 0
        self.speed_t = 0
        self.speed_p = 0
        self.speed_pt = 0
        # 增伤buff
        self.damage = 0
        self.damage_t = 0
        self.damage_p = 0
        self.damage_pt = 0
        # 破甲buff
        self.penetration = 0
        self.penetration_t = 0
        self.penetration_p = 0
        self.penetration_pt = 0
        # 免疫次数
        self.immune_c = 0
        # 免疫时长
        self.immune_t = 0
