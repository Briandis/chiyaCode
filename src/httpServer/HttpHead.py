class HttpRequestHead:
    # 可接受的相应内容类型
    ACCEPT = "Accept"
    # 可接受响应内容的语言列表
    ACCEPT_LANGUAGE = "Accept-Language"
    # 可接受的字符集
    ACCEPT_CHARSET = "Accept-Charset"
    # 可接受的响应内容的编码方式
    ACCEPT_ENCODING = "Accept-Encoding"
    # 用于表示HTTP协议中需要认证资源的认证信息
    ACCEPT_DATETIME = "Accept-Datetime"
    # 用来指定当前的请求、回复中是否使用缓存机制
    CACHE_CONTROL = "Cache-Control"
    # keep-alive/Upgrade客户端（浏览器有限使用的连接类型）
    CONNECTION = "Connection"
    # 用于服务器与客户端间的通讯
    COOKIE = "Cookie"
    # 请求体的长度
    CONTENT_LENGTH = "Content-Length"
    # 请求体的MIME类型
    CONTENT_TYPE = "Content-type"
    # 发送该消息的日期和时间
    DATE = "Date"
    # 表示客户端服务器做出特定的行为
    EXPECT = "Expect"
    # 表示浏览器所访问的前一个页面
    REFERER = "Referer"
    # 浏览器的身份标识字符串
    USER_AGENT = "User-Agent"


class HttpResponseHead:
    # 跨域共享
    ACCESS_CONTROL_ALLOW_ORIGIN = "Access-Control-Allow-Origin"
    # 服务器所支持的内容范围
    ACCEPT_RANGES = "Accept-Ranges"
    # 响应对象在代理缓存中存在的时间，以秒为单位
    AGE = "Age"
    # 通知从服务器到客户端内的所有缓存机制
    CACHE_CONTROL = "Cache-Control"
    # 针对该连接所预期的选项
    CONNECTION = "Connection"
    # 对已知MIME类型资源的描述
    CONTENT_DISPOSITION = "Content-Disposition"
    # 响应资源所使用的编码类型
    CONTENT_ENCODING = "Content-Encoding"
    # 响就内容所使用的语言
    CONTENT_LANGUAGE = "Content-Language"
    # 响应消息体的长度
    CONTENT_LENGTH = "Content-Length"
    # 所返回的数据的一个候选位置
    CONTENT_LOCATION = "Content-Location"
    # 如果是响应部分消息
    CONTENT_RANGE = "Content-Range"
    # 当前内容的MIME类型
    CONTENT_TYPE = "Content-Type"
    # 此条消息被发送时的日期和时间
    DATE = "Date"
    # 指定一个日期/时间
    EXPIRES = "Expires"
    # 设置HTTP cookie
    SET_COOKIE = "Set-Cookie"
    # 服务器的名称
    SERVER = "Server"
