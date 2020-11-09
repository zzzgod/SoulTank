#导入pygame模块
import pygame,time,random
from pygame.sprite import Sprite
import music
'''
单人模式
    剧情模式
        关卡一
        二...
    小游戏
        我的坦克不能开炮
        夺旗
    生存模式
        谁笑到最后？
双人模式
    
仓库
    养成？
图鉴
    
退出
'''
SCREEN_WIDTH=1280
SCREEN_HEIGHT=720
GAME_WIDTH=1140
GAME_HEIGHT=720
BG_COLOR=pygame.Color(0,0,0)
TEXT_COLOR_RED=pygame.Color(255,0,0)
TEXT_COLOR_GREEN=pygame.Color(50,205,50)
TEXT_COLOR_YELLOW=pygame.Color(255,255,0)
lasttime=0
fullscreen=0
#定义一个基类
class BaseItem(Sprite):
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

class MainGame():
    window=None
    my_tank=None
    #存储敌方坦克的列表
    enemyTankList=[]
    #定义敌方坦克的数量
    enemyTankCount=10
    #存储我方子弹的列表
    myBulletList=[]
    #存储敌方子弹的列表
    enemyBulletList=[]
    #存储爆炸效果的列表
    explodeList=[]
    explodebigList=[]
    explodesmallList=[]
    #存储墙壁的列表
    wallList=[]
    def __init__(self):
        pass
    #开始游戏
    def startGame(self):
        #加载主窗口
        #初始化窗口
        pygame.display.init()
        #设置窗口的大小及显示
        MainGame.window=pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
        #初始化我方坦克
        self.createMytank()
        #初始化敌方坦克，并将敌方坦克添加到列表中
        self.createEnemyTank()
        #初始化墙壁
        self.createWall()
        #设置窗口的标题
        pygame.display.set_caption('坦克大战1.03')
        while True:
            #使用坦克移动的速度慢一点
            time.sleep(0.02)
            #给窗口设置填充色
            MainGame.window.fill(BG_COLOR)
            #获取事件
            self.getEvent()
            #信息板
            image_imformation=pygame.image.load('img/imformation.gif')
            MainGame.window.blit(image_imformation,(1140,0))
            #绘制图标
            image_enemy_tank_num=pygame.image.load('img/enemy_tank_num_black.gif')
            MainGame.window.blit(image_enemy_tank_num,(1170,25))
            image_enemy_tank_num=pygame.image.load('img/my_tank_hp_black.gif')
            MainGame.window.blit(image_enemy_tank_num,(1170,100))
            #绘制文字
            MainGame.window.blit(self.getTextSufaceRed('%d'%len(MainGame.enemyTankList)),(1220,35))
            #调用坦克显示的方法
            #判断我方坦克是否是否存活
            if MainGame.my_tank and MainGame.my_tank.live:
                MainGame.my_tank.displayTank()
                if MainGame.my_tank.hp>3:
                    MainGame.window.blit(self.getTextSufaceGreen('%d'%MainGame.my_tank.hp),(1220,110))
                elif MainGame.my_tank.hp>1:
                    MainGame.window.blit(self.getTextSufaceYellow('%d'%MainGame.my_tank.hp),(1220,110))
                else :
                    MainGame.window.blit(self.getTextSufaceRed('%d'%MainGame.my_tank.hp),(1220,110))
            else:
                #删除我方坦克
                del MainGame.my_tank
                MainGame.window.blit(self.getTextSufaceRed('0'),(1220,110))
                MainGame.my_tank=None
            #循环遍历敌方坦克列表，展示敌方坦克
            self.blitEnemyTank()
            #循环遍历显示我方坦克的子弹
            self.blitMyBullet()
            #循环遍历敌方子弹列表，展示敌方子弹
            self.blitEnemyBullet()
            #循环遍历墙壁列表，展示墙壁
            self.blitWall()
            #循环遍历爆炸列表，展示爆炸效果
            self.blitExplode()
            self.blitbigExplode()
            self.blitsmallExplode()
            #调用移动方法
            #如果坦克的开关是开启，才可以移动
            if MainGame.my_tank and MainGame.my_tank.live:
                if not MainGame.my_tank.stop:
                    MainGame.my_tank.move()
                    #检测我方坦克是否与墙壁发生碰撞
                    MainGame.my_tank.hitWall()
                    #检测我方坦克是否与敌方坦克发生碰撞
                    MainGame.my_tank.myTank_hit_enemyTank()

            pygame.display.update()
    # 循环遍历墙壁列表，展示墙壁
    def blitWall(self):
        for wall in MainGame.wallList:
            #判断墙壁是否存活
            if wall.live:
                #调用墙壁的显示方法
                wall.displayWall()
            else:
                #从墙壁列表移出
                MainGame.wallList.remove(wall)
    #初始化墙壁
    def createWall(self):
        with open('map.txt','r') as f:
            commands = f.readlines()
            for i in commands:
                eval(i.strip())
        for i in range(19):
             #初始化墙壁
             wall1=Wall(i*60,220)
             wall2=Wall(i*60,420)
             #将墙壁添加到列表中
             MainGame.wallList.append(wall1)
             MainGame.wallList.append(wall2)
    #创建我方坦克的方法
    def createMytank(self):
        MainGame.my_tank = MyTank(350, 300)
        music.Music('img/start.wav')
    # 初始化敌方坦克，并将敌方坦克添加到列表中
    def createEnemyTank(self):
        top=100
        #循环生成敌方坦克
        for i in range(MainGame.enemyTankCount):
            left=random.randint(0,600)
            speed=random.randint(1,4)
            enemy=EnemyTank(left,top,speed)
            MainGame.enemyTankList.append(enemy)
    #循环展示小爆炸效果
    def blitsmallExplode(self):
        for explode in MainGame.explodesmallList:
            #判断是否活着
            if explode.live:
                #展示
                explode.displaysmallExplode()
            else:
                #在爆炸列表中移除
                MainGame.explodesmallList.remove(explode)
    #循环展示爆炸效果
    def blitExplode(self):
        for explode in MainGame.explodeList:
            #判断是否活着
            if explode.live:
                #展示
                explode.displayExplode()
            else:
                #在爆炸列表中移除
                MainGame.explodeList.remove(explode)
    #循环展示大爆炸效果
    def blitbigExplode(self):
        for explode in MainGame.explodebigList:
            #判断是否活着
            if explode.live:
                #展示
                explode.displaybigExplode()
            else:
                #在爆炸列表中移除
                MainGame.explodebigList.remove(explode)
    # 循环遍历敌方坦克列表，展示敌方坦克
    def  blitEnemyTank(self):
        for enemyTank in MainGame.enemyTankList:
            #判断当前敌方坦克是否活着
            if enemyTank.live:
                enemyTank.displayTank()
                enemyTank.randMove()
                #调用检测是否与墙壁碰撞
                enemyTank.hitWall()
                #检测敌方坦克是否与我方坦克发生碰撞
                if MainGame.my_tank and MainGame.my_tank.live:
                    enemyTank.enemyTank_hit_myTank()
                # 发射子弹
                enemyBullet = enemyTank.shot()
                # 敌方子弹是否是None，如果不为None则添加到敌方子弹列表中
                if enemyBullet:
                    # 将敌方子弹存储到敌方子弹列表中
                    MainGame.enemyBulletList.append(enemyBullet)
            else:#不活着，从敌方坦克列表中移除
                MainGame.enemyTankList.remove(enemyTank)


    #循环遍历我方子弹存储列表
    def blitMyBullet(self):
        for myBullet in MainGame.myBulletList:
            #判断当前的子弹是否是活着状态，如果是则进行显示及移动，
            if myBullet.live:
                myBullet.display_my_Bullet()
                # 调用子弹的移动方法
                myBullet.move()
                #调用检测我方子弹是否与敌方坦克发生碰撞
                myBullet.myBullet_hit_enemyTank()
                # 检测我方子弹是否与墙壁碰撞
                myBullet.hitWall()
            # 否则在列表中删除
            else:
                MainGame.myBulletList.remove(myBullet)

    # 循环遍历敌方子弹列表，展示敌方子弹
    def blitEnemyBullet(self):
        for enemyBullet in MainGame.enemyBulletList:
            if enemyBullet.live: #判断敌方子弹是否存活
                enemyBullet.displayBullet()
                enemyBullet.move()
                #调用敌方子弹与我方坦克碰撞的方法
                enemyBullet.enemyBullet_hit_myTank()
                #检测敌方子弹是否与墙壁碰撞
                enemyBullet.hitWall()
            else:
                MainGame.enemyBulletList.remove(enemyBullet)


    #结束游戏
    def endGame(self):
        print('谢谢使用，欢迎再次使用')
        exit()
    #左上角文字的绘制
    def getTextSufaceGreen(self,text):
        #初始化字体模块
        pygame.font.init()
        #查看所有的字体名称
        # print(pygame.font.get_fonts())
        #获取字体Font对象
        font=pygame.font.SysFont('heiti',36)
        #绘制文字信息
        textSurface=font.render(text,True,TEXT_COLOR_GREEN)
        return textSurface
    def getTextSufaceYellow(self,text):
        #初始化字体模块
        pygame.font.init()
        #查看所有的字体名称
        # print(pygame.font.get_fonts())
        #获取字体Font对象
        font=pygame.font.SysFont('heiti',36)
        #绘制文字信息
        textSurface=font.render(text,True,TEXT_COLOR_YELLOW)
        return textSurface
    def getTextSufaceRed(self,text):
        #初始化字体模块
        pygame.font.init()
        #查看所有的字体名称
        # print(pygame.font.get_fonts())
        #获取字体Font对象
        font=pygame.font.SysFont('heiti',36)
        #绘制文字信息
        textSurface=font.render(text,True,TEXT_COLOR_RED)
        return textSurface
    #获取事件
    def getEvent(self):
        #获取所有事件
        eventList= pygame.event.get()
        #遍历事件
        for event in eventList:
            #判断按下的键是关闭还是键盘按下
            #如果按的是退出，关闭窗口
            if event.type == pygame.QUIT:
                self.endGame()
            #如果是键盘的按下
            if event.type == pygame.KEYDOWN:
                #esc键切换全屏和窗口
                if event.key == pygame.K_ESCAPE:
                    global fullscreen
                    if fullscreen==1:
                       pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
                       fullscreen=0
                    else:
                       pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT],pygame.FULLSCREEN)
                       fullscreen=1
                #当坦克不重在死亡
                if not MainGame.my_tank:
                   #判断按下的是1键，让坦克重生
                   if event.key == pygame.K_1:
                       # 让我方坦克重生及调用创建坦克的方法
                       self.createMytank()
                if MainGame.my_tank and MainGame.my_tank.live:
                   # 判断按下的是上、下、左、右
                   if event.key == pygame.K_a:
                       # 切换方向
                       MainGame.my_tank.direction = 'L'
                       # 修改坦克的开关状态
                       MainGame.my_tank.stop = False
                       # MainGame.my_tank.move()
                       print('按下a键，坦克向左移动')
                   elif event.key == pygame.K_d:
                       # 切换方向
                       MainGame.my_tank.direction = 'R'
                       # 修改坦克的开关状态
                       MainGame.my_tank.stop = False
                       # MainGame.my_tank.move()
                       print('按下d键，坦克向右移动')
                   elif event.key == pygame.K_w:
                       # 切换方向
                       MainGame.my_tank.direction = 'U'
                       # 修改坦克的开关状态
                       MainGame.my_tank.stop = False
                       # MainGame.my_tank.move()
                       print('按下w键，坦克向上移动')
                   elif event.key == pygame.K_s:
                       # 切换方向
                       MainGame.my_tank.direction = 'D'
                       # 修改坦克的开关状态
                       MainGame.my_tank.stop = False
                       # MainGame.my_tank.move()
                       print('按下s键，坦克向下移动')
                   elif event.key == pygame.K_j:
                       print('发射子弹')
                       # 如果当前我方子弹列表的大小 射击间隔大于1才可以创建
                       nowtime=time.perf_counter()
                       global lasttime
                       timediffer=nowtime-lasttime
                       print(nowtime)
                       print(lasttime)
                       print(timediffer)
                       if timediffer > 1:
                           # 创建我方坦克发射的子弹
                           myBullet = Bullet(MainGame.my_tank)
                           MainGame.myBulletList.append(myBullet)
                           #我方坦克发射子弹添加音效
                           music.Music('img/fire1.wav')
                           lasttime=nowtime



            #松开方向键，坦克停止移动，修改坦克的开关状态
            if event.type == pygame.KEYUP:
                #判断松开的键是上、下、左、右时候才停止坦克移动
                if  MainGame.my_tank and MainGame.my_tank.live:
                    if (MainGame.my_tank.direction == 'U' and event.key==pygame.K_w) or(MainGame.my_tank.direction == 'L' and event.key==pygame.K_a) or(MainGame.my_tank.direction == 'D' and event.key==pygame.K_s) or(MainGame.my_tank.direction == 'R' and event.key==pygame.K_d) :
                        MainGame.my_tank.stop = True

