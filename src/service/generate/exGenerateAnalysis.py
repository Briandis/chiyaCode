import json
import os
from src.service import serviceCreate
from src.controller import controllerCreate
from src.mapper import JAVAExMapperCreate, XMLExMapperCreate
from src.pojo import POJOExtradimensionalClone
from src.service import serviceImplExtradimensionalClone


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
    with open(os.path.join(path, file_name + suffix), "w") as file:
        file.write(data)


class ExGenerate:

    def __init__(self):
        path = "exConfig"
        path = os.path.join(os.getcwd(), path)
        if not os.path.exists(path):
            raise FileNotFoundError("exConfig文件夹不存在！！！！")
        list_file = os.listdir(path)
        self.data = []
        for file in list_file:
            if ".json" in file:
                print(f"发现{file}")
                self.data.append(json.load(open(os.path.join(path, file))))
        print(f"总共{len(self.data)}个文件")

    def generate(self):
        print("开始准备解析")
        for i in self.data:
            self.__parsing(i)

    def __parsing(self, data: dict):

        m_data = data["extradimensionalData"]
        # 生成Controller文件
        string = controllerCreate.create(m_data)
        save_file(m_data["path_controller"], m_data["controllerName"], "java", string)

        # 生成service接口件
        string = serviceCreate.create_service(m_data)
        save_file(m_data["path_service"], m_data["serviceName"], "java", string)

        # 生成mapper.java文件
        string = JAVAExMapperCreate.create_java_mapper(data)
        save_file(m_data["path_java_mapper"], m_data["javaMapperName"], "java", string)

        # 生成Mapper.xml文件
        string = XMLExMapperCreate.create_xml_mapper(data)
        save_file(m_data["path_xml_mapper"], m_data["XMLMapperName"], "xml", string)

        # # 生成serviceImpl实现类文件
        string = serviceImplExtradimensionalClone.create_service_impl(data)
        save_file(m_data["path_service_impl"], m_data["serviceImplName"], "java", string)

        # 生成实体类文件
        string = POJOExtradimensionalClone.create_pojo(data)
        save_file(m_data["path_pojo"], m_data["className"], "java", string)
