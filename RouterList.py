import os
from tkinter import messagebox

__author__ = '高一航'


class RouterList(object):
    # 路由表类
    def __init__(self, path):
        # 是否存在
        if os.path.exists(path):
            self.router_name = os.path.basename(path).split('.')[0]
            self.path = path
            f = open(path)
            io_data_s = f.readlines()
            f.close()
            self.router_list = [{'target': io_data.split('  ')[0], 'distance': io_data.split('  ')[1],
                                 'next': io_data.split('  ')[2].replace('\n', '')}
                                for io_data in io_data_s]
        else:
            # 不存在则创建
            f = open(path, 'w+')
            f.close()
            self.router_name = os.path.basename(path).split('.')[0]
            self.router_list = []
            self.path = path

    def get_router_name(self):
        # 获取路由器名
        return self.router_name

    def get_router_list_path(self):
        # 获取路由表路径
        return self.path

    def get_router_list_count(self):
        # 获得路由表中路由信息数量
        return len(self.router_list)

    def get_router_info(self):
        # 获取所有路由信息
        return self.router_list

    def add_router_info(self, data):
        # 添加路由信息
        if isinstance(data, dict):
            if self.router_list:
                if data['target'] in [router_data['target'] for router_data in self.router_list]:
                    messagebox.showinfo('警告', '此目的网络已经存在!')
                    return
                else:
                    self.router_list.append(data)
            else:
                self.router_list.append(data)

    def save_router_list(self):
        # 保存路由表
        new_router_list = [io_data['target'] + '  ' + io_data['distance'] + '  ' + io_data['next']
                           for io_data in self.router_list]
        f = open(self.path, 'w+')
        f.write('\n'.join(new_router_list))
        f.close()

    def is_near_router(self, other):
        # 判断两路由器是否相邻
        if isinstance(other, RouterList):
            for data in [router_info for router_info in self.router_list
                         if int(router_info['distance']) == 1]:
                if data in other.get_router_info():
                    return True
            return False

    def set_send_router_info(self):
        # 发送路由表前修改路由表信息
        for router_info in self.router_list:
            if int(router_info['distance']) > 15:
                pass
            else:
                router_info['distance'] = str(int(router_info['distance'])+1)
            router_info['next'] = self.router_name
        return self.router_list