class Tank(BaseItem):
    #添加距离左边left 距离上边top
    def __init__(self,left,top):
        #保存加载的图片
        self.images={
            'U':pygame.image.load('img/p1tankU.gif'),
            'D':pygame.image.load('img/p1tankD.gif'),
            'L':pygame.image.load('img/p1tankL.gif'),
            'R':pygame.image.load('img/p1tankR.gif'),
        }
        #方向
        self.direction='L'
        #根据当前图片的方向获取图片 surface
        self.image=self.images[self.direction]
        #根据图片获取区域
        self.rect=self.image.get_rect()
        #设置区域的left 和top
        self.rect.left=left
        self.rect.top=top
        #速度  决定移动的快慢
        self.speed=5
        #坦克移动的开关
        self.stop=True
        #是否活着
        self.live=True
        #新增属性原来坐标
        self.oldLeft=self.rect.left
        self.oldTop=self.rect.top

    #移动
    def move(self):
        #标记坦克是否接触边界
        self.touch=1
        #移动后记录原始的坐标
        self.oldLeft=self.rect.left
        self.oldTop=self.rect.top
        #判断坦克的方向进行移动
        if self.direction == 'L':
            if self.rect.left>0:
                self.rect.left -= self.speed
            else:
                self.touch=0
        elif self.direction == 'U':
            if self.rect.top>0:
                self.rect.top -= self.speed
            else:
                self.touch=0
        elif self.direction == 'D':
            if self.rect.top+self.rect.height<GAME_HEIGHT:
                self.rect.top += self.speed
            else:
                self.touch=0
        elif self.direction == 'R':
            if self.rect.left+self.rect.height<GAME_WIDTH:
                self.rect.left += self.speed
            else:
                self.touch=0
        return self.touch

    #射击
    def shot(self):
        return Bullet(self)
    #
    def stay(self):
        self.rect.left=self.oldLeft
        self.rect.top=self.oldTop
    #检测坦克是否与墙壁发生碰撞
    def hitWall(self):
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(self,wall):
                #将坐标设置为移动之前的坐标
                self.stay()
    #展示坦克的方法
    def displayTank(self):
        #获取展示的对象
        self.image=self.images[self.direction]
        #调用blit方法展示
        MainGame.window.blit(self.image,self.rect)
