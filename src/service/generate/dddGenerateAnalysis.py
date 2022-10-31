import json
import os

from src.ddd.api import Controller, Api
from src.ddd.domain import Domain, DomainImpl
from src.ddd.entity import Entity, BaseEntity
from src.ddd.repository import Repository, RepositoryImpl
from src.ddd.repository.cache import Cache
from src.ddd.repository.mapper import JavaMapper, JavaBaseMapper
from src.ddd.service import Service, ServiceImpl
from src.service.mapper.xml import XmlMapper, XmlBaseMapper
from src.structure.CodeConfig import CodeConfig
from src.structure.CreateConfig import FileType
from src.util.OSUtil import save_file


class Generate:

    def __init__(self):
        path = "config"
        path = os.path.join(os.getcwd(), path)
        if not os.path.exists(path):
            raise FileNotFoundError("config文件夹不存在！！！！")
        list_file = os.listdir(path)
        self.data = []
        self.config = []
        for file in list_file:
            if ".json" in file:
                print(f"发现{file}")
                self.data.append(json.load(open(os.path.join(path, file), encoding="utf-8")))
        print(f"总共{len(self.data)}个文件")

    def code_config(self):
        """
        字典转对象配置
        """
        for d in self.data:
            code_config = CodeConfig.get_code_config(d)
            self.config.append(code_config)
            # for i in code_config.__dict__:
            #     print(i, code_config.__getattribute__(i))
            # print()
            # for i in code_config.oneToMany:
            #     for j in i.__dict__:
            #         print(j, i.__getattribute__(j))

    def generate(self):
        print("开始准备解析")
        self.code_config()
        for i in range(len(self.config)):
            self.__parsing(self.config[i], self.data[i])

    def __parsing(self, config: CodeConfig, dict_config: dict):

        # 生成控制层
        if self.check_create(FileType.controller, config):
            string = Controller.CreateFile.create(config)
            save_file(config.module.controller.path, config.module.controller.className, "java", string)

        # RPC接入层
        if self.check_create(FileType.api, config):
            string = Api.CreateFile.create(config)
            save_file(config.module.api.path, config.module.api.className, "java", string)

        # 业务接口层
        if self.check_create(FileType.service, config):
            string = Service.CreateFile.create(config)
            save_file(config.module.serviceInterface.path, config.module.serviceInterface.className, "java", string)

        # 业务接口实现
        if self.check_create(FileType.serviceImpl, config):
            string = ServiceImpl.CreateFile.create(config)
            save_file(config.module.serviceImplements.path, config.module.serviceImplements.className, "java", string)

        # 领域层接口
        if self.check_create(FileType.domain, config):
            string = Domain.CreateFile.create(config)
            save_file(config.module.domain.path, config.module.domain.className, "java", string)

        # 领域层接口实现
        if self.check_create(FileType.domainImpl, config):
            string = DomainImpl.CreateFile.create(config)
            save_file(config.module.domainImpl.path, config.module.domainImpl.className, "java", string)

        # 仓库层接口
        if self.check_create(FileType.repository, config):
            string = Repository.CreateFile.create(config)
            save_file(config.module.repository.path, config.module.repository.className, "java", string)

        # 仓库层接口实现
        if self.check_create(FileType.repositoryImpl, config):
            string = RepositoryImpl.CreateFile.create(config)
            save_file(config.module.repositoryImpl.path, config.module.repositoryImpl.className, "java", string)

        # mapper层接口
        if self.check_create(FileType.javaMapper, config):
            string = JavaMapper.CreateFile.create(config)
            save_file(config.module.mapperInterface.path, config.module.mapperInterface.className, "java", string)

        # 抽象mapper层接口
        if self.check_create(FileType.javaBaseMapper, config):
            string = JavaBaseMapper.CreateFile.create(config)
            save_file(config.module.baseMapperInterface.path, config.module.baseMapperInterface.className, "java", string)

        # cache层接口
        if self.check_create(FileType.cache, config):
            string = Cache.CreateFile.create(config)
            save_file(config.module.cache.path, config.module.cache.className, "java", string)

        # 实体
        if self.check_create(FileType.entity, config):
            string = Entity.CreateFile.create(config)
            save_file(config.path, config.className, "java", string)

        # 抽象实体
        if self.check_create(FileType.entityBase, config):
            string = BaseEntity.CreateFile.create(config)
            save_file(config.module.baseEntity.path, config.module.baseEntity.className, "java", string)

        # 生成Mapper.xml文件
        if self.check_create(FileType.xmlMapper, config):
            string = XmlMapper.CreateFile.create(dict_config)
            save_file(dict_config["module"]["mapperXml"]["path"], f'{dict_config["module"]["mapperXml"]["className"]}', "xml", string)

        # 生成自动生成的XML文件
        if self.check_create(FileType.xmlBaseMapper, config):
            string = XmlBaseMapper.CreateFile.create(dict_config)
            save_file(dict_config["module"]["baseMapperXml"]["path"], f'{dict_config["module"]["baseMapperXml"]["className"]}', "xml", string)

    @staticmethod
    def check_create(create_type: str, config: CodeConfig):
        """
        检查文件是否能生成
        :param create_type: 生成的类型
        :param config: 配置信息
        :return: true:能/false:不能
        """
        create_list = config.createConfig.createFile.value
        if create_list is None:
            create_list = config.createConfig.createFile.default
        not_create_list = config.createConfig.notCreateFile.value
        if not_create_list is None:
            not_create_list = config.createConfig.notCreateFile.default
        return create_type in create_list and create_type not in not_create_list
