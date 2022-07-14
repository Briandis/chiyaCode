import os


def is_not_dir_create(path: str, dir: str):
    """
    如果没有文件夹，则创建
    :param path: 文件路径
    :param dir: 当前的文件夹
    :return: 当前构建的路径
    """
    path = os.path.join(path, dir)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def create_dir(packet_name: str) -> str:
    """
    创建文件夹
    :param packet_name:java的模块路径
    :return:
    """
    lists = packet_name.split(".")
    path = os.getcwd()

    path = is_not_dir_create(path, "data")
    path = is_not_dir_create(path, "src")
    for i in lists:
        path = os.path.join(path, i)
        if not os.path.exists(path):
            os.mkdir(path)
    return path


def save_file(path, file_name, suffix, data):
    """
    保存文件
    :param path: 文件路径，java包名的
    :param file_name: 文件名
    :param suffix: 文件后缀
    :param data: 存储的字符数据
    :return:
    """
    path = create_dir(path)
    if "." not in suffix:
        suffix = "." + suffix
    with open(os.path.join(path, file_name + suffix), "w", encoding="utf-8") as file:
        file.write(data)


def save_file_java(package, class_name, data):
    """
    构建java文件
    :param package:所在包路径
    :param class_name: 类名
    :param data: 文件内容
    """
    save_file(package, class_name, "java", data)
