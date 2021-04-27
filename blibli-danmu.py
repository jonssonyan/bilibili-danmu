import threading
import time
import tkinter.simpledialog  # 使用Tkinter前需要先导入
from tkinter import END, messagebox

import requests


class Danmu():
    def __init__(self, room_id):
        # 弹幕url
        self.url = 'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory'
        # 请求头
        self.headers = {
            'Host': 'api.live.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        }
        # 定义POST传递的参数
        self.data = {
            'roomid': room_id,
            'csrf_token': '',
            'csrf': '',
            'visit_id': '',
        }
        # 日志写对象
        self.log_file_write = open('danmu.log', mode='a', encoding='utf-8')
        # 读取日志
        log_file_read = open('danmu.log', mode='r', encoding='utf-8')
        self.log = log_file_read.readlines()

    def get_danmu(self):
        # 暂停0.5防止cpu占用过高
        time.sleep(1)
        # 获取直播间弹幕
        html = requests.post(url=self.url, headers=self.headers, data=self.data).json()
        # 解析弹幕列表
        for content in html['data']['room']:
            # 获取昵称
            nickname = content['nickname']
            # 获取发言
            text = content['text']
            # 获取发言时间
            timeline = content['timeline']
            # 记录发言
            msg = timeline + ' ' + nickname + ': ' + text
            # 判断对应消息是否存在于日志，如果和最后一条相同则打印并保存
            if msg + '\n' not in self.log:
                # 打印消息
                listb.insert(END, msg)
                listb.see(END)
                # 保存日志
                self.log_file_write.write(msg + '\n')
                # 添加到日志列表
                self.log.append(msg + '\n')
            # 清空变量缓存
            nickname = ''
            text = ''
            timeline = ''
            msg = ''


def bilibili(delay, room_id):
    # 创建bDanmu实例
    bDanmu = Danmu(room_id)
    while True:
        # 暂停防止cpu占用过高
        time.sleep(delay)
        # 获取弹幕
        bDanmu.get_danmu()


def author():
    # 弹出对话框
    messagebox.showinfo(title='关于', message='作者：阿壮Jonson\n日期：2021年2月4日\n微信公众号：科技猫')


# 实例化object，建立窗口window
window = tkinter.Tk()
# 给窗口的可视化起名字
window.title('BiliBli弹幕查看工具')
# 设定窗口的大小(长 * 宽)
window.minsize(300, 500)
window.geometry('400x600+250+100')

# 菜单栏
menubar = tkinter.Menu(window)
# Open放在菜单栏中，就是装入容器
menubar.add_command(label='关于', command=author)
# 创建菜单栏完成后，配置让菜单栏menubar显示出来
window.config(menu=menubar)

# 创建一个主frame，长在主window窗口上
frame = tkinter.Frame(window)
frame.pack()

# 创建第二层框架frame，长在主框架frame上面
# 上
frame_t = tkinter.Frame(frame)
# 下
frame_b = tkinter.Frame(frame)
frame_t.pack(side=tkinter.TOP)
frame_b.pack(side=tkinter.BOTTOM)

# 创建标签
tkinter.Label(frame_t, text='请输入房间号：', width=10, font=('Arial', 10)).pack(side=tkinter.LEFT)
# 显示成明文形式
default_text = tkinter.StringVar()
default_text.set("21089733")
e1 = tkinter.Entry(frame_t, show=None, width=15, textvariable=default_text, font=('Arial', 10))
e1.pack(side=tkinter.LEFT)


# 定义两个触发事件时的函数start_point和end_point（注意：因为Python的执行顺序是从上往下，所以函数一定要放在按钮的上面）
# 开始
def start_point():
    try:
        room = e1.get()
        room_int = int(room)
        e1.configure(state=tkinter.DISABLED)
        b1.configure(state=tkinter.DISABLED)
        b2.configure(state=tkinter.NORMAL)
        if room_int is not None:
            # 创建获取弹幕线程
            t = threading.Thread(target=bilibili, args=(0.5, str(room_int),))
            t.setDaemon(True)
            t.start()
    except ValueError:
        messagebox.showinfo(title='警告', message='输入的房间号格式不正确,请再次尝试输入!')


# 停止
def end_point():
    e1.configure(state=tkinter.NORMAL)
    b1.configure(state=tkinter.NORMAL)
    b2.configure(state=tkinter.DISABLED)
    print('停止')


# 创建并放置两个按钮分别触发两种情况
b1 = tkinter.Button(frame_t, text='开始', width=10, command=start_point, font=('Arial', 10))
b1.pack(side=tkinter.LEFT)
b2 = tkinter.Button(frame_t, text='停止', width=10, command=end_point, font=('Arial', 10))
b2.pack(side=tkinter.LEFT)

# 滚动条
sc = tkinter.Scrollbar(frame_b)
sc.pack(side=tkinter.RIGHT, fill=tkinter.Y)
# Listbox控件
listb = tkinter.Listbox(frame_b, yscrollcommand=sc.set, width=200, height=120)
# 将部件放置到主窗口中
listb.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
# 滚动条动，列表跟着动
sc.config(command=listb.yview)

# 主窗口循环显示
window.mainloop()
