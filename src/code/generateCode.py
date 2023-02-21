import json
import os

from src.java import JavaCode
from src.java.BaseModuleConfig import FileType
from src.java.CodeConfig import CodeConfig
from src.module.api import Api
from src.module.api.Controller import ControllerJavaCode
from src.module.base import BaseApi
from src.module.domain import Domain
from src.module.domain.DomainImpl import DomainImplJavaCode
from src.module.entity import Entity, BaseEntity
from src.module.repository import Repository
from src.module.repository.RepositoryImpl import RepositoryImplJavaCode
from src.module.repository.cache import Cache
from src.module.repository.mapper import JavaMapper, JavaBaseMapper
from src.module.repository.mapper.XmlBaseMapper import XmlBaseMapperCode
from src.module.repository.mapper.XmlMapper import XmlMapperCode
from src.module.service import Service
from src.module.service.ServiceImpl import ServiceImplJavaCode
from src.util.chiyaUtil import OSUtil


class CodeTemplate:

    @staticmethod
    def analyze_template_flow(codeConfig: CodeConfig):
        """
        解析代码流
        :param codeConfig: 代码配置
        :return: 代码流
        """
        if codeConfig.createConfig.codeTemplateFlow.value is not None:
            code_list = codeConfig.createConfig.codeTemplateFlow.value.split("->")
        else:
            return codeConfig.createConfig.codeTemplateFlow.default
        for i in range(len(code_list)):
            code_list[i] = code_list[i].replace(" ", "")
        # 得到有效排序集
        new_code_list = []
        for i in code_list:
            if i.lower() in ["controller", "service", "domain", "repository", "mapper"]:
                new_code_list.append(i.lower())
        code_flow = {}
        for i in range(1, len(new_code_list)):
            code_flow[new_code_list[i - 1]] = new_code_list[i]
        return code_flow

    @staticmethod
    def get_template(template_type: str, next_type: str, codeConfig: CodeConfig):
        if template_type == "controller":
            return ControllerJavaCode.create(codeConfig, JavaCode.DefaultAttribute.get_service(codeConfig))

        if template_type == "service":
            if next_type == "domain":
                return ServiceImplJavaCode.create(codeConfig, JavaCode.DefaultAttribute.get_domain(codeConfig), BaseApi.BaseAPIImpl)
            if next_type == "repository":
                return ServiceImplJavaCode.create(codeConfig, JavaCode.DefaultAttribute.get_repository(codeConfig), BaseApi.BaseAPIImpl)
            if next_type == "mapper":
                return ServiceImplJavaCode.create(codeConfig, JavaCode.DefaultAttribute.get_mapper(codeConfig), BaseApi.BaseRepository)

        if template_type == "domain":
            if next_type == "repository":
                return DomainImplJavaCode.create(codeConfig, JavaCode.DefaultAttribute.get_repository(codeConfig), BaseApi.BaseAPIImpl)
            if next_type == "mapper":
                return DomainImplJavaCode.create(codeConfig, JavaCode.DefaultAttribute.get_mapper(codeConfig), BaseApi.BaseRepository)

        if template_type == "repository":
            if next_type == "mapper":
                return RepositoryImplJavaCode.create(codeConfig, JavaCode.DefaultAttribute.get_mapper(codeConfig), BaseApi.BaseRepository)


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
        for config in self.data:
            code_config = CodeConfig.get_code_config(config)
            self.config.append(code_config)

    def generate(self):
        print("开始准备解析")
        self.code_config()
        for code_config in self.config:
            self.parsing(code_config)

    def parsing(self, codeConfig: CodeConfig):

        code_flow = CodeTemplate.analyze_template_flow(codeConfig)
        # 生成控制层
        if self.check_create(FileType.controller, codeConfig):
            string = CodeTemplate.get_template("controller", code_flow.get("controller"), codeConfig)
            OSUtil.save_file(codeConfig.module.controller.path, codeConfig.module.controller.className, "java", string)

        # RPC接入层
        if self.check_create(FileType.api, codeConfig):
            string = Api.APIJavaCode.create(codeConfig)
            OSUtil.save_file(codeConfig.module.api.path, codeConfig.module.api.className, "java", string)

        # 业务接口层
        if self.check_create(FileType.service, codeConfig):
            string = Service.ServiceJavaCode.create(codeConfig)
            OSUtil.save_file(codeConfig.module.serviceInterface.path, codeConfig.module.serviceInterface.className, "java", string)

        # 业务接口实现
        if self.check_create(FileType.serviceImpl, codeConfig):
            string = CodeTemplate.get_template("service", code_flow.get("service"), codeConfig)
            OSUtil.save_file(codeConfig.module.serviceImplements.path, codeConfig.module.serviceImplements.className, "java", string)

        # 领域层接口
        if self.check_create(FileType.domain, codeConfig):
            string = Domain.DomainJavaCode.create(codeConfig)
            OSUtil.save_file(codeConfig.module.domain.path, codeConfig.module.domain.className, "java", string)

        # 领域层接口实现
        if self.check_create(FileType.domainImpl, codeConfig):
            string = CodeTemplate.get_template("domain", code_flow.get("domain"), codeConfig)
            OSUtil.save_file(codeConfig.module.domainImpl.path, codeConfig.module.domainImpl.className, "java", string)

        # 仓库层接口
        if self.check_create(FileType.repository, codeConfig):
            string = Repository.RepositoryJavaCode.create(codeConfig)
            OSUtil.save_file(codeConfig.module.repository.path, codeConfig.module.repository.className, "java", string)

        # 仓库层接口实现
        if self.check_create(FileType.repositoryImpl, codeConfig):
            string = CodeTemplate.get_template("repository", code_flow.get("repository"), codeConfig)
            OSUtil.save_file(codeConfig.module.repositoryImpl.path, codeConfig.module.repositoryImpl.className, "java", string)

        # mapper层接口
        if self.check_create(FileType.javaMapper, codeConfig):
            string = JavaMapper.MapperJavaCode.create(codeConfig)
            OSUtil.save_file(codeConfig.module.mapperInterface.path, codeConfig.module.mapperInterface.className, "java", string)

        # 抽象mapper层接口
        if self.check_create(FileType.javaBaseMapper, codeConfig):
            string = JavaBaseMapper.BaseMapperJavaCode.create(codeConfig)
            OSUtil.save_file(codeConfig.module.baseMapperInterface.path, codeConfig.module.baseMapperInterface.className, "java", string)

        # cache层接口
        if self.check_create(FileType.cache, codeConfig):
            string = Cache.CacheJavaCode.create(codeConfig)
            OSUtil.save_file(codeConfig.module.cache.path, codeConfig.module.cache.className, "java", string)

        # 实体
        if self.check_create(FileType.entity, codeConfig):
            string = Entity.EntityJavaCode.create(codeConfig)
            OSUtil.save_file(codeConfig.module.entity.path, codeConfig.module.entity.className, "java", string)

        # 抽象实体
        if self.check_create(FileType.entityBase, codeConfig):
            string = BaseEntity.BaseEntityJavaCode.create(codeConfig)
            OSUtil.save_file(codeConfig.module.baseEntity.path, codeConfig.module.baseEntity.className, "java", string)

        # 生成Mapper.xml文件
        if self.check_create(FileType.xmlMapper, codeConfig):
            string = XmlMapperCode.create(codeConfig)
            OSUtil.save_file(codeConfig.module.mapperXml.path, codeConfig.module.mapperXml.className, "xml", string)

        # 生成自动生成的XML文件
        if self.check_create(FileType.xmlBaseMapper, codeConfig):
            string = XmlBaseMapperCode.create(codeConfig)
            OSUtil.save_file(codeConfig.module.baseMapperXml.path, codeConfig.module.baseMapperXml.className, "xml", string)

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
