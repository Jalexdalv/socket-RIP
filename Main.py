import SocketRIP.Tools
import SocketRIP.Gui
import tkinter

__author__ = '高一航'

# 日志根目录
LOG_PATH = 'C:\\Users\\Administrator\\PycharmProjects\\Jalexdalv\\SocketRIP\\LOG'

gui = tkinter.Tk()
# 窗口标题
gui.title('RIP协议模拟系统')
# 主窗口大小
gui.geometry('800x600')
# 禁止改变窗口大小
gui.resizable(width=False, height=False)

# 新建一个日志文件
log_file_path = SocketRIP.Tools.create_log(LOG_PATH)
# 窗口添加组件
app = SocketRIP.Gui.Gui(gui, log_file_path)
# 进入消息循环
gui.mainloop()
