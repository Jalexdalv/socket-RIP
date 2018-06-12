import SocketRIP.Event
import SocketRIP.Router
import SocketRIP.Tools
import os
import tkinter
from tkinter import messagebox
from tkinter import ttk

__author__ = '高一航'


class Gui(object):

    def __init__(self, master, log):
        self.master = master
        self.log = log
        # 全界面
        self.maxFrame = tkinter.Frame()
        self.maxFrame.pack(fill=tkinter.BOTH, expand=1, padx=10, pady=15)
        # 左侧控制区域
        self.leftFrame = tkinter.LabelFrame(self.maxFrame, font=18, padx=5 ,pady=40)
        self.leftFrame.pack(side=tkinter.LEFT)
        # 路由创建区域
        tkinter.Label(self.leftFrame, text='创建路由', font=18).grid(row=0, column=0, sticky='W', pady=5)
        tkinter.Label(self.leftFrame, text='路由器名称：', font=16).grid(row=1, column=0, sticky='W', pady=5)
        tkinter.Label(self.leftFrame, text='路由器地址：', font=16).grid(row=2, column=0, sticky='W', pady=5)
        tkinter.Label(self.leftFrame, text='目的网络：', font=16).grid(row=3, column=0, sticky='W', pady=5)
        tkinter.Label(self.leftFrame, text='距离：', font=16).grid(row=4, column=0, sticky='W', pady=5)
        tkinter.Label(self.leftFrame, text='下一跳：', font=16).grid(row=5, column=0, sticky='W', pady=5)
        self.routerName = tkinter.Entry(self.leftFrame, justify=tkinter.CENTER)
        self.routerName.grid(row=1, column=1)
        self.routerIp = tkinter.Entry(self.leftFrame, justify=tkinter.CENTER)
        self.routerIp.grid(row=2, column=1)
        self.routerTarget = tkinter.Entry(self.leftFrame, justify=tkinter.CENTER)
        self.routerTarget.grid(row=3, column=1)
        # 距离选择下拉框
        self.comboboxData = tkinter.StringVar()
        self.routerDistance = ttk.Combobox(self.leftFrame, width=18, textvariable=self.comboboxData,
                                           state='readonly')
        self.routerDistance['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)  # 设置下拉列表的值
        self.routerDistance.grid(row=4, column=1)
        self.routerDistance.current(0)
        # 下一跳输入框
        self.EntryData = tkinter.StringVar()
        self.routerNext = tkinter.Entry(self.leftFrame, justify=tkinter.CENTER,
                                        textvariable=self.EntryData, state='readonly')
        self.EntryData.set('*')
        self.routerNext.grid(row=5, column=1)
        self.routerAdd = tkinter.Button(self.leftFrame, text='添加', font=18, padx=20, pady=5)
        self.routerAdd.grid(row=6, column=0, pady=5, columnspan=2)
        tkinter.Label(self.leftFrame, text='更新路由表', font=18).grid(row=7, column=0, sticky='W', pady=5)
        self.routerUpdate = tkinter.Button(self.leftFrame, text='发送', font=18, padx=20, pady=5)
        self.routerUpdate.grid(row=8, column=0, pady=5, columnspan=2)
        # 故障模拟区域
        tkinter.Label(self.leftFrame, text='模拟网络故障', font=18).grid(row=9, column=0, sticky='W', pady=5)
        tkinter.Label(self.leftFrame, text='故障网络名称：', font=16).grid(row=10, column=0, sticky='W', pady=5)
        self.routerFault = tkinter.Entry(self.leftFrame, justify=tkinter.CENTER)
        self.routerFault.grid(row=10, column=1)
        self.faultStart = tkinter.Button(self.leftFrame, text='故障', font=18, padx=20, pady=5)
        self.faultStart.grid(row=11, column=0, pady=5, columnspan=2)
        tkinter.Label(self.leftFrame, text='', font=18).grid(row=12, column=0, sticky='W', pady=5)
        tkinter.Label(self.leftFrame, text='', font=18).grid(row=13, column=0, sticky='W', pady=5)

        # 路由信息显示界面
        self.routeInfoFrame = tkinter.LabelFrame(self.maxFrame, font=18, padx=5, pady=15)
        self.routeInfoFrame.pack()
        tkinter.Label(self.routeInfoFrame, text='路由表信息', font=16).pack()
        self.routeShowArea = tkinter.Scrollbar(self.routeInfoFrame)
        self.routeShowArea.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.routeData = tkinter.Text(self.routeInfoFrame, width=60, height=18, font=16, state=tkinter.DISABLED,
                                      yscrollcommand=self.routeShowArea.set)
        self.routeData.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.routeShowArea.config(command=self.routeData.yview)

        # 日志信息显示界面
        self.logFrame = tkinter.LabelFrame(self.maxFrame, padx=5, pady=15)
        self.logFrame.pack()
        tkinter.Label(self.logFrame, text='日志信息', font=16).pack()
        self.logShowArea = tkinter.Scrollbar(self.logFrame)
        self.logShowArea.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.logData = tkinter.Text(self.logFrame, width=60, height=13, font=16, state=tkinter.DISABLED,
                                    yscrollcommand=self.logShowArea.set)
        self.logData.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.logShowArea.config(command=self.logData.yview)
        # 按钮功能绑定
        self.event_bound()

    def event_bound(self):
        # 添加路由按钮
        self.routerAdd.bind('<ButtonRelease-1>', self.add_button)
        # 更新路由表按钮
        self.routerUpdate.bind('<ButtonRelease-1>', self.update_button)
        # 设置故障按钮
        self.faultStart.bind('<ButtonRelease-1>', self.fault_button)
        # 距离下拉框
        self.routerDistance.bind("<<ComboboxSelected>>", self.set_router_next)
        # 退出时保存日志
        self.master.protocol('WM_DELETE_WINDOW', self.save_log_event)

    def set_router_next(self, event):
        # 距离下拉框选择1时，设置下一跳为*
        if self.routerDistance.get() == '1':
            self.EntryData = tkinter.StringVar()
            self.routerNext = tkinter.Entry(self.leftFrame, justify=tkinter.CENTER,
                                            textvariable=self.EntryData, state='readonly')
            self.EntryData.set('*')
            self.routerNext.grid(row=5, column=1)
        else:
            self.routerNext = tkinter.Entry(self.leftFrame, justify=tkinter.CENTER)
            self.routerNext.grid(row=5, column=1)

    def update_button(self, event):
        # 发送按钮功能绑定
        # 如果没有路由表
        if len(os.listdir(SocketRIP.Router.ROOT_ROUTER_PATH)) == 0:
            messagebox.showinfo('警告', '不存在路由表，无法发送!')
            return
        SocketRIP.Event.update_router(log_show=self.logData, router_show=self.routeData)

    def add_button(self, event):
        # 添加按钮功能绑定
        # 输入为空
        if (self.routerName.get().strip() == '') or \
           (self.routerTarget.get().strip() == '') or \
           (self.routerTarget.get().strip() == '') or \
           (self.routerNext.get().strip() == ''):
            return
        SocketRIP.Event.add_router(log_show=self.logData, router_show=self.routeData,
                                   name=self.routerName.get(), ip=self.routerIp.get(),
                                   target=self.routerTarget.get(), distance=self.routerDistance.get(),
                                   next=self.routerNext.get())

    def fault_button(self, event):
        # 故障按钮功能绑定
        # 如果没有路由表
        if len(os.listdir(SocketRIP.Router.ROOT_ROUTER_PATH)) == 0:
            messagebox.showinfo('警告', '不存在路由表，无法发送!')
            return
        # 判断网络是否存在
        sign = 0  # 标志位
        for router_list in SocketRIP.Tools.get_all_router_list(SocketRIP.Router.ROOT_ROUTER_PATH):
            if self.routerFault.get() in [router_info['target'] for router_info
                                          in router_list.get_router_info()]:
                sign = 1
                break
        if sign == 0:
            messagebox.showinfo('警告', '此网络不存在，无法进行故障测试!')
            return
        SocketRIP.Event.fault_test(log_show=self.logData, router_show=self.routeData,
                                   fault=self.routerFault.get())

    def save_log_event(self):
        # 保存日志
        SocketRIP.Tools.save_log(log_data=self.logData, log=self.log)
        # 关闭窗口
        self.master.destroy()
