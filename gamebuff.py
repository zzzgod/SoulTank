import pygame
import gamebullet
import gametank


# 单个buff
class Buff:
    # 构造一个buff，其中buff_type是buff的类型，0是数值型，1是百分比型
    def __init__(self, buff_type, var, var_t):
        self.type = buff_type
        self.var = var
        self.time = var_t

    # 检查当前buff是否过期，True为不过期，False过期
    def check(self, time):
        # 如果time为-1则认为是永久buff
        if self.time == -1:
            return True
        return self.time >= time

    # 获取当前buff的增益，需要传入基础值
    def get(self, base):
        if self.type == 0:
            return self.var
        else:
            return self.var * base


# 单项状态值
class BaseStatus:
    def __init__(self, value=None):
        # 可以立刻设定基础值，或者之后使用set方法进行设置
        self.base = value
        self.vars = []

    # 设置基础值
    def set(self, value):
        self.base = value

    # 添加一个buff
    def add(self, buff_type, value, duration):
        # 获取当前时间
        time = pygame.time.get_ticks()
        duration += time
        # 存储状态值
        buff = Buff(buff_type, value, duration)
        self.vars.append(buff)

    # 清理过期的buff
    def clear(self, time):
        i = 0
        while i < len(self.vars):
            # 如果已过期
            if not self.vars[i].check(time):
                self.vars.pop(i)
            else:
                i += 1

    # 获取当前的状态值
    def get(self):
        if self.base is None:
            raise AttributeError('必须提供属性的基准值')
        # 获取当前时间
        time = pygame.time.get_ticks()
        # 清除过期buff
        self.clear(time)
        # 状态初始化为基础属性
        status = self.base
        # 叠加各种buff
        for buff in self.vars:
            status += buff.get(status)
        return status


# 集中了坦克状态的基础值及所有的buff
class Status:
    def __init__(self, health, fire_rate, armor, speed):
        # 初始化各类数值
        # 坦克
        # 最大生命值
        self._max_health = BaseStatus(health)
        # 生命值
        self._health = BaseStatus(health)
        # 射速
        self._fire_rate = BaseStatus(fire_rate)
        # 护甲
        self._armor = BaseStatus(armor)
        # 速度
        self._tank_speed = BaseStatus(speed)

        # 炮弹
        # 速度
        self._bullet_speed = BaseStatus()
        # 伤害
        self._damage = BaseStatus()
        # 破甲
        self._penetration = BaseStatus()
        # 伤害减益系数
        self._damage_reduction_rate = BaseStatus()
        # 免疫次数
        self._immune_c = 0
        # 免疫时长
        self._immune_t = 0

    # health, fire_rate, tank_speed, armor, bullet_speed, damage, penetration, damage_reduction_rate

    # 属性的getter, setter
    @property
    def max_health(self):
        return self._max_health.get()

    @property
    def health(self):
        return self._health.get()

    @property
    def fire_rate(self):
        return self._fire_rate.get()

    @property
    def armor(self):
        return self._armor.get()

    @property
    def tank_speed(self):
        return self._tank_speed.get()

    @property
    def bullet_speed(self):
        return self._bullet_speed.get()

    @property
    def damage(self):
        return self._damage.get()

    @property
    def penetration(self):
        return self._penetration.get()

    @property
    def damage_reduction_rate(self):
        return self._damage_reduction_rate.get()

    @property
    def immune_c(self):
        return self._immune_c

    @property
    def immune_t(self):
        return self._immune_t

    @max_health.setter
    def max_health(self, value):
        self._max_health.set(value)

    @health.setter
    def health(self, value):
        self._health.set(value)

    @fire_rate.setter
    def fire_rate(self, value):
        self._fire_rate.set(value)

    @bullet_speed.setter
    def bullet_speed(self, value):
        self._bullet_speed.set(value)

    @damage.setter
    def damage(self, value):
        self._damage.set(value)

    @penetration.setter
    def penetration(self, value):
        self._penetration.set(value)

    @damage_reduction_rate.setter
    def damage_reduction_rate(self, value):
        self._damage_reduction_rate.set(value)

    @immune_c.setter
    def immune_c(self, value):
        self._immune_c = value

    @immune_t.setter
    def immune_t(self, value):
        self._immune_t = pygame.time.get_ticks() + value

    # 添加一个buff
    def add(self, buff_name, buff_type, value, duration=-1):
        # 根据不同类别的buff来添加效果
        if buff_name == 'Immune':
            if buff_type == 0:
                # 加免疫次数
                self._immune_c += value
            else:
                # 加免疫时长
                self._immune_t = pygame.time.get_ticks() + duration
        elif buff_name == "Health":
            self._health.add(buff_type, value, duration)
        elif buff_name == "FireRate":
            self._fire_rate.add(buff_type, value, duration)
        elif buff_name == "Armor":
            self._armor.add(buff_type, value, duration)
        elif buff_name == "TankSpeed":
            self._tank_speed.add(buff_type, value, duration)
        elif buff_name == "BulletSpeed":
            self._bullet_speed.add(buff_type, value, duration)
        elif buff_name == "Damage":
            self._damage.add(buff_type, value, duration)
        elif buff_name == "Penetration":
            self._penetration.add(buff_type, value, duration)
        elif buff_name == "DamageReductionRate":
            self._damage_reduction_rate.add(buff_type, value, duration)

    # 坦克不用额外设置函数获取buff后的属性值
    # 给子弹加buff
    def buff_bullet(self, bullet: gamebullet.Bullet):
        # 先拿到基础值
        self.bullet_speed = bullet.speed
        self.damage = bullet.damage
        self.penetration = bullet.penetration
        self.damage_reduction_rate = bullet.damage_reduction_rate
        # 再赋增益后的值
        bullet.speed = self.bullet_speed
        bullet.damage = self.damage
        bullet.penetration = self.penetration
        bullet.damage_reduction_rate = self.damage_reduction_rate
