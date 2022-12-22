class Tag:
    """
    XML基础构成的TAG
    """

    def __init__(self, name):
        """
        初始化
        :param name:标签名称
        """
        self._name = name
        self._attribute = {}
        self._data = []
        self.indent = 0
        self.line_tag = False

    def add_attribute(self, name, value):
        """
        初始化
        :param name:标签属性名称
        :param value: 标签属性值
        :return  自身
        """
        self._attribute[name] = value
        return self

    def _create_start(self):
        """
        构建标签头部
        :return: 标签头部
        """
        data = "\t" * self.indent + f'<{self._name}'
        for k, v in self._attribute.items():
            data += f' {k}="{v}"'
        if self.line_tag:
            return data + '/>'

        if self._check_line():
            data += ">"
        else:
            data += ">\n"
        return data

    def _create_end(self):
        """
        构建标签结尾
        :return: 标签结尾
        """
        end = f'</{self._name}>'
        if self._check_line():
            return end
        return "\t" * self.indent + end

    def create(self):
        """
        构建单行双标签
        :return:
        """
        if self.line_tag:
            return self._create_start()
        return self._create_start() + self._create_data() + self._create_end()

    def _create_data(self):
        """
        构建数据体
        :return:数据体
        """
        data = ""
        if len(self._data) == 1:
            k, v = self._data[0]
            if k == "data":
                return v
        indent = "\t" * (self.indent + 1)
        for k, v in self._data:
            if k == "data":
                data += f'{indent}{v}\n'
            if k == "tag":
                v.indent += self.indent + 1
                data += f'{v.create()}\n'
        return data

    def _check_line(self):
        """
        检查是否能构成单行
        :return: true:能/false:不能
        """
        if len(self._data) == 0:
            return True
        if len(self._data) == 1:
            k, v = self._data[0]
            return k == "data"
        return False

    def add_blank_line(self):
        """
        添加空行
        :return:自身
        """
        self._data.append(("data", ""))
        return self

    def add_data(self, data):
        """
        添加一行数据
        :param data:一行数据
        :return 自身
        """
        self._data.append(("data", data))
        return self

    def add_tag(self, tags):
        """
        添加标签
        :param tags:标签
        :return: 自身
        """
        self._data.append(("tag", tags))
        return self
