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
