import tkinter as tk

strings = []


def set_img(i, j, choice):
    def f():
        strings[i][j].set(choice.get())
    return f


if __name__ == '__main__':
    # 初始化窗口
    window = tk.Tk()
    # 标题
    window.title('地图编辑器')
    # 设置窗口大小
    window.geometry('1280x720')
    # 左侧工具栏
    frame1 = tk.Frame(window)
    # 生成提示文本
    text = tk.Label(frame1, text='道具栏', width=20, height=2, font=('songti', 18)).pack(side='top')
    frame1.pack(side='left')
    # 记录选择
    choice = tk.StringVar()
    choice.set('0')
    # 生成一堆按钮
    for i in range(1, 10):
        check_button = tk.Checkbutton(frame1, text=str(i), variable=choice, onvalue=str(i), offvalue='0', width=25, height=2,
                                      bg='green', pady=10).pack()
    # 右侧显示地图
    frame2 = tk.Frame(window, pady=5, padx=10)
    for i in range(12):
        strings.append([])
        for j in range(19):
            s = tk.StringVar()
            label = tk.Button(frame2, textvariable=s, width=6, height=2, bg='green', command=set_img(i, j, choice)).grid(row=i, column=j)
            strings[-1].append(s)
    frame2.pack(side='right')
    # 窗口主循环
    window.mainloop()
