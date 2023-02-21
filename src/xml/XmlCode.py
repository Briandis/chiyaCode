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
        """ 标签的名称 """
        self._attribute = {}
        """ 标签的属性 """
        self._data = []
        """ 数据内容 """
        self.indent = 0
        """ 缩进 """
        self.line_tag = False
        """ 单行标签 """
        self.is_note = False
        """ 是注释 """
        self._data_type = {"indent": 0, "tag": 0, "data": 0}
        """ 内容存储计数 """
        self.force_multiline = False
        """ 强制为多行 """

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
        # 是注释
        if self.is_note:
            return "\t" * self.indent + f'<!-- {self._create_data()} -->'
        # 是单行标签的情况
        if self.line_tag:
            return self._create_start()
        return self._create_start() + self._create_data() + self._create_end()

    def _create_data(self):
        """
        构建数据体
        :return:数据体
        """
        data = ""
        if len(self._data) == 1 and self.force_multiline is False:
            k, v = self._data[0]
            if k == "data":
                return v
        indent = "\t" * (self.indent + 1)
        for k, v in self._data:
            if k == "indent":
                self.indent += v
                indent = "\t" * (self.indent + 1)
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
        # 强制多行
        if self.force_multiline:
            return False
        # 存在内部缩进不可能单行
        if self._data_type["indent"] > 0:
            return False
        # 存在标签不可能单行
        if self._data_type["tag"] > 0:
            return False
        # 大于1行以上的数据不可能是单行
        if self._data_type["data"] > 1:
            return False
        return True

    def add_blank_line(self):
        """
        添加空行
        :return:自身
        """
        self._data.append(("data", ""))
        self._data_type["data"] += 1
        return self

    def add_data(self, data):
        """
        添加一行数据
        :param data:一行数据
        :return 自身
        """
        self._data.append(("data", data))
        self._data_type["data"] += 1
        return self

    def add_tag(self, tags):
        """
        添加标签
        :param tags:标签
        :return: 自身
        """
        self._data.append(("tag", tags))
        self._data_type["tag"] += 1
        return self

    def indent_increase(self):
        """
        缩进增加一
        :return: 自身
        """
        self._data.append(("indent", 1))
        self._data_type["indent"] += 1
        return self

    def indent_decrease(self):
        """
        缩进减少一
        :return: 自身
        """
        self._data.append(("indent", -1))
        self._data_type["indent"] += 1
        return self
