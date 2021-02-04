import _thread
import time
import tkinter.simpledialog
from tkinter import END, simpledialog, messagebox

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


def set_room():
    # 获取字符串（标题，提示，初始值）
    room_id = simpledialog.askstring(title='请输入房间号', prompt='请输入房间号：', initialvalue='21089733')
    if room_id is not None:
        # 创建获取弹幕线程
        try:
            _thread.start_new_thread(bilibili, (0.5, str(room_id),))
        except:
            print("Error: 启动失败！请检查房间号是否正确")


def author():
    # 弹出对话框
    messagebox.showinfo(title='关于', message='作者：阿壮Jonson\n日期：2021年2月4日\n微信公众号：科技猫')


# tkinter GUI
window = tkinter.Tk()
window.title('BiliBli弹幕查看工具')
window.geometry('500x700')

# 菜单栏
menubar = tkinter.Menu(window)
# Open放在菜单栏中，就是装入容器
menubar.add_cascade(label='设置房间号', command=set_room)
menubar.add_command(label='关于', command=author)
# 创建菜单栏完成后，配置让菜单栏menubar显示出来
window.config(menu=menubar)

# 滚动条
sc = tkinter.Scrollbar(window)
sc.pack(side=tkinter.RIGHT, fill=tkinter.Y)
# Listbox控件
listb = tkinter.Listbox(window, yscrollcommand=sc.set)
# 将部件放置到主窗口中
listb.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
# 滚动条动，列表跟着动
sc.config(command=listb.yview)

# 进入循环显示
window.mainloop()
