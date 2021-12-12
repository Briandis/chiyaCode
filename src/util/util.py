def if_return(boolean, true, false):
    """
    三目运算
    :param boolean: 真假
    :param true: 正确获取的
    :param false: 失败获取的
    """
    if boolean:
        return true
    return false


def dict_set(data: dict, key: str, value: str):
    """
    字典set结构
    :param data:字典
    :param key: Key
    :param value: 值
    """
    if key not in data:
        data[key] = set()
    data[key].add(value)


def dict_dict(data: dict, key: str, key2: str, value: str):
    """
    字典套字典结构
    :param data:字典
    :param key: Key
    :param value: 值
    """
    if key not in data:
        data[key] = {key2: value}
    else:
        data[key][key2] = value
