import json
import re
import socket
from typing import Dict
from urllib import parse

from src.httpServer.HttpEntity import HttpRequestHead, Multipart, TimeMap


class ParamUtil:
    @staticmethod
    def param_parsing(params_string: str, params: dict):
        """
        参数解析
        :param params_string: 待解析的参数字符串，
        :param params: 解析出的参数
        """
        for param_key_map in params_string.split("&"):
            param = param_key_map.split("=")
            if len(param) == 2:
                params[param[0]] = param[1]


class RequestLine:

    def __init__(self):
        """
        请求行
        """
        self.method = None
        """ 请求方式 """
        self.url = None
        """ 请求地址 """
        self.version = None
        """ 协议版本 """

    def parsing(self, line: str, params: dict):
        """
        解析请求行数据并装配
        :param line: 请求字符串
        :param params: 解析出的参数
        """
        if params is None:
            params = {}
        lines = line.split(" ")
        # 获取URI中的参数
        temp_string = lines[1].split("?")
        # 解析URI中的参数
        if len(temp_string) > 1:
            ParamUtil.param_parsing(temp_string[1], params)
        self.method = lines[0]
        self.url = temp_string[0]
        self.version = lines[2]


class RequestHead:

    def __init__(self):
        self.head = {}

    def parsing(self, list_string: list):
        """
        装配请求头参数
        :param list_string: 请求头的参数
        """
        for string in list_string:
            head_map_list = string.split(":")
            self.head[head_map_list[0]] = head_map_list[1].replace(" ", "")

    def get_head(self, name) -> str:
        """
        获取请求头参数
        :param name:请参数名称
        :return: str
        """
        return self.head.get(name)


class RequestUtil:
    @staticmethod
    def parsing_cookie(head: RequestHead, cookie_param: TimeMap):
        """
        cookie解析
        :param head: 请求头
        :param cookie_param:cookie
        """
        cookies = head.get_head(HttpRequestHead.COOKIE)
        if cookies is None:
            return
        cookies = cookies.split(";")
        for cookie in cookies:
            cookie_map = cookie.split("=")
            cookie_param[cookie_map[0]] = cookie_map[1]

    @staticmethod
    def parsing_utf_8(params: dict, cookie: TimeMap):
        """
        参数UTF8编码
        :param params:参数
        :param cookie: cookie
        """
        for key, value in params.items():
            params[key] = parse.unquote(value)
        for key, value in cookie:
            params[key] = parse.unquote(value)

    @staticmethod
    def parsing_multipart(body: bytes, head: RequestHead, params: dict, multipart_param: dict):
        """
        对多文件上传进行解析
        :param body: 原始请求体二进制数据
        :param head: 请求头
        :param params: 参数
        :param multipart_param: 上传的文件
        """
        # 对多文件拆解成块信息拆解
        split = f'\r\n--{head.get_head(HttpRequestHead.CONTENT_TYPE).split("=")[1]}\r\n'.encode()
        # 移除最后的结束标识符
        end = f'\r\n--{head.get_head(HttpRequestHead.CONTENT_TYPE).split("=")[1]}--\r\n'
        body = body[:len(body) - len(end)]
        # 按照文件唯一标识字符串切割
        body_list = body.split(split)
        for multipart_data in body_list:
            multipart = multipart_data.split("\r\n\r\n".encode(), 1)
            if len(multipart) > 1:
                multipart_object = Multipart()

                multipart_string = multipart[0].decode()
                # 名字处理
                names = re.findall('name="(.*?)"', multipart_string)
                # 上传的字段
                multipart_object.name = names[0]
                if len(names) > 1:
                    # 文件名
                    multipart_object.file_name = names[1]
                # 文件
                multipart_object.data = multipart[1]
                # 文件类型处理
                content_type = re.findall("Content-Type: (.*)", multipart_string)
                if len(content_type) > 0:
                    multipart_object.type = content_type[0]
                # 不是文件，就是一起提交的参数
                if multipart_object.file_name is None:
                    params[multipart_object.name] = multipart_object.data
                    continue
                if multipart_object.type is not None and "text" in multipart_object.type:
                    multipart_object.data = multipart_object.data.decode()
                multipart_param[multipart_object.name] = multipart_object

    @staticmethod
    def parsing(client: socket.socket):
        """
        解析
        :param client:连接
        :return:
        """
        request_data = client.recv(1024 * 1024 * 4)
        params: Dict[str, str] = {}
        cookie = TimeMap()
        multipart: Dict[str, Multipart] = {}
        line = RequestLine()
        head = RequestHead()

        pack = request_data.split("\r\n\r\n".encode(), 1)
        # 获取头信息并编码成字符串
        head_string = pack[0].decode().split("\r\n")
        # 请求体初始化
        body_data = "".encode()
        # 如果大于两个，说明已经包含请求体了
        if len(pack) > 1:
            body_data = pack[1]

        # 解析请求行
        line.parsing(head_string[0], params)

        # 解析请求头
        head.parsing(head_string[1:])

        # cookie处理
        RequestUtil.parsing_cookie(head, cookie)

        # 针对POST解析请求体
        content_type = head.get_head(HttpRequestHead.CONTENT_TYPE)
        if content_type is not None:
            # 普通表单处理
            if "application/x-www-form-urlencoded" in content_type:
                ParamUtil.param_parsing(body_data.decode(), params)
            # 文件上传处理
            if "multipart/form-data" in content_type:
                RequestUtil.parsing_multipart(body_data, head, params, multipart)
            # JSON处理
            if "application/json" in content_type:
                params.update(json.loads(body_data.decode()))

        # 编码处理
        RequestUtil.parsing_utf_8(params, cookie)
        return line, head, params, cookie, multipart


class HttpRequest:
    def __init__(self, client: socket.socket):
        """
        初始化操作
        :param client:连接
        """
        self.line, self.head, self.param, self.cookie, self.multipart = RequestUtil.parsing(client)
        self.session = {}
        self.session_flag = False

    def get_cookie(self, name) -> str:
        """
        获取存储的cookie
        :param name: 名称
        :return: 自身
        """
        return self.cookie.get(name)

    def get_session(self, key):
        """
        获取session中的数据
        :param key: 键
        """
        return self.session.get(key)

    def set_session(self, key, value):
        """
        存储session
        :param key:键
        :param value:值
        """
        self.session_flag = True
        self.session[key] = value

    def remove_session(self, key):
        """
        移除session
        :param key:键
        """
        del self.session[key]
