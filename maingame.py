import json
import gamewall
import gametank
import gameExplode
from gamebullet import Bullet
import gamebullet
import Text
import gamegetevent
from constant import *
from gamevictory import victory
from gamedefeat import defeat
import gamedrop
import game_show_imformation
import gamearchitecture
from gamecheck import *

BG_COLOR = pygame.Color(0, 0, 0)

'''
公式：
穿透判定：总穿透力(All_Penetration)-总装甲值(All_Armor)>=0，可穿透
 总穿透力(All_Penetration)=（火炮火力(fire)+炮弹穿透(gun_Penetration)）*浮动系数(0.8~1.2)+（精准判定*100）
  精准判定取决于对装甲精准系数(to_armor_accuracy，初始值为5%)，若触发则为1，不触发则为0
伤害判定：
 穿透时：
  总伤害(All_Damage)=（火炮火力(fire)+炮弹伤害(gun_Damage)）*浮动系数(0.8~1.2)*对结构精准系数(to_structure_accuracy，初始为1)
 未穿透时：
  总伤害=（火炮火力+炮弹伤害）*浮动系数*对结构精准系数*0.2
  
'''


class MainGame:
    window: pygame.Surface = None
    my_tank: gametank.MyTank = None
    time_info = "30:00"
    # 存储敌方坦克的列表
    enemyTankList = []
    # 存储敌方炮塔的列表
    enemyBatteryList = []
    # 存储我方子弹的列表
    myBulletList = []
    # 我方当前选中的炮弹
    bullet_now = 0
    # 炮弹选择框
    bullet_choice_rect = [pygame.rect.Rect(1160, 250, 100, 45), pygame.rect.Rect(1160, 325, 100, 45),
                          pygame.rect.Rect(1160, 400, 100, 45)]
    # 定义我方炮弹数量
    AP_num = 0
    HE_num = 0
    APCR_num = 0
    # 存储敌方子弹的列表
    enemyBulletList = []
    # 存储掉落物的列表
    dropList = []
    # 存储爆炸效果的列表
    explodeList = []
    explodebigList = []
    explodesmallList = []
    # 存储墙壁的列表
    wallList = []
    waterList = []
    grassList = []
    map_info = None
    # 精灵组
    sprite_group = pygame.sprite.Group()
    # 游戏时钟
    clock = pygame.time.Clock()
    # 掉落物概率
    drops_probability = {}
    # 记录游戏开始的时刻
    time_start = 0
    # 时间上限
    time = 0

    # 开始游戏
    @staticmethod
    def startGame(n):
        map_index = n
        # 获取地图路经
        map_path = 'maps/map' + str(map_index) + '.json'
        # 设置炮弹选择为穿甲弹
        MainGame.bullet_now = 0
        # 加载主窗口
        # 初始化窗口
        pygame.display.init()
        # 设置窗口的大小及显示
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        # 读入地图信息
        with open(map_path, 'r', encoding='utf-8') as f:
            MainGame.map_info = json.load(f)
            # 初始化我方坦克
            MainGame.my_tank = createMytank(MainGame.map_info['Player'])
            # 初始化敌人，并将敌人添加到列表中
            create_enemy(MainGame, MainGame.map_info['Enemies'])
            # 初始化墙壁
            gamewall.createWall(MainGame, MainGame.map_info['MapBlocks'])
            # 读取我方炮弹数量
            MainGame.AP_num = MainGame.map_info['Bullets']['AP']
            MainGame.HE_num = MainGame.map_info['Bullets']['HE']
            MainGame.APCR_num = MainGame.map_info['Bullets']['APCR']
            # 读取掉落物概率
            MainGame.drops_probability = MainGame.map_info['DropsProbability']
            # 读取最大时间
            MainGame.time = MainGame.map_info['Time']
        # 设置窗口的标题
        pygame.display.set_caption('Soul Tank')
        # 记录开始的时刻
        time_start = pygame.time.get_ticks()
        while True:
            # 使用坦克移动的速度慢一点
            MainGame.clock.tick(60)
            # 给窗口设置填充色
            MainGame.window.fill(BG_COLOR)
            # 获取事件
            if gamegetevent.getEvent(MainGame):
                return
            # 绘制信息板
            game_show_imformation.show(MainGame)
            # 绘制剩余时间
            time_now = pygame.time.get_ticks()
            rest_time = MainGame.time + time_start - time_now
            minute = rest_time // 60000
            second = rest_time % 60000 // 1000
            MainGame.time_info = '%02d:%02d' % (minute, second)
            MainGame.window.blit(Text.getTextSufaceGreen(MainGame.time_info), (1180, 35))
            # 绘制文字
            MainGame.window.blit(Text.getTextSufaceRed('%d' % len(MainGame.enemyTankList)), (1220, 110))
            # 绘制炮弹数量
            MainGame.window.blit(Text.getTextSufaceRed('%d' % MainGame.AP_num), (1220, 260))
            MainGame.window.blit(Text.getTextSufaceRed('%d' % MainGame.HE_num), (1220, 335))
            MainGame.window.blit(Text.getTextSufaceRed('%d' % MainGame.APCR_num), (1220, 410))
            # 绘制炮弹选择框
            pygame.draw.rect(MainGame.window, blue, MainGame.bullet_choice_rect[MainGame.bullet_now], 4)
            # 调用坦克显示的方法
            # 判断我方坦克是否是否存活
            if MainGame.my_tank and MainGame.my_tank.live:
                # 展示我方坦克
                MainGame.my_tank.displayTank(MainGame)
                if MainGame.my_tank.status.health > 3:
                    MainGame.window.blit(Text.getTextSufaceGreen('%d' % MainGame.my_tank.status.health), (1220, 185))
                elif MainGame.my_tank.status.health > 1:
                    MainGame.window.blit(Text.getTextSufaceYellow('%d' % MainGame.my_tank.status.health), (1220, 185))
                else:
                    MainGame.window.blit(Text.getTextSufaceRed('%d' % MainGame.my_tank.status.health), (1220, 185))
            else:
                # 删除我方坦克
                del MainGame.my_tank
                MainGame.window.blit(Text.getTextSufaceRed('0'), (1220, 185))
                MainGame.my_tank = None
            # 循环遍历敌方坦克列表，检查敌方坦克
            check_enemy_tank(MainGame)
            # 循环遍历敌方炮塔列表，检查敌方炮塔
            check_enemy_battery(MainGame)
            # 循环遍历检查我方坦克的子弹
            checkMyBullet(MainGame)
            # 循环遍历检查掉落物
            gamedrop.check_drop(MainGame)
            # 循环遍历敌方子弹列表，检查敌方子弹
            checkEnemyBullet(MainGame)
            # 循环遍历墙壁列表，展示墙壁
            gamewall.blitWall(MainGame)
            # 循环遍历敌方坦克列表，展示敌方坦克
            blit_enemy_tank(MainGame)
            # 循环遍历敌方坦克列表，展示敌方炮塔
            blit_enemy_architecture(MainGame)
            # 循环遍历显示我方坦克的子弹
            blitMyBullet(MainGame)
            # 循环遍历敌方子弹列表，展示敌方子弹
            blitEnemyBullet(MainGame)
            # 循环遍历掉落物列表，展示敌方掉落物
            gamedrop.blit_drop(MainGame)
            # 循环遍历草列表，展示草
            gamewall.blitGrass(MainGame)
            # 循环遍历爆炸列表，展示爆炸效果
            gameExplode.blitExplode(MainGame)
            gameExplode.blitbigExplode(MainGame)
            gameExplode.blitsmallExplode(MainGame)
            # 显示特效
            MainGame.sprite_group.update(time_now)
            MainGame.sprite_group.draw(MainGame.window)
            # 判断是否有敌人剩余
            if not MainGame.enemyTankList:
                if victory().startGame(n):
                    MainGame.enemyBatteryList.clear()
                    MainGame.enemyTankList.clear()
                    MainGame.myBulletList.clear()
                    MainGame.enemyBulletList.clear()
                    MainGame.explodeList.clear()
                    MainGame.explodebigList.clear()
                    MainGame.explodesmallList.clear()
                    MainGame.wallList.clear()
                    MainGame.waterList.clear()
                    MainGame.grassList.clear()
                    MainGame.dropList.clear()
                    return
            # 如果坦克的开关是开启，才可以移动
            # 超时也是失败
            if MainGame.my_tank and MainGame.my_tank.live and rest_time >= 0:
                if not MainGame.my_tank.stop:
                    MainGame.my_tank.move()
                    # 检测我方坦克是否与墙壁发生碰撞
                    MainGame.my_tank.hit_wall(MainGame)
                    # 检测我方坦克是否与敌方坦克发生碰撞
                    MainGame.my_tank.myTank_hit_enemyTank(MainGame)
            else:
                if defeat().fail(n):
                    MainGame.enemyBatteryList.clear()
                    MainGame.enemyTankList.clear()
                    MainGame.myBulletList.clear()
                    MainGame.dropList.clear()
                    MainGame.enemyBulletList.clear()
                    MainGame.explodeList.clear()
                    MainGame.explodebigList.clear()
                    MainGame.explodesmallList.clear()
                    MainGame.wallList.clear()
                    MainGame.waterList.clear()
                    MainGame.grassList.clear()
                    MainGame.dropList.clear()
                return
            pygame.display.update()


# 初始化敌人，并将敌人添加到列表中
def create_enemy(MainGame, enemy_info: dict):
    for enemy in enemy_info:
        if enemy['EnemyType'] == "Light":
            enemy = gametank.EnemyTank('LightTank', enemy['x'] * 60, enemy['y'] * 60)
            MainGame.enemyTankList.append(enemy)
        elif enemy['EnemyType'] == "Middle":
            enemy = gametank.EnemyTank('MediumTank', enemy['x'] * 60, enemy['y'] * 60)
            MainGame.enemyTankList.append(enemy)
        elif enemy['EnemyType'] == "Heavy":
            enemy = gametank.EnemyTank('HeavyTank', enemy['x'] * 60, enemy['y'] * 60)
            MainGame.enemyTankList.append(enemy)
        elif enemy['EnemyType'] == "Heavy2":
            enemy = gametank.EnemyTank('HeavyTank2', enemy['x'] * 60, enemy['y'] * 60)
            MainGame.enemyTankList.append(enemy)
        elif enemy['EnemyType'] == "Battery":
            enemy = gamearchitecture.Battery('Battery', enemy['x'] * 60, enemy['y'] * 60)
            MainGame.enemyBatteryList.append(enemy)

