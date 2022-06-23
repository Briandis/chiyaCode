import json
import re
from urllib import parse

from src.httpServer.Cookie import Cookie
from src.httpServer.HttpHead import HttpRequestHead

from src.httpServer.Multipart import Multipart


class HttpRequest:
    def __init__(self, request_data: bytes):
        """
        初始化操作
        :param request_data:带解析的完整数据
        """
        self.__params = {}
        self.__head = {}
        self.method = ""
        self.version = ""
        self.uri = ""
        self.__multipart = {}
        self.__cookie = {}
        # 解析并装配请求信息
        self.__parsing(request_data)
        # cookie解析
        self.__cookie_parsing()
        # 解析所有参数为UTF8编码
        self.__parsing_utf_8()
        self.session = {}

    def __parsing(self, request_data: bytes):
        """
        解析请信息
        :param request_data:数据
        """
        # 10M的数据量
        # 根据请求体与请求体分隔符切割
        pack = request_data.split("\r\n\r\n".encode(), 1)
        # 获取头信息并编码成字符串
        head = pack[0].decode()
        # 请求体初始化
        body = ""
        # 如果大于两个，说明已经包含请求体了
        if len(pack) > 1:
            body = pack[1]
        # 请求头解析
        request_list_head = head.split("\r\n")
        # 解析请求行
        self.__line_decode(request_list_head[0])
        # 解析请求头
        self.__head_decode(request_list_head[1:])
        # 针对POST解析请求体
        content_type = self.get_head(HttpRequestHead.CONTENT_TYPE)
        if content_type is not None:
            # 普通表单处理
            if "application/x-www-form-urlencoded" in content_type:
                self.__param_parsing(body.decode())
            # 文件上传处理
            if "multipart/form-data" in content_type:
                self.__multipart_parsing(body)
            # JSON处理
            if "application/json" in content_type:
                self.__params.update(json.loads(body.encode()))

    def __line_decode(self, line: str):
        """
        解析请求行数据并装配
        :param line: 请求字符串
        """
        lines = line.split(" ")
        # 获取URI中的参数
        temp_string = lines[1].split("?")
        # 解析URI中的参数
        if len(temp_string) > 1:
            self.__param_parsing(temp_string[1])
        self.method = lines[0]
        self.uri = temp_string[0]
        self.version = lines[2]

    def __head_decode(self, list_string: list):
        """
        装配请求头参数
        :param list_string: 请求头的参数
        """
        for string in list_string:
            head_map_list = string.split(":")
            self.__head[head_map_list[0]] = head_map_list[1].replace(" ", "")

    def __multipart_parsing(self, body):
        """
        对多文件上传进行解析
        :param body: 原始请求体二进制数据
        """
        # 对多文件拆解成块信息拆解
        q = "\r\n--" + self.get_head(HttpRequestHead.CONTENT_TYPE).split("=")[1] + "\r\n"
        # 移除最后的结束标识符
        end = f'\r\n--{self.get_head(HttpRequestHead.CONTENT_TYPE).split("=")[1]}--\r\n'
        body = body[:len(body) - len(end)]
        body_list = body.split(q.encode())
        for i in body_list:
            multiparts = i.split("\r\n\r\n".encode(), 1)
            if len(multiparts) > 1:
                m = Multipart()
                multipart_string = multiparts[0].decode()
                names = re.findall('name="(.*?)"', multipart_string)

                m.name = names[0]
                if len(names) > 1:
                    m.file_name = names[1]
                m.data = multiparts[1]

                content_type = re.findall("Content-Type: (.*)", multipart_string)
                if len(content_type) > 0:
                    m.type = content_type[0]

                if m.type is None:
                    self.__params[m.name] = m.data.decode()
                    continue
                if "text" in m.type:
                    m.data = m.data.decode()
                self.__multipart[m.name] = m

    def __param_parsing(self, params: str):
        """
        参数解析
        :param params: 待解析的参数字符串，
        :return: Node
        """
        params = params.split("&")
        for param_key_map in params:
            param_list = param_key_map.split("=")
            if len(param_list) == 2:
                self.__params[param_list[0]] = param_list[1]

    def __cookie_parsing(self):
        """
        cookie解析
        """
        cookies = self.get_head(HttpRequestHead.COOKIE)
        if cookies is None:
            return
        cookies = cookies.split(";")
        for i in cookies:
            cookie_map = i.split("=")
            cookie = Cookie(cookie_map[0], cookie_map[1])
            self.__cookie[cookie.name] = cookie

    def __parsing_utf_8(self):
        for i in self.__params:
            self.__params[i] = parse.unquote(self.__params[i])
        for i in self.__cookie:
            self.__cookie[i].value = parse.unquote(self.__cookie[i].value)

    def show_view(self):
        return str(self.__dict__)

    def get_multipart(self, name) -> Multipart:
        """
        获取文件对象
        :param name: 获取的参数名称
        :return: Multipart对象
        """
        return self.__multipart.get(name)

    def get_cookie(self, name) -> Cookie:
        """
        获取Cookie参数
        :param name:cookie名称
        :return: cookie对象
        """

        return self.__cookie.get(name)

    def get_head(self, name) -> str:
        """
        获取请求头参数
        :param name:请参数名称
        :return: str
        """
        return self.__head.get(name)

    def get_param(self, name) -> str:
        """
        获取提交参数
        :param name: 参数名称
        :return: str
        """
        return self.__params.get(name)

    def show_head(self):
        for i in self.__head:
            print(f"{i}=>{self.__head[i]}")
        for i in self.__params:
            print(f"{i}=>{self.__params[i]}")
        for i in self.__cookie:
            print(f"{i}=>{self.__cookie[i]}")

    def get_session(self, name):
        if name in self.session:
            return self.session[name].get_value()
        else:
            return None

    def show_all_cookie(self):
        for i in self.__cookie:
            print(f"{i} -> {self.__cookie[i].value}")
