from src.httpServer.Cookie import Cookie
from src.httpServer.HttpHead import HttpResponseHead
from src.httpServer.Session import Session


class HttpResponse:

    def __init__(self, file_root):
        """
        响应报文封装
        :param file_root: 服务器目录
        """
        self.version = "HTTP/1.1"
        self.code = "200"
        self.msg = "OK"
        self.content_type = "text/html"
        self.header = None
        self.body = ""
        self.content_length = 0
        self.flag = "text"
        self.cookies = {}
        self.session = {}
        self.__root = file_root

    def __create_response_line(self) -> str:
        """
        生成响应行
        :return: str
        """
        return f"{self.version} {self.code} {self.msg} \r\n"

    def __create_response_head(self) -> str:
        """
        生成响应头
        :return: str
        """
        return f"{HttpResponseHead.CONTENT_LENGTH}:{len(self.body)}\r\n{HttpResponseHead.CONTENT_TYPE}:{self.content_type}\r\n"

    def __create_cookie(self):
        """
        生成cookie的响应信息
        :return: str
        """
        if len(self.cookies) == 0:
            return ""
        string = ""
        for i in self.cookies:
            string += f"Set-Cookie:{i}={self.cookies[i].value}\r\n"
        return string

    def write_body(self, string: str):
        """
        字符串的形式追加进响应体
        :param string: 追加的字符串
        """
        self.body = self.body + string

    def open_file(self, file_path):
        """
        读取服务器路径下的某个文件
        :param file_path: 服务器路径
        """
        try:
            with open(self.__root + file_path, "rb") as f:
                self.body = f.read()
        except FileNotFoundError:
            self.code = 404
            self.msg = ""

    def set_cookie(self, name, value):
        self.cookies[name] = Cookie(name, value)

    def set_sessions(self, name, value):
        self.session[name] = Session(name, value)

    def encode(self) -> bytes:
        """
        生成二进制流
        :return: bytes
        """
        head = self.__create_response_line() + self.__create_response_head() + self.__create_cookie()
        head = head.encode()
        if not isinstance(self.body, bytes):
            body = ("\r\n" + self.body).encode()
        else:
            body = "\r\n".encode() + self.body
        return head + body
