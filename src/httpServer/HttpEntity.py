import time


class HttpRequestHead:
    """
    请求头
    """
    ACCEPT = "Accept"
    """ 可接受的相应内容类型 """
    ACCEPT_LANGUAGE = "Accept-Language"
    """ 可接受响应内容的语言列表 """
    ACCEPT_CHARSET = "Accept-Charset"
    """ 可接受的字符集 """
    ACCEPT_ENCODING = "Accept-Encoding"
    """ 可接受的响应内容的编码方式 """
    ACCEPT_DATETIME = "Accept-Datetime"
    """ 用于表示HTTP协议中需要认证资源的认证信息 """
    CACHE_CONTROL = "Cache-Control"
    """ 用来指定当前的请求、回复中是否使用缓存机制 """
    CONNECTION = "Connection"
    """ keep-alive/Upgrade客户端（浏览器有限使用的连接类型） """
    COOKIE = "Cookie"
    """ 用于服务器与客户端间的通讯 """
    CONTENT_LENGTH = "Content-Length"
    """ 请求体的长度 """
    CONTENT_TYPE = "Content-Type"
    """ 请求体的MIME类型 """
    DATE = "Date"
    """ 发送该消息的日期和时间 """
    EXPECT = "Expect"
    """ 表示客户端服务器做出特定的行为 """
    REFERER = "Referer"
    """ 表示浏览器所访问的前一个页面 """
    USER_AGENT = "User-Agent"
    """ 浏览器的身份标识字符串 """


class HttpResponseHead:
    """
    响应头
    """

    ACCESS_CONTROL_ALLOW_ORIGIN = "Access-Control-Allow-Origin"
    """ 跨域共享 """
    ACCEPT_RANGES = "Accept-Ranges"
    """ 服务器所支持的内容范围 """
    AGE = "Age"
    """ 响应对象在代理缓存中存在的时间，以秒为单位 """
    CACHE_CONTROL = "Cache-Control"
    """ 通知从服务器到客户端内的所有缓存机制 """
    CONNECTION = "Connection"
    """ 针对该连接所预期的选项 """
    CONTENT_DISPOSITION = "Content-Disposition"
    """ 对已知MIME类型资源的描述 """
    CONTENT_ENCODING = "Content-Encoding"
    """ 响应资源所使用的编码类型 """
    CONTENT_LANGUAGE = "Content-Language"
    """ 响就内容所使用的语言 """
    CONTENT_LENGTH = "Content-Length"
    """ 响应消息体的长度 """
    CONTENT_LOCATION = "Content-Location"
    """ 所返回的数据的一个候选位置 """
    CONTENT_RANGE = "Content-Range"
    """ 如果是响应部分消息 """
    CONTENT_TYPE = "Content-Type"
    """ 当前内容的MIME类型 """
    DATE = "Date"
    """ 此条消息被发送时的日期和时间 """
    EXPIRES = "Expires"
    """ 指定一个日期/时间 """
    SET_COOKIE = "Set-Cookie"
    """ 设置HTTP cookie """
    SERVER = "Server"
    """ 服务器的名称 """


class TimeMap:
    def __init__(self, timeout=30):
        """
        带时间的key,value结构
        :param timeout:超时时间
        """
        self.__data = {}
        self.__timeout = timeout

    def get(self, key):
        """
        获取值
        :param key:键
        :return: 值
        """
        value = self.__data.get(key)
        if value is None:
            return None
        if time.time() > value[0] + self.__timeout:
            self.delete(key)
            return None
        return value[1]

    def put(self, key, value):
        """
        存放值
        :param key:键
        :param value: 值
        """
        self.__data[key] = (time.time(), value)

    def delete(self, key):
        """
        删除键
        :param key:键
        """
        del self.__data[key]

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __iter__(self):
        for key in list(self.__data.keys()):
            value = self.__data[key]
            if time.time() < value[0] + self.__timeout:
                yield key, value[1]
            else:
                self.delete(key)


class Multipart:
    def __init__(self):
        self.name = None
        """ 上传的字段名称 """
        self.file_name = None
        """ 上传的文件名称 """
        self.data = None
        """ 数据 """
        self.type = None
        """ 类型 """
