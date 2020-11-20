from gamebullet import Bullet
import json


class BaseGun:
    def __init__(self, gun_type, bullet: Bullet):
        path = "entity/equipments/artillery/" + gun_type + ".json"
        # 读取炮的信息
        f = open(path, 'r')
        self.gun_info = json.load(f)
        self.damage = self.gun_info['Damage']
        self.penetration = self.gun_info['Penetration']
        self.speed = self.gun_info['Speed']
        # 给炮弹加强属性
        self.bullet = bullet
        self.bullet.speed += self.speed
        self.bullet.damage += self.damage
        self.bullet.penetration += self.penetration

    def shot(self) -> Bullet:
        return self.bullet
