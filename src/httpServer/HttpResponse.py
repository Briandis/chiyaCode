from src.httpServer.HttpEntity import HttpResponseHead, TimeMap


class ResponseLine:
    def __init__(self):
        """
        相应行
        """
        self.version = "HTTP/1.1"
        self.code = "200"
        self.msg = "OK"

    def create(self):
        """
        构建
        :return: 请求行
        """
        return f'{self.version} {self.code} {self.msg}'


class ResponseHead:

    def __init__(self, cookie: TimeMap = TimeMap()):
        """
        响应头信息
        """
        self.param = {}
        self.cookie: TimeMap = cookie

    def set_param(self, key, value):
        """
        设置响应头参数
        :param key:键
        :param value:值
        """
        self.param[key] = value

    def set_body_length(self, length):
        """
        设置响应体长度
        :param length:长度
        """
        self.set_param(HttpResponseHead.CONTENT_LENGTH, length)

    def create(self):
        """
        构建
        :return:请求头
        """
        head = ""
        for head_name, value in self.param.items():
            head += f'\r\n{head_name}:{value}'
        for cookie in self.cookie:
            head += f'\r\nSet-Cookie:{cookie}'
        head += '\r\n\r\n'
        return head

    def set_access_control_allow_origin(self):
        self.param["Access-Control-Allow-Methods"] = "*"
        self.param["Access-Control-Allow-Origin"] = "*"
        self.param["Access-Control-Allow-Headers"] = "*"


class ResponseBody:

    def __init__(self):
        """
        响应体
        """
        self.string_body = []

    def write(self, data):
        """
        写入数据
        :param data:数据
        """
        self.string_body.append(data)

    def create(self) -> bytes:
        """
        构建响应体
        :return:响应体的二进制
        """
        all_body = "".encode()
        for body in self.string_body:
            if body is None:
                continue
            if isinstance(body, bytes):
                all_body += body
            elif isinstance(body, str):
                all_body += body.encode()
            else:
                all_body += f'{body}'.encode()
        return all_body


class HttpResponse:

    def __init__(self, file_root):
        """
        响应报文封装
        :param file_root: 服务器目录
        """
        self.cookie = TimeMap()
        self.line = ResponseLine()
        self.head = ResponseHead(self.cookie)
        self.body = ResponseBody()
        self._root = file_root

    def write(self, data):
        """
        写入数据
        :param data:数据
        """
        self.body.write(data)

    def set_cookie(self, name, value):
        """
        设置cookie
        :param name:名称
        :param value: 值
        """
        self.cookie.put(name, value)

    def open_file(self, file_path):
        """
        读取服务器路径下的某个文件
        :param file_path: 服务器路径
        """
        try:
            with open(self._root + file_path, "rb") as f:
                self.body.write(f.read())
        except FileNotFoundError:
            self.line.code = 404
            self.line.msg = ""

    def create(self) -> bytes:
        """
        构建响应报文
        :return: 二进制数据
        """
        response_body = self.body.create()
        self.head.set_body_length(len(response_body))

        response_head = self.line.create() + self.head.create()
        return response_head.encode() + response_body
