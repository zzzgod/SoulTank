import pygame
import gametank
import gamebullet
import gamedrop
import gameExplode
import gametext
import gamearchitecture
import random
import music


# 子弹是否碰撞墙壁
def hit_wall(bullet, MainGame):
    # 如果可以穿墙，直接返回
    if bullet.cross_wall:
        return
    # 循环遍历墙壁列表
    for wall in MainGame.wallList:
        if pygame.sprite.collide_rect(bullet, wall):
            # 修改子弹的生存状态，让子弹消失
            bullet.live = False
            # 墙壁的生命值减小
            wall.hp -= bullet.damage
            if wall.hp <= 0:
                # 修改墙壁的生存状态
                wall.live = False
                # 产生爆炸对象
                explode = gameExplode.Explode(wall)
                # 将爆炸对象添加到爆炸列表中
                MainGame.explodesmallList.append(explode)


# 子弹与坦克的碰撞
def bullet_hit_tank(bullet, MainGame, tank_type):
    if tank_type == 'EnemyTank':
        # 循环遍历敌方坦克列表，判断是否发生碰撞
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(enemyTank, bullet):
                # 修改敌方坦克和我方子弹的状态
                damage = calculate_bullet_damage_tank(enemyTank, bullet)
                enemyTank.status.health -= damage
                if enemyTank.status.health <= 0:
                    enemyTank.live = False
                    music.Music('img/enemy1_explode.wav')
                bullet.live = False
                # 创建爆炸对象
                explode = gameExplode.Explode(enemyTank)
                # 将爆炸对象添加到爆炸列表中
                MainGame.explodeList.append(explode)
                # 添加伤害数字特效
                sprite = gametext.FlashMessage(bullet.rect.left, bullet.rect.top, 300, str(damage), font_size=54,
                                               color=pygame.color.Color(255, 109, 29))
                MainGame.sprite_group.add(sprite)
                break
    elif tank_type == 'PlayerTank':
        if MainGame.my_tank and MainGame.my_tank.live:
            if pygame.sprite.collide_rect(MainGame.my_tank, bullet):
                # 修改敌方子弹与我方坦克的状态
                bullet.live = False
                # 如果坦克正处于隐身状态，则不受伤害
                time_now = pygame.time.get_ticks()
                if MainGame.my_tank.status.immune_t >= time_now:
                    return
                # 若处于护盾下，免疫本次伤害
                elif MainGame.my_tank.status.immune_c > 0:
                    MainGame.my_tank.status.immune_c -= 1
                    return
                damage = calculate_bullet_damage_tank(MainGame.my_tank, bullet)
                MainGame.my_tank.status.health -= damage
                if MainGame.my_tank.status.health <= 0:
                    MainGame.my_tank.live = False
                    # 产生爆炸对象
                    explode = gameExplode.Explode(MainGame.my_tank)
                    # 将爆炸对象添加到爆炸列表中
                    MainGame.explodebigList.append(explode)
                else:
                    # 产生爆炸对象
                    explode = gameExplode.Explode(MainGame.my_tank)
                    # 将爆炸对象添加到爆炸列表中
                    MainGame.explodeList.append(explode)
                    # 添加伤害数字特效
                    sprite = gametext.FlashMessage(bullet.rect.left, bullet.rect.top, 300, str(damage),
                                                   font_size=54, color=pygame.color.Color(255, 109, 29))
                    MainGame.sprite_group.add(sprite)


# 敌方坦克与我方坦克是否发生碰撞
def enemyTank_hit_myTank(enemyTank, MainGame):
    if pygame.sprite.collide_rect(enemyTank, MainGame.my_tank):
        enemyTank.stay()


# 创建我方坦克的方法
def createMytank(tank_info: dict):
    music.Music('img/start.wav')
    return gametank.MyTank(tank_info)


# 循环遍历敌方坦克列表，展示敌方坦克
def blit_enemy_tank(MainGame):
    for enemyTank in MainGame.enemyTankList:
        # 判断当前敌方坦克是否活着
        if enemyTank.live:
            enemyTank.displayTank(MainGame)


# 循环遍历敌方建筑列表，展示敌方坦克
def blit_enemy_architecture(MainGame):
    for arch in MainGame.enemyBatteryList:
        arch.display(MainGame)


# 循环遍历敌方坦克列表，检查敌方坦克
def check_enemy_tank(MainGame):
    for enemyTank in MainGame.enemyTankList:
        # 判断当前敌方坦克是否活着
        if enemyTank.live:
            enemyTank.randMove()
            # 调用检测是否与墙壁碰撞
            enemyTank.hit_wall(MainGame)
            # 检测敌方坦克是否与我方坦克发生碰撞
            if MainGame.my_tank and MainGame.my_tank.live:
                enemyTank_hit_myTank(enemyTank, MainGame)
            # 发射子弹
            enemyBullet = enemyTank.shot()
            # 敌方子弹是否是None，如果不为None则添加到敌方子弹列表中
            if enemyBullet:
                # 加一次buff
                enemyTank.status.buff_bullet(enemyBullet)
                # 将敌方子弹存储到敌方子弹列表中
                MainGame.enemyBulletList.append(enemyBullet)
        # 不活着，从敌方坦克列表中移除
        else:
            # 获取一个随机数
            rand = random.random()
            # 记录前缀和
            record = 0
            # 添加掉落物，按概率抽取
            for key in MainGame.drops_probability:
                record += MainGame.drops_probability[key]
                if rand <= record:
                    MainGame.dropList.append(gamedrop.Drop(enemyTank, key))
                    break
            MainGame.enemyTankList.remove(enemyTank)


