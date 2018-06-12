import SocketRIP.Router
import os
import time
import copy
import tkinter

__author__ = '高一航'


def get_all_router(root_path):
    # 获取全部路由器,返回值为路由器列表
    return [SocketRIP.Router.Router(name=os.path.basename(router_list).split('.')[0],
                                    ip_address=router_dir.replace(' ', ':'))
            for router_dir in os.listdir(root_path)
            for router_list in os.listdir(root_path+'\\'+router_dir)]


def get_all_router_list(root_path):
    # 获取全部路由表,返回值为路由表列表
    return [router.get_router_list() for router in get_all_router(root_path)]


def get_all_near_router(root_path):
    # 相邻路由器
    all_near_router = {}
    # 获取所有路由表
    all_router = get_all_router(root_path)
    # 获取所有相邻路由器
    sign_index = 0  # 标志位
    for router in all_router:
        copy_all_router = copy.deepcopy(all_router)  # 全部路由表复制
        copy_all_router.pop(sign_index)
        near_list = []  # 存储每个路由器相邻路由器表的临时变量
        for copy_router in copy_all_router:
            if router.get_router_list().is_near_router(copy_router.get_router_list()):
                near_list.append(copy_router)
        all_near_router[router.get_router_name()] = near_list
        sign_index += 1
    return all_near_router


def get_now_time(sign):
    # 按格式获取当前时间
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    now_time1 = time.strftime('%Y-%m-%d %H %M %S', time.localtime(time.time()))
    if sign == 0:
        return '['+now_time+']'
    if sign == 1:
        return now_time1


def show_log(log_data, data):
    # 日志显示
    log_data.config(state=tkinter.NORMAL)
    log_data.insert(tkinter.END, data)
    log_data.see(tkinter.END)


def show_router_info(route_data, data):
    # 路由信息显示
    route_data.config(state=tkinter.NORMAL)
    route_data.insert(tkinter.END, data)
    route_data.see(tkinter.END)


def create_log(log_root_path):
    # 日志文件创建
    log_file_path = log_root_path+'\\'+get_now_time(1)+'.log'
    if os.path.exists(log_file_path):
        log_file_path = log_root_path+'\\'+get_now_time(1)+'COPY'+'.log'
    f = open(log_file_path, 'w+')
    f.close()
    return log_file_path


def save_log(**params):
    # 保存日志
    show_log_data = get_now_time(0) + '保存日志\n'
    show_log(params['log_data'], show_log_data)
    f = open(params['log'], 'w+')
    f.write(params['log_data'].get(1.0, tkinter.END))
    f.close()
