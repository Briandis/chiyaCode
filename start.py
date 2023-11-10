import _thread
import os
import webbrowser

from src.controller.API import *

from src.httpServer.Server import Server

if __name__ == '__main__':
    port = 14514
    print(f"默认端口{port}")
    ip = ""
    print("开始将本启动器下的html设为web文件夹~~~")
    path = os.path.join(os.getcwd(), "html")
    print(f"服务器静态资源路径:{path}")
    listen_size = 35
    run_flag = False
    server_obj = None
    while True:
        try:
            server_obj = Server(path, address=(ip, port), listen_size=listen_size)
            print(f"服务器地址：http://127.0.0.1:{port}")
            webbrowser.open(f'http://127.0.0.1:{port}')
            # 注册页面
            server_obj.index[""] = "/index.html"
            server_obj.index["/"] = "/index.html"
            server_obj.index["/index"] = "/index.html"
            server_obj.index["/index.html"] = "/index.html"

            # 注册servlet
            server_obj.servlet["/hello"] = HelloWorld()

            run_flag = True
            print("服务器启动成功")
            break
        except:
            string = input("端口被占用，输入数字更换端口，其他字符退出")
            if string.isnumeric():
                port = int(string)
            else:
                break
    if run_flag:
        _thread.start_new_thread(server_obj.start, ())
        while server_obj.flag:
            flag = input("输入exit关闭服务器")
            if flag == "exit":
                server_obj.flag = False
        print("服务器开始关闭")
