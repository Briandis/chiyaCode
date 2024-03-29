import re


def is_null(string: str) -> bool:
    """
    判断字符串是否为null或者空
    :param string: 待检测字符串
    :return: true:是空/false:不为空
    """
    return string is None or len(string) == 0


def is_not_null(string: str) -> bool:
    """
    判断字符串是否不为null或者空
    :param string: 待检测字符串
    :return: true:不为空/false:为空
    """
    return string is not None and len(string) > 0


def first_char_lower_case(string: str) -> str:
    """
    首字母转小写
    :param string: 待转换字符串
    :return: 转换后的字符串
    """
    if is_null(string):
        return ""
    if len(string) == 1:
        return string.lower()
    return string[0].lower() + string[1:]


def first_char_upper_case(string: str) -> str:
    """
    首字母大写
    :param string: 待转换字符串
    :return: 转换后的字符串
    """
    if is_null(string):
        return ""
    if len(string) == 1:
        return string.upper()
    return string[0].upper() + string[1:]


def underscore_to_small_hump(string: str) -> str:
    """
    下划线转小驼峰
    :param string:待转换字符串
    :return:  转换后的字符串
    """
    if is_null(string):
        return ""
    # 移除首尾下划线
    string = string.strip("_")
    underscore_list = string.split("_")
    new_str = first_char_lower_case(underscore_list[0])
    for i in range(1, len(underscore_list)):
        new_str += first_char_upper_case(underscore_list[i])
    return new_str


def underscore_to_big_hump(string: str) -> str:
    """
    下划线转大驼峰
    :param string:待转换字符串
    :return:  转换后的字符串
    """
    if is_null(string):
        return ""
    string = string.strip("_")
    new_str = ""
    for i in string.split("_"):
        new_str += first_char_upper_case(i)
    return new_str


def hump_to_underscore(string: str) -> str:
    """
    驼峰转下划线
    :param name:
    :return:
    """
    if is_null(string):
        return ""
    new_str = ""

    first = False
    for i in string:
        if re.match("[A-Z]", i) and first:
            new_str += "_"
        new_str += i.lower()
        first = True
    return new_str


def remove_prefix(string: str, prefix: str) -> str:
    """
    移除字符串前缀
    :param string: 原字符串
    :param prefix: 要移除的前缀
    :return: 移除后的字符串
    """
    if prefix == string[:len(prefix)]:
        string = string[len(prefix):]
    return string


def remove_suffix(string: str, prefix: str) -> str:
    """
    移除字符串后缀
    :param string: 原字符串
    :param prefix: 要移除的后缀
    :return: 移除后的字符串
    """
    if prefix == string[len(prefix):]:
        string = string[:len(prefix)]
    return string


def remove_prefix_not_case(string: str, suffix: str) -> str:
    """
    移除字符串前缀，不区分大小写
    :param string: 原字符串
    :param suffix: 要移除的前缀
    :return: 移除后的字符串
    """
    if suffix.lower() == string[:len(suffix)].lower():
        string = string[len(suffix):]
    return string


def remove_suffix_not_case(string: str, suffix: str) -> str:
    """
    移除字符串后缀，不区分大小写
    :param string: 原字符串
    :param suffix: 要移除的后缀
    :return: 移除后的字符串
    """
    if suffix.lower() == string[len(suffix):].lower():
        string = string[:len(suffix)]
    return string


def is_string_tail(string: str, suffix) -> bool:
    """
    判断是否是后缀
    :param string:原字符串
    :param suffix:后缀字符串
    :return: true:是/false:不是
    """
    s_len, p_len = len(string), len(suffix)
    if s_len == 0 or p_len == 0 or p_len > s_len:
        return False
    return suffix == string[s_len - p_len:]


def is_string_tail_not_case(string: str, suffix) -> bool:
    """
    判断是否是后缀，不区分大小写
    :param string:原字符串
    :param suffix:后缀字符串
    :return: true:是/false:不是
    """
    string, prefix = string.lower(), suffix.lower()
    return is_string_tail(string, prefix)


def create_annotation(msg=None, res=None, *args):
    """
    创建注解方法
    :param msg: 注解内容
    :param res: 返回值说明
    :param args: 参数说明
    :return: 注解字符串
    """
    data = ""
    data += "\t/**\n"
    # 内容行
    if msg is not None:
        data += f'\t * {msg}\n'
    # 如果返回值和参数都有，换行
    if (args is not None and len(args) > 0) or res is not None:
        data += f'\t * \n'
    # 参数
    for i in args:
        if i is not None and len(i) > 0:
            data += f'\t * @param {i}\n'
    # 返回值
    if res is not None:
        data += f'\t * @return {res}\n'
    data += "\t */\n"
    return data


def eq(a: str, b: str):
    """
    比较两字符串是否相等
    :param a: 字符串
    :param b: 字符串
    :return: 相等、不相等
    """
    return a == b


def eq_not_case(a: str, b: str):
    """
    比较两字符串是否相等
    :param a: 字符串
    :param b: 字符串
    :return: 相等、不相等
    """
    return a.lower() == b.lower()


def list_not_null(lists):
    """
    判断列表是否为空
    :param lists: 列表
    :return: 是、不是
    """
    return lists is not None and len(lists) > 0


def string_join(joiner, *args):
    """
    对字符串进行拼接
    :param joiner: 拼接符
    :param args: 多个参数
    :return: 字符串返回值
    """
    if args is None:
        return None
    i = 0
    string = ""
    for item in args:
        i += 1
        string += f'{item}'
        if len(args) != i:
            string += f'{joiner}'
    return string


def string_join_neglect_null(joiner, *args):
    """
    对字符串进行凭借，忽略多个目标中空值
    :param joiner: 拼接符
    :param args: 多个参数
    :return: 字符串返回值
    """
    if args is None:
        return None
    first = False
    string = ""
    for item in args:

        if is_not_null(item):
            if first:
                string += f'{joiner}'
            string += f'{item}'
            first = True
    return string


def create_java_function(scope, return_value, name, *args):
    """
    生成java方法字符串
    :param scope: 作用域
    :param return_value: 返回值
    :param name: 方法名称
    :param args: 参数，需要字符串，不用考虑前后逗号
    :return: 方法字符串
    """
    function = ""
    if is_not_null(scope):
        function += f'{scope} {return_value} {name}('
    else:
        function += f'{return_value} {name}('
    function += string_join_neglect_null(", ", *args)
    function += ")"
    return function


def create_java_interface(return_value, name, *args):
    """
    创建java的接口
    :param return_value: 返回类型
    :param name: 接口名称
    :param args: 参数，需要字符串，不用考虑逗号
    :return: 方法字符串
    """
    return f'\t{create_java_function(None, return_value, name, *args)};\n\n'