#我方坦克
class MyTank(Tank):
    def __init__(self,left,top):
        super(MyTank, self).__init__(left,top)
        #坦克血量
        self.hp=5

    #检测我方坦克与敌方坦克发生碰撞
    def myTank_hit_enemyTank(self):
        #循环遍历敌方坦克列表
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(self,enemyTank):
                self.stay()
#敌方坦克
class EnemyTank(Tank):
    def __init__(self,left,top,speed):
        #调用父类的初始化方法
        super(EnemyTank, self).__init__(left,top)
        #加载图片集
        self.images={
            'U':pygame.image.load('img/enemy1U.gif'),
            'D':pygame.image.load('img/enemy1D.gif'),
            'L':pygame.image.load('img/enemy1L.gif'),
            'R':pygame.image.load('img/enemy1R.gif')
        }
        #方向,随机生成敌方坦克的方向
        self.direction=self.randDirection()
        #根据方向获取图片
        self.image=self.images[self.direction]
        #区域
        self.rect=self.image.get_rect()
        #对left和top进行赋值
        self.rect.left=left
        self.rect.top=top
        #速度
        self.speed=speed
        #移动开关键
        self.flag=True
        #薪增加一个步数变量 step
        self.step=60
        #坦克血量
        self.hp=100
        

    #敌方坦克与我方坦克是否发生碰撞
    def enemyTank_hit_myTank(self):
        if pygame.sprite.collide_rect(self,MainGame.my_tank):
            self.stay()
    # 随机生成敌方坦克的方向
    def randDirection(self):
        num=random.randint(1,4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return "L"
        elif num == 4:
            return 'R'

    #敌方坦克随机移动的方法
    def randMove(self):
        if self.step<=0:
            #修改方向
            self.direction=self.randDirection()
            #让步数复位
            self.step=60
        else:
            self.touch=self.move()
            #让步数递减
            self.step-=1
            #如果接触墙壁就马上转向
            if self.touch==0:
                self.step=-1
    #重写shot()
    def shot(self):
        #随机生成100以内的数
        num=random.randint(1,1000)
        if num<30:
            return Bullet(self)
#子弹类
class Bullet(BaseItem):
    def __init__(self,tank):
        #加载图片
        self.image=pygame.image.load('img/enemymissile.gif')
        self.image_my=pygame.image.load('img/tankmissile.gif')
        #坦克的方向决定子弹的方向
        self.direction=tank.direction
        #获取区域
        self.rect=self.image.get_rect()
        #子弹的left和top与方向有关
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        #子弹的速度
        self.speed=6
        #子弹的状态，是否碰到墙壁，如果碰到墙壁，修改此状态
        self.live=True
    #移动
    def move(self):
        if self.direction == 'U':
            if self.rect.top>0:
                self.rect.top-=self.speed
            else:
                #修改子弹的状态
                self.live=False
        elif self.direction == 'R':
            if self.rect.left+self.rect.width<GAME_WIDTH:
                self.rect.left+=self.speed
            else:
                #修改子弹的状态
                self.live=False
        elif self.direction =='D':
            if self.rect.top+self.rect.height<GAME_HEIGHT:
                self.rect.top+=self.speed
            else:
                #修改子弹的状态
                self.live=False
        elif self.direction == 'L':
            if self.rect.left>0:
                self.rect.left-=self.speed
            else:
                #修改子弹的状态
                self.live=False
    #子弹是否碰撞墙壁
    def hitWall(self):
        #循环遍历墙壁列表
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(self,wall):
                #修改子弹的生存状态，让子弹消失
                self.live=False
                #墙壁的生命值减小
                wall.hp-=1
                if wall.hp<=0:
                    #修改墙壁的生存状态
                    wall.live=False
                    # 产生爆炸对象
                    explode = Explode(wall)
                    # 将爆炸对象添加到爆炸列表中
                    MainGame.explodesmallList.append(explode)
                    

                    


    #展示子弹的方法
    def displayBullet(self):
        #将图片surface加载到窗口
        MainGame.window.blit(self.image,self.rect)

    def display_my_Bullet(self):
        #将图片surface加载到窗口
        MainGame.window.blit(self.image_my,self.rect)
    #我方子弹与敌方坦克的碰撞
    def myBullet_hit_enemyTank(self):
        #循环遍历敌方坦克列表，判断是否发生碰撞
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(enemyTank,self):
                #修改敌方坦克和我方子弹的状态
                enemyTank.hp-=1
                if enemyTank.hp<=99:
                    enemyTank.live=False
                    music.Music('img/enemy1_explode.wav')
                self.live=False
                #创建爆炸对象
                explode=Explode(enemyTank)
                #将爆炸对象添加到爆炸列表中
                MainGame.explodeList.append(explode)
    #敌方子弹与我方坦克的碰撞
    def enemyBullet_hit_myTank(self):
        if MainGame.my_tank and MainGame.my_tank.live:
            if pygame.sprite.collide_rect(MainGame.my_tank, self):
                # 修改敌方子弹与我方坦克的状态
                self.live = False
                MainGame.my_tank.hp-=1
                if MainGame.my_tank.hp<=0:
                    MainGame.my_tank.live=False
                    # 产生爆炸对象
                    explode = Explode(MainGame.my_tank)
                    # 将爆炸对象添加到爆炸列表中
                    MainGame.explodebigList.append(explode)
                else:
                    # 产生爆炸对象
                    explode = Explode(MainGame.my_tank)
                    # 将爆炸对象添加到爆炸列表中
                    MainGame.explodeList.append(explode)
class Wall():
    def __init__(self,left,top):
        #加载墙壁图片
        self.image=pygame.image.load('img/walls.gif')
        #获取墙壁的区域
        self.rect=self.image.get_rect()
        #设置位置left、top
        self.rect.left=left
        self.rect.top=top
        #是否存活
        self.live=True
        #设置生命值
        self.hp=3
    #展示墙壁的方法
    def displayWall(self):
        MainGame.window.blit(self.image,self.rect)
class Explode():
    def __init__(self,tank):
        #爆炸的位置由当前子弹打中的坦克位置决定
        self.rect=tank.rect
        self.images=[
            pygame.image.load('img/blast0.gif'),
            pygame.image.load('img/blast1.gif'),
            pygame.image.load('img/blast2.gif'),
            pygame.image.load('img/blast3.gif'),
            pygame.image.load('img/blast4.gif'),
            pygame.image.load('img/blast5.gif'),
            pygame.image.load('img/blast6.gif'),
            pygame.image.load('img/blast7.gif'),
        ]
        self.step=0
        self.divstep=0
        self.image=self.images[self.step]
        #是否活着
        self.live=True
    #展示小爆炸效果的方法
    def displaysmallExplode(self):
        if self.step<3:
            #根据索引获取爆炸对象
            self.image=self.images[self.step]
            self.divstep+=1
            if self.divstep%3==0:
                self.step+=1
            #添加到主窗口
            MainGame.window.blit(self.image,(self.rect[0]-30,self.rect[1]-30))
        else:
            #修改活着的状态
            self.live=False
            self.step=0
            self.divstep=0
    #展示爆炸效果的方法
    def displayExplode(self):
        if self.step<5:
            #根据索引获取爆炸对象
            self.image=self.images[self.step]
            self.divstep+=1
            if self.divstep%3==0:
                self.step+=1
            #添加到主窗口
            MainGame.window.blit(self.image,(self.rect[0]-30,self.rect[1]-30))
        else:
            #修改活着的状态
            self.live=False
            self.step=0
            self.divstep=0
    #展示大爆炸效果的方法
    def displaybigExplode(self):
        if self.step<8:
            #根据索引获取爆炸对象
            self.image=self.images[self.step]
            self.divstep+=1
            if self.divstep%5==0:
                self.step+=1
            #添加到主窗口
            MainGame.window.blit(self.image,(self.rect[0]-30,self.rect[1]-30))
        else:
            #修改活着的状态
            self.live=False
            self.step=0
            self.divstep=0



if __name__=='__main__':
    #lc yyds
    MainGame().startGame()
    # MainGame().getTextSuface()
