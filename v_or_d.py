from gamevictory import victory
from gamedefeat import defeat
# 判断是否有敌人剩余
def V_or_D(n,MainGame,rest_time):
            if n==6:
                if not MainGame.enemyBatteryList:
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
                        return True
            elif n==11:
                if not MainGame.enemyCommandList:
                    if victory().startGame(n):
                        MainGame.enemyCommandList.clear()
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
                        return True
            elif n==13:
                if MainGame.my_tank and MainGame.my_tank.live and rest_time <= 0 and MainGame.myCommandList:
                    if victory().startGame(n):
                        MainGame.enemyCommandList.clear()
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
                        return True
            else:
                if not MainGame.enemyTankList:
                    if victory().startGame(n):
                        MainGame.enemyBatteryList.clear()
                        MainGame.myBatteryList.clear()
                        MainGame.enemyCommandList.clear()
                        MainGame.myCommandList.clear()
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
                        return True
            # 如果坦克的开关是开启，才可以移动
            # 超时也是失败
            if MainGame.my_tank and MainGame.my_tank.live and rest_time >= 0:
                if not MainGame.my_tank.stop:
                    MainGame.my_tank.move()
                    # 检测我方坦克是否与墙壁发生碰撞
                    MainGame.my_tank.hit_wall(MainGame)
                    # 检测我方坦克是否与敌方坦克发生碰撞
                    MainGame.my_tank.myTank_hit_enemyTank(MainGame)
            else :
                if defeat().fail(n):
                    MainGame.enemyBatteryList.clear()
                    MainGame.enemyCommandList.clear()
                    MainGame.myBatteryList.clear()
                    MainGame.myCommandList.clear()
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
                    return True
            if n==13:
                if not MainGame.myCommandList:
                    if defeat().fail(n):
                        MainGame.myCommandList.clear()
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
                        return True