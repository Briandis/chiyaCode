import socket
import re
import uuid
import traceback
from concurrent.futures import ThreadPoolExecutor

from src.httpServer.ContentType import ContentType
from src.httpServer.HttpRequest import HttpRequest
from src.httpServer.HttpResponse import HttpResponse


class Server:

    def __init__(self, path, listen_size=10, address=("", 11451)):
        """
        初始化服务器
        :param path: 服务器物理路径
        :param listen_size: 服务器最大并发数
        :param address: 服务器的地址
        """
        # 创建socket
        self.socket = socket.socket()
        # 绑定地址
        self.socket.bind(address)
        # 设置监听数
        self.socket.listen(listen_size)
        # 加载响应类型
        self.content_type = ContentType.data
        # 配置服务器路径
        self.path = path
        # 全局Session容器
        self.all_session = {}
        # 全局业务容器
        self.servlet = {}
        # 全局路由
        self.index = {}
        # 创建线程池
        self.threadPool = ThreadPoolExecutor(listen_size)
        self.flag = True

    def start(self):
        """
        启动服务器
        """
        print("服务器已启动")
        while self.flag:
            client, address = self.socket.accept()
            self.threadPool.submit(self.run, client, address)

    def run(self, client: socket.socket, address):
        # 一次性拿4M
        request_data = client.recv(1024 * 1024 * 4)
        # 无效访问过滤
        if len(request_data) < 10:
            resp = HttpResponse(self.path)
            resp.code = 404
            resp.write_body("404 ERROR")
            client.send(resp.encode())
            return
        # 创建解析的请求体对象
        request = HttpRequest(request_data)
        # session解析
        session_cookie = request.get_cookie("SESSION_ID")
        session_id = None
        # 从cookie中拿
        if session_cookie is not None:
            session_id = session_cookie.value
        # 如果session_id是存在的
        if session_id is not None:
            session_map = self.all_session.get(session_id)
            if session_map is None:
                session_id = None
            else:
                request.session = session_map
        # 创建响应体
        response = HttpResponse(self.path)
        uri = request.uri
        print(f"访问了地址：{uri}")
        # 优先检查业务中是否绑定了路径
        if uri in self.servlet:
            try:
                # 执行业务
                self.servlet[uri].servlet(request, response)
            except:
                response.code = 500
                response.write_body("code:500 server error")
                traceback.print_exc()
        # 检查是否绑定了路由
        elif uri in self.index:
            response.open_file(self.index[uri])
        else:
            # 去服务器目录找
            file_type = re.findall(".*(\..*)", uri)
            response_type = self.content_type.get(".*")
            if len(file_type) > 0:
                if file_type[0] in self.content_type:
                    response_type = self.content_type[file_type[0]]
            response.content_type = response_type
            response.open_file(uri)
        # 如使用了session就保存起来
        if len(response.session) > 0:
            if session_id is None:
                session_id = str(uuid.uuid4()).replace("-", "")
                self.all_session[session_id] = response.session
            else:
                self.all_session[session_id].update(response.session)
            response.set_cookie("SESSION_ID", session_id)
        client.send(response.encode())
        client.close()