# 计算子弹伤害
def calculate_bullet_damage_tank(tank: gametank.Tank, bullet: gamebullet.Bullet):
    # 子弹穿透力
    penetration = bullet.penetration * (random.random() * 0.4 + 0.8)
    # 基础伤害
    damage = bullet.damage * (random.random() * 0.4 + 0.8)
    # 未击穿的伤害减益
    if penetration < tank.status.armor:
        damage *= bullet.damage_reduction_rate
    # 对伤害取整
    damage = int(damage)
    return damage


# 展示子弹的方法
def display_bullet(Bullet, main_game):
    # 将图片surface加载到窗口
    main_game.window.blit(Bullet.image, Bullet.rect)


# 循环遍历我方子弹存储列表
def blitMyBullet(MainGame):
    for myBullet in MainGame.myBulletList:
        # 判断当前的子弹是否是活着状态，如果是则进行显示
        if myBullet.live:
            display_bullet(myBullet, MainGame)


# 循环遍历我方子弹存储列表
def checkMyBullet(MainGame):
    for myBullet in MainGame.myBulletList:
        # 判断当前的子弹是否是活着状态，如果是则进行移动，
        if myBullet.live:
            # 调用子弹的移动方法
            myBullet.move()
            # 调用检测我方子弹是否与敌方坦克发生碰撞
            bullet_hit_tank(myBullet, MainGame, 'EnemyTank')
            # 检测我方子弹是否与墙壁碰撞
            hit_wall(myBullet, MainGame)
            # 检测是否和炮塔发生碰撞
            bullet_hit_architecture(myBullet, MainGame, 'EnemyBattery')
        # 否则在列表中删除
        else:
            MainGame.myBulletList.remove(myBullet)


# 循环遍历敌方子弹列表，展示敌方子弹
def blitEnemyBullet(MainGame):
    for enemyBullet in MainGame.enemyBulletList:
        if enemyBullet.live:  # 判断敌方子弹是否存活
            display_bullet(enemyBullet, MainGame)


# 循环遍历敌方子弹列表
def checkEnemyBullet(MainGame):
    for enemyBullet in MainGame.enemyBulletList:
        if enemyBullet.live:  # 判断敌方子弹是否存活
            enemyBullet.move()
            # 调用敌方子弹与我方坦克碰撞的方法
            bullet_hit_tank(enemyBullet, MainGame, 'PlayerTank')
            # 检测敌方子弹是否与墙壁碰撞
            hit_wall(enemyBullet, MainGame)
        else:
            MainGame.enemyBulletList.remove(enemyBullet)


def bullet_hit_architecture(bullet, MainGame, arch_type):
    if arch_type == 'EnemyBattery':
        # 循环遍历敌方炮塔列表，判断是否发生碰撞
        for enemyBattery in MainGame.enemyBatteryList:
            if pygame.sprite.collide_rect(enemyBattery, bullet):
                # 修改敌方炮塔和我方子弹的状态
                damage = calculate_bullet_damage_architecture(enemyBattery, bullet)
                enemyBattery.health -= damage
                if enemyBattery.health <= 0:
                    enemyBattery.live = False
                    music.Music('img/enemy1_explode.wav')
                bullet.live = False
                # 创建爆炸对象
                explode = gameExplode.Explode(enemyBattery)
                # 将爆炸对象添加到爆炸列表中
                MainGame.explodeList.append(explode)
                # 添加伤害数字特效
                sprite = gametext.FlashMessage(bullet.rect.left, bullet.rect.top, 300, str(damage), font_size=54,
                                               color=pygame.color.Color(255, 109, 29))
                MainGame.sprite_group.add(sprite)
                break
    elif arch_type == 'PlayerBattery':
        pass


# 循环遍历敌方炮塔列表，检查敌方炮塔
def check_enemy_battery(MainGame):
    for enemy_battery in MainGame.enemyBatteryList:
        # 判断当前敌方炮塔是否活着
        if enemy_battery.live:
            # 发射子弹
            bullet = enemy_battery.shot()
            # 敌方子弹是否是None，如果不为None则添加到敌方子弹列表中
            if bullet:
                # 将敌方子弹存储到敌方子弹列表中
                MainGame.enemyBulletList.append(bullet)
        # 死了，从敌方炮塔列表中移除
        else:
            MainGame.enemyBatteryList.remove(enemy_battery)


# 计算子弹伤害
def calculate_bullet_damage_architecture(arch: gamearchitecture.Architecture, bullet: gamebullet.Bullet):
    # 子弹穿透力
    penetration = bullet.penetration * (random.random() * 0.4 + 0.8)
    # 基础伤害
    damage = bullet.damage * (random.random() * 0.4 + 0.8)
    # 未击穿的伤害减益
    if penetration < arch.armor:
        damage *= bullet.damage_reduction_rate
    # 对伤害取整
    damage = int(damage)
    return damage
