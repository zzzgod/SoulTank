import os
import tkinter as tk
from tkinter.filedialog import asksaveasfile
from tkinter.messagebox import showwarning

player_count = 0
labels = []
indices = []
item_name = ['Empty', 'Grass', 'Steel', 'Wall', 'Water', 'LightTank', 'MediumTank', 'HeavyTank', 'Player']


def set_img(i, j, choice):
    def f():
        n = int(choice.get())
        global player_count
        if 0 <= n <= 8:
            # 控制只能有一个玩家的坦克
            if indices[i][j] == 8:
                player_count -= 1
            if n == 8:
                if player_count >= 1:
                    showwarning(title='警告',message='玩家数量不能多于1个。')
                    return
                else:
                    player_count += 1
            labels[i][j]['image'] = imgs[n]
            indices[i][j] = n
        window.update()

    return f


def save():
    file = asksaveasfile(filetypes=[('地图文件', '.json')])
    # 如果放弃保存
    if file is None:
        return
    # 记录输出字符串, flag用来控制结束时不输出逗号
    block = ''
    flag_block = 0
    enemy_tank = ''
    flag_enemy_tank = 0
    player = ''
    for i in range(12):
        for j in range(19):
            # 记录方块信息
            if 1 <= indices[i][j] <= 4:
                # 第一次不输入换行符
                if flag_block:
                    block += ',\n'
                flag_block = 1
                block += '\t\t{"BlockType": "%s", "x": %d, "y": %d}' % (item_name[indices[i][j]], j, i)
            # 记录敌方坦克信息
            elif 5 <= indices[i][j] <= 7:
                if flag_enemy_tank:
                    enemy_tank += ',\n'
                flag_enemy_tank = 1
                enemy_tank += '\t\t{"EnemyType": "%s", "x": %d, "y": %d}' % (item_name[indices[i][j]], j, i)
            # 记录我方坦克信息
            elif indices[i][j] == 8:
                player = '\t"Player": {"x": %d, "y": %d},\n' % (j, i)
    file.write('{\n\t"MapBlocks": [\n')
    file.write(block)
    file.write('\n\t],\n')
    file.write(player)
    file.write('\t"Enemies": [\n')
    file.write(enemy_tank)
    file.write('\n\t]\n}')
    file.close()


if __name__ == '__main__':
    # 初始化窗口
    window = tk.Tk()
    # 图片列表
    imgs = [tk.PhotoImage(file='../img/blocks/background.png'),
            tk.PhotoImage(file='../img/blocks/grass.gif'),
            tk.PhotoImage(file='../img/blocks/steels.gif'),
            tk.PhotoImage(file='../img/blocks/walls.gif'),
            tk.PhotoImage(file='../img/blocks/water.gif'),
            tk.PhotoImage(file='../img/tank/LightTankUp.gif'),
            tk.PhotoImage(file='../img/tank/MediumTankUp.gif'),
            tk.PhotoImage(file='../img/tank/HeavyTankUp.gif'),
            tk.PhotoImage(file='../img/tank/PlayerTankUp.gif'),
            ]
    # 标题
    window.title('地图编辑器')
    # 设置窗口大小
    window.geometry('1580x840')
    # 左侧工具栏
    frame1 = tk.Frame(window)
    # 生成提示文本
    text = tk.Label(frame1, text='道具栏', width=20, height=2, font=('songti', 18)).pack(side='top')
    frame1.pack(side='left')
    # 记录选择
    choice = tk.StringVar()
    choice.set('0')
    # 生成一堆按钮
    for i in range(1, 9):
        if i < len(item_name):
            s = item_name[i]
        else:
            s = '啥都没有'
        tk.Checkbutton(frame1, text=s, variable=choice, onvalue=str(i), offvalue='0', width=25,
                       height=2, bg='yellow', pady=10).pack()
    # 保存按钮
    tk.Button(frame1, text='保存', width=10, bg='LightGreen', font=('songti', 18), command=save).pack()
    # 右侧显示地图
    frame2 = tk.Frame(window, pady=5, padx=10)
    for i in range(12):
        labels.append([])
        indices.append([])
        for j in range(19):
            label = tk.Button(frame2, image=imgs[0], width=60, height=60, command=set_img(i, j, choice))
            label.grid(row=i, column=j)
            labels[-1].append(label)
            indices[-1].append(0)
    frame2.pack(side='right')
    # 窗口主循环
    window.mainloop()
