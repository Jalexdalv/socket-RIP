import socketserver
import json

__author__ = '高一航'


class Server(socketserver.BaseRequestHandler):
    def handle(self):
        io_data = self.request[0]
        io_list = json.loads(io_data.decode())
        # 把接收数据写入文件
        f = open(io_list[0], 'w+')
        f.write(io_list[1])
        f.close()




