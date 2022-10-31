class KeyWord:
    """
    关键字
    """
    JAVA_KEYWORD = {
        "abstract": "abs", "assert": "assertion",
        "boolean": "bool", "break": "recoil", "byte": "bytes",
        "case": "cases", "catch": "catching", "char": "chars", "class": "classes", "const": "consts", "continue": "continued",
        "default": "defaults", "do": "make", "double": "doubles",
        "else": "elsewhere", "enum": "enums", "extends": "extend",
        "final": "finale", "finally": "finalize", "float": "floats", "for": "form",
        "if": "ifs", "implements": "implements", "import": "imports", "instanceof": "instance", "int": "integer",
        "interface": "interfaces",
        "long": "longs",
        "native": "natives", "new": "news",
        "package": "packages", "private": "privates", "protected": "protect", "public": "publicity",
        "return": "returns",
        "short": "shorts", "static": "statics", "strictfp": "strict", "super": "supers", "switch": "switches", "synchronized": "synchronize",
        "this": "these", "throw": "thrower", "throws": "throwers", "transient": "transients", "try": "trying",
        "void": "voids", "volatile": "volatiles",
        "while": "whiles",
        # 非关键字的保留字
        "cast": "castle",
        "false": "falsely",
        "future": "futures",
        "generic": "generics",
        "inner": "inside",
        "operator": "operators", "outer": "outers",
        "rest": "repose",
        "true": "real",
        "var": "vars",
        "goto": "jump",
        "null": "nil",
    }


class StringUtil:
    """
    字符串处理库
    """

    @staticmethod
    def keyword_convert(string: str, reference: dict = KeyWord.JAVA_KEYWORD):
        """
        根据字典转换对应关键字
        :param string:
        :param reference:
        :return:
        """
        if string in reference:
            return reference[string]
        return string

    @staticmethod
    def replace_keyword(string: str, source: str, target: str = "", reference: dict = KeyWord.JAVA_KEYWORD):
        """
        替换字符，并将间隔的字符串过滤关键字
        :param string:
        :param source:
        :param target:
        :param reference:
        :return:
        """
        if StringUtil.is_null(string):
            return ""
        lists = string.split(source)
        values = StringUtil.keyword_convert(lists[0], reference)
        for i in range(1, len(lists)):
            values += target + StringUtil.keyword_convert(lists[i], reference)
        return values

    @staticmethod
    def is_null(string: str) -> bool:
        """
        判断字符串是否为null或者空
        :param string: 待检测字符串
        :return: true:是空/false:不为空
        """
        return string is None or len(string) == 0

    @staticmethod
    def is_not_null(string: str) -> bool:
        """
        判断字符串是否不为null或者空
        :param string: 待检测字符串
        :return: true:不为空/false:为空
        """
        return string is not None and len(string) > 0

    @staticmethod
    def first_char_lower_case(string: str) -> str:
        """
        首字母转小写
        :param string: 待转换字符串
        :return: 转换后的字符串
        """
        if StringUtil.is_null(string):
            return ""
        if len(string) == 1:
            return string.lower()
        return string[0].lower() + string[1:]

    @staticmethod
    def first_char_upper_case(string: str) -> str:
        """
        首字母大写
        :param string: 待转换字符串
        :return: 转换后的字符串
        """
        if StringUtil.is_null(string):
            return ""
        if len(string) == 1:
            return string.upper()
        return string[0].upper() + string[1:]

    @staticmethod
    def underscore_to_small_hump(string: str) -> str:
        """
        下划线转小驼峰
        :param string:待转换字符串
        :return:  转换后的字符串
        """
        if StringUtil.is_null(string):
            return ""
        # 移除首尾下划线
        string = string.strip("_")
        underscore_list = string.split("_")
        new_str = StringUtil.first_char_lower_case(underscore_list[0])
        for i in range(1, len(underscore_list)):
            new_str += StringUtil.first_char_upper_case(underscore_list[i])
        return new_str

    @staticmethod
    def underscore_to_big_hump(string: str) -> str:
        """
        下划线转大驼峰
        :param string:待转换字符串
        :return:  转换后的字符串
        """
        if StringUtil.is_null(string):
            return ""
        string = string.strip("_")
        new_str = ""
        for i in string.split("_"):
            new_str += StringUtil.first_char_upper_case(i)
        return new_str

    @staticmethod
    def hump_to_underscore(string: str) -> str:
        """
        驼峰转下划线
        :param string:待转换字符串
        :return:  转换后的字符串
        """
        if StringUtil.is_null(string):
            return ""
        new_str = ""
        first = False
        for char in string:
            # 首字母大写前不加下划线，之后才加
            if char.isupper() and first:
                new_str += "_"
            new_str += char.lower()
            first = True
        return new_str

    @staticmethod
    def remove_prefix(string: str, prefix: str, not_case=False) -> str:
        """
        移除字符串前缀
        :param string: 原字符串
        :param prefix: 要移除的前缀
        :param not_case: 是否区分大小写
        :return: 移除后的字符串
        """
        if not_case:
            if prefix == string[:len(prefix)]:
                string = string[len(prefix):]
        else:
            if prefix.lower() == string[:len(prefix)].lower():
                string = string[len(prefix):]
        return string

    @staticmethod
    def remove_suffix(string: str, suffix: str, not_case=False) -> str:
        """
        移除字符串后缀
        :param string: 原字符串
        :param suffix: 要移除的后缀
        :param not_case: 是否区分大小写
        :return: 移除后的字符串
        """
        if not_case:
            if suffix == string[len(suffix):]:
                string = string[:len(suffix)]
        else:
            if suffix.lower() == string[len(suffix):].lower():
                string = string[:len(suffix)]
        return string

    @staticmethod
    def is_string_tail(string: str, suffix, not_case=False) -> bool:
        """
        判断是否是后缀
        :param string:原字符串
        :param suffix:后缀字符串
        :param not_case: 是否区分大小写
        :return: true:是/false:不是
        """
        s_len, p_len = len(string), len(suffix)
        if s_len == 0 or p_len == 0 or p_len > s_len:
            return False
        if not_case:
            return suffix == string[s_len - p_len:]
        else:
            return suffix.lower() == string.lower()[s_len - p_len:]

    @staticmethod
    def eq(a: str, b: str, not_case=False):
        """
        比较两字符串是否相等
        :param a: 字符串
        :param b: 字符串
        :param not_case: 是否区分大小写
        :return: 相等、不相等
        """
        if not_case:
            return a == b
        else:
            return a.lower() == b.lower()

    @staticmethod
    def string_join(joiner, *args):
        """
        对字符串进行拼接
        :param joiner: 拼接符
        :param args: 多个参数
        :return: 字符串返回值
        """
        if args is None or len(args) == 0:
            return None
        string = args[0]
        for i in range(1, len(args)):
            if StringUtil.is_not_null(args[i]):
                string += joiner + args[i]
        return string


class CollectionUtil:
    """
    集合工具库
    """

    @staticmethod
    def dict_set(data: dict, key: str, value: str):
        """
        生成key set(value)的集合，
        :param data: 字段对象
        :param key: key
        :param value: 值
        :return: data本身
        """
        if key not in data:
            data[key] = set()
        data[key].add(value)
        return data

    @staticmethod
    def dict_list(data: dict, key: str, value: str):
        """
        生成key list(value)的集合，
        :param data: 字段对象
        :param key: key
        :param value: 值
        :return: data本身
        """
        if key not in data:
            data[key] = []
        data[key].append(value)
        return data
