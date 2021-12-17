import json
import os

from src.constant.ProtocolConstant import JsonKey
from src.service.controller import Controller
from src.service.entity import Entity, BaseEntity
from src.service.mapper.xml import XmlMapper, XmlBaseMapper
from src.service.mapper.java import JavaMapper, JavaBaseMapper
from src.service.service import Service, ServiceImpl
from src.util import StringUtil


def is_not_dir_create(path, dir):
    path = os.path.join(path, dir)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def create_dir(packet_name: str) -> str:
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
    path = create_dir(path)
    if "." not in suffix:
        suffix = "." + suffix
    with open(os.path.join(path, file_name + suffix), "w", encoding="utf-8") as file:
        file.write(data)


class FileType:
    controller = "Controller"
    service = "Service"
    serviceImpl = "ServiceImpl"
    javaMapper = "JavaMapper"
    javaBaseMapper = "JavaBaseMapper"
    xmlMapper = "XmlMapper"
    xmlBaseMapper = "XmlBaseMapper"
    entity = "Entity"
    entityBase = "EntityBase"


class Generate:

    def __init__(self):
        path = "config"
        path = os.path.join(os.getcwd(), path)
        if not os.path.exists(path):
            raise FileNotFoundError("config文件夹不存在！！！！")
        list_file = os.listdir(path)
        self.data = []
        for file in list_file:
            if ".json" in file:
                print(f"发现{file}")
                self.data.append(json.load(open(os.path.join(path, file), encoding="utf-8")))
        print(f"总共{len(self.data)}个文件")

    def generate(self):
        print("开始准备解析")
        for i in self.data:
            self.__parsing(i)

    def __parsing(self, data: dict):
        create_file = [
            FileType.controller,
            FileType.service,
            FileType.serviceImpl,
            FileType.javaMapper,
            FileType.javaBaseMapper,
            FileType.xmlMapper,
            FileType.xmlBaseMapper,
            FileType.entity,
            FileType.entityBase
        ]
        # if StringUtil.list_not_null(data[JsonKey.config.self][JsonKey.config.createFile.self][JsonKey.config.createFile.value]):
        #     create_file = data[JsonKey.config.self][JsonKey.config.createFile.self][JsonKey.config.createFile.value]

        not_create_file = []
        if StringUtil.list_not_null(data[JsonKey.config.self][JsonKey.config.notCreateFile.self][JsonKey.config.notCreateFile.value]):
            not_create_file = data[JsonKey.config.self][JsonKey.config.notCreateFile.self][JsonKey.config.notCreateFile.value]

        # 生成实体类文件
        if FileType.entity in create_file and FileType.entity not in not_create_file:
            string = Entity.CreateFile.create(data)
            save_file(data["path"], data["className"], "java", string)

        # 生成自动生成实体类文件
        if FileType.entityBase in create_file and FileType.entityBase not in not_create_file:
            string = BaseEntity.CreateFile.create(data)
            save_file(data["baseEntity"]["path"], f'{data["baseEntity"]["className"]}', "java", string)

        # 生成service接口件
        if FileType.service in create_file and FileType.service not in not_create_file:
            string = Service.CreateFile.create(data)
            # print(string)
            save_file(data["serviceInterface"]["path"], f'{data["serviceInterface"]["className"]}', "java", string)

        # 生成serviceImpl实现类文件
        if FileType.serviceImpl in create_file and FileType.serviceImpl not in not_create_file:
            string = ServiceImpl.CreateFile.create(data)
            # print(string)
            save_file(data["serviceImplements"]["path"], f'{data["serviceImplements"]["className"]}', "java", string)

        # 生成Controller文件
        if FileType.controller in create_file and FileType.controller not in not_create_file:
            string = Controller.CreateFile.create(data)
            # print(string)
            save_file(data["controller"]["path"], f'{data["controller"]["className"]}', "java", string)

        # 生成mapper.java文件
        if FileType.javaMapper in create_file and FileType.javaMapper not in not_create_file:
            string = JavaMapper.CreateFile.create(data)
            save_file(data["mapperInterface"]["path"], f'{data["mapperInterface"]["className"]}', "java", string)

        # 生成自动生成的mapper.java文件
        if FileType.javaBaseMapper in create_file and FileType.javaBaseMapper not in not_create_file:
            string = JavaBaseMapper.CreateFile.create(data)
            save_file(data["baseMapperInterface"]["path"], f'{data["baseMapperInterface"]["className"]}', "java", string)

        # 生成Mapper.xml文件
        if FileType.xmlMapper in create_file and FileType.xmlMapper not in not_create_file:
            string = XmlMapper.CreateFile.create(data)
            save_file(data["mapperXml"]["path"], f'{data["mapperXml"]["className"]}', "xml", string)

        # 生成自动生成的XML文件
        if FileType.xmlBaseMapper in create_file and FileType.xmlBaseMapper not in not_create_file:
            string = XmlBaseMapper.CreateFile.create(data)
            save_file(data["baseMapperXml"]["path"], f'{data["baseMapperXml"]["className"]}', "xml", string)
