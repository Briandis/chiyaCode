class Cookie:
    def __init__(self, name, value, time_out=None):
        """
        创建要设置的Cookie
        :param name: cookie的名称
        :param value: cookie的值
        :param time_out: 默认失效时间
        """
        self.name = name
        self.value = value
        self.timeOut = time_out
