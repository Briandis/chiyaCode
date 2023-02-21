import json
import os


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
    def keyword_convert(string: str, reference=None):
        """
        根据字典转换对应关键字
        :param string:
        :param reference:
        :return:
        """
        if reference is None:
            reference = KeyWord.JAVA_KEYWORD
        if string in reference:
            return reference[string]
        return string

    @staticmethod
    def replace_keyword(string: str, source: str, target: str = "", reference=None):
        """
        替换字符，并将间隔的字符串过滤关键字
        :param string:
        :param source:
        :param target:
        :param reference:
        :return:
        """
        if reference is None:
            reference = KeyWord.JAVA_KEYWORD
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
            return ""
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


class JsonUtil:
    """
    JSON工具库
    """

    @staticmethod
    def get_base_type(obj: object) -> int:
        """
        获取基础数据类型
        :param obj: 对象
        :return: 0:null,1:boolean,2:int,3:float,4:string,-1:other
        """
        if obj is None:
            return 0
        obj_type = type(obj)
        if obj_type == bool:
            return 1
        if obj_type == int:
            return 2
        if obj_type == float:
            return 3
        if obj_type == str:
            return 4
        return -1

    @staticmethod
    def new_dict(obj: dict) -> dict:
        """
        根据字典，生成新的字典，会自动迭代
        :param obj: 字典对象
        :return: 新的字典
        """
        object_dict = {}
        for key, value in obj.items():
            if JsonUtil.get_base_type(value) > -1:
                object_dict[key] = value
            else:
                object_dict[key] = JsonUtil.convert_object(value)
        return object_dict

    @staticmethod
    def convert_object(obj):
        """
        迭代对象解析成json
        :param obj: 对象
        :return: 可识别的字典或列表
        """
        if obj is None:
            return None
        # 如果是基础类型，则直接返回
        if JsonUtil.get_base_type(obj) > -1:
            return obj
        # 如果是列表，则迭代
        if type(obj) == list:
            object_list = []
            for item in obj:
                object_list.append(JsonUtil.convert_object(item))
            return object_list
        # 如果是字典，则直接迭代
        if type(obj) == dict:
            return JsonUtil.new_dict(obj)
        else:
            return JsonUtil.new_dict(obj.__dict__)

    @staticmethod
    def to_json(obj):
        """
        将对象转换成JSON
        :param obj: 对象
        :return: JSON字符串
        """
        return json.dumps(JsonUtil.convert_object(obj), indent=2, ensure_ascii=False)


class TypeConstant:
    """
    类型常量
    """
    STRING = "String"
    INTEGER = "Integer"
    LONG = "Long"
    DATE = "Date"
    FLOAT = "Float"
    DOUBLE = "Double"
    BOOLEAN = "Boolean"
    CHARACTER = "Character"
    DECIMAL = "BigDecimal"


class PackTypeDict:
    """
    包装类
    """
    PACK_DICT = {
        "int": TypeConstant.INTEGER,
        "long": TypeConstant.LONG,
        "char": TypeConstant.CHARACTER,
        "time": TypeConstant.DATE,
        "float": TypeConstant.FLOAT,
        "double": TypeConstant.DOUBLE,
        "boolean": TypeConstant.BOOLEAN,
    }

    @staticmethod
    def get_java_pack_object(type_name: str) -> str:
        """
        获取Java基础数据类型的包装类
        :param type_name:基础类型包装类
        :return: 类型的字符串
        """
        type_name = type_name.lower()
        if type_name in PackTypeDict.PACK_DICT:
            return PackTypeDict.PACK_DICT.get(type_name)
        return TypeConstant.STRING


