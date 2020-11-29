import tkinter as tk

labels = []


def set_img(i, j, choice):

    def f():
        n = int(choice.get())
        if 0 <= n <= 4:
            labels[i][j]['image'] = imgs[n]
        window.update()

    return f


if __name__ == '__main__':
    # 初始化窗口
    window = tk.Tk()
    # 图片列表
    imgs = [tk.PhotoImage(file='../img/blocks/background.png'),
             tk.PhotoImage(file='../img/blocks/grass.gif'),
             tk.PhotoImage(file='../img/blocks/steels.gif'),
             tk.PhotoImage(file='../img/blocks/walls.gif'),
             tk.PhotoImage(file='../img/blocks/water.gif')]
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
        check_button = tk.Checkbutton(frame1, text=str(i), variable=choice, onvalue=str(i), offvalue='0', width=25,
                                      height=2,
                                      bg='green', pady=10).pack()
    # 右侧显示地图
    frame2 = tk.Frame(window, pady=5, padx=10)
    for i in range(12):
        labels.append([])
        for j in range(19):
            label = tk.Button(frame2, image=imgs[0], width=60, height=60, command=set_img(i, j, choice))
            label.grid(row=i, column=j)
            labels[-1].append(label)
    frame2.pack(side='right')
    # 窗口主循环
    window.mainloop()