class SQLTypeDict:
    """
    SQL数据类型对应的JAVA数据类型
    """
    """
    包装类对应的类型
    """
    PACK_DICT = {
        "int": TypeConstant.INTEGER,
        "long": TypeConstant.LONG,
        "char": TypeConstant.CHARACTER,
        "time": TypeConstant.DATE,
        "float": TypeConstant.FLOAT,
        "double": TypeConstant.DOUBLE,
        "boolean": TypeConstant.BOOLEAN,
    }

    """
    SQL类型对应JAVA类型的字典
    """
    SQL_DICT = {
        # 整数类
        "tinyint": TypeConstant.INTEGER,
        "smallint": TypeConstant.INTEGER,
        "mediumint": TypeConstant.INTEGER,
        "int": TypeConstant.INTEGER,
        "integer": TypeConstant.INTEGER,
        "long": TypeConstant.LONG,
        "bigint": TypeConstant.LONG,
        # 小数类
        "float": TypeConstant.FLOAT,
        "double": TypeConstant.DOUBLE,
        "decimal": TypeConstant.DECIMAL,
        # 时间类
        "time": TypeConstant.DATE,
        "date": TypeConstant.DATE,
        "datetime": TypeConstant.DATE,
        "year": TypeConstant.DATE,
        "timestamp": TypeConstant.DATE,
        # 字符串类
        "char": TypeConstant.STRING,
        "varchar": TypeConstant.STRING,
        "tinyblob": TypeConstant.STRING,
        "tinytext": TypeConstant.STRING,
        "blob": TypeConstant.STRING,
        "text": TypeConstant.STRING,
        "mediumblob": TypeConstant.STRING,
        "mediumtext": TypeConstant.STRING,
        "longblob": TypeConstant.STRING,
        "longtext": TypeConstant.STRING,
        # postgres类型
        "int2": TypeConstant.INTEGER,
        "int4": TypeConstant.INTEGER,
        "int8": TypeConstant.LONG,
        "timestamptz": TypeConstant.DATE,
        "timestampt": TypeConstant.DATE,
        "numeric": TypeConstant.DOUBLE
    }

    @staticmethod
    def get(type_name: str) -> str:
        """
        根据数据类型，获取JAVA数据类型
        :param type_name: SQL数据类型
        :return: JAVA数据类型
        """
        type_name = type_name.lower()
        if type_name in SQLTypeDict.SQL_DICT:
            return SQLTypeDict.SQL_DICT[type_name]
        return TypeConstant.STRING


class OSUtil:

    @staticmethod
    def is_not_dir_create(path: str, now_dir: str):
        """
        如果没有文件夹，则创建
        :param path: 文件路径
        :param now_dir: 当前的文件夹
        :return: 当前构建的路径
        """
        path = os.path.join(path, now_dir)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    @staticmethod
    def create_dir(packet_name: str) -> str:
        """
        创建文件夹
        :param packet_name:java的模块路径
        :return:
        """
        lists = packet_name.split(".")
        path = os.getcwd()

        path = OSUtil.is_not_dir_create(path, "data")
        path = OSUtil.is_not_dir_create(path, "src")
        for i in lists:
            path = os.path.join(path, i)
            if not os.path.exists(path):
                os.mkdir(path)
        return path

    @staticmethod
    def save_file(path, file_name, suffix, data):
        """
        保存文件
        :param path: 文件路径，java包名的
        :param file_name: 文件名
        :param suffix: 文件后缀
        :param data: 存储的字符数据
        :return:
        """
        path = OSUtil.create_dir(path)
        if "." not in suffix:
            suffix = "." + suffix
        with open(os.path.join(path, file_name + suffix), "w", encoding="utf-8") as file:
            file.write(data)

    @staticmethod
    def save_file_java(package, class_name, data):
        """
        构建java文件
        :param package:所在包路径
        :param class_name: 类名
        :param data: 文件内容
        """
        OSUtil.save_file(package, class_name, "java", data)


class ObjectUtil:
    """
    对象工具库
    """

    @staticmethod
    def object_set_attr(obj: object, attr_dict: dict):
        """
        根据对象中的属性，获取字典中的值
        :param obj: 任意对象
        :param attr_dict: 需要装配的字典
        """
        for i in obj.__dict__:
            obj.__setattr__(i, attr_dict.get(i))
