from typing import List

from src.java.BaseModuleConfig import FileType


class AnalysisConfig:
    def __init__(self):
        """
        数据库链接解析类
        """
        self.database_host = "127.0.0.1"
        """ 数据库地址 """
        self.database_port = 3306
        """ 数据库端口 """
        self.database_user = "root"
        """ 数据库连接用户 """
        self.database_password = "123456"
        """ 数据库连接秘密 """
        self.database_name = None
        """ 连接数据库的名称 """
        self.database_type = "mysql"
        """ 数据库连接类型 """

        self.project_name = "com.test"
        """ 工程名称 """
        self.project_structure = "多层次结构MVC模式"
        """ 工程结构模式 """
        self.code_flow = {
            "controller": "service",
            "service": "mapper"
        }
        """ 工程模板流 """

        self.create_file: List[str] = [FileType.entityBase, FileType.xmlBaseMapper, FileType.javaBaseMapper]
        """ 生成的文件,枚举值为FileType类 """
        self.not_create_file: List[str] = []
        """ 不生成的文件,枚举值为FileType类 """
        self.analysis_table: List[str] = []
        """ 解析并生成的表 """
        self.analysis_not_create_table: List[str] = []
        """ 解析但不生成的表 """
        self.not_analysis_table: List[str] = []
        """ 不解析也不生成的表 """

        self.class_name_is_big_hump = True
        """ 将类名转成大驼峰 """
        self.class_name_table_prefix_string = None
        """ 需要统一移除的表前缀 """

        self.colum_need_hump = True
        """ 需要字段名称驼峰命名 """
        self.column_prefix_string = None
        """ 要统一移除的字段前缀 """
        self.column_prefix_table = True
        """ 要统一移除表名称作为的字段前缀 """

        self.multi_table = True
        """ 多表关系解析 """
        self.one_to_one = {}
        """ 指定一对一的表 """
        self.one_to_many = {}
        """ 指定一对多的表 """
        self.many_to_many = {}
        """ 指定多对多的表 """
        self.init_project = False
        """ 需要初始化工程 """
        self.add_to_module_package = True
        """ 将生成的代码添加至module子包下 """
        self.fast_json_to_string = True
        """ 使用fastJSON进行序列化 """
        self.use_cache = False
        """ 使用缓存类 """

    def use_default_project_structure(self):
        """ 使用默认的层次结构 """
        self.project_structure = "多层次结构MVC模式"
        self.use_default_flow()

    def use_domain_design_project_structure(self):
        """ 使用领域驱动设计层次结构 """
        self.project_structure = "领域驱动设计模式"
        self.use_domain_design_flow()

    def use_domain_design_flow(self):
        """
        使用领域驱动设计模板流
        """
        self.code_flow = {
            "controller": "service",
            "service": "domain",
            "domain": "repository",
            "repository": "mapper"
        }

    def use_default_flow(self):
        """
        使用默认模板流
        """
        self.code_flow = {
            "controller": "service",
            "service": "mapper"
        }

    def create_default_all_file(self):
        """
        生成默认的全部文件
        """
        self.create_file = [
            FileType.entityBase,  # 抽象基础实体
            FileType.entity,  # 实体
            FileType.service,  # 业务层接口
            FileType.serviceImpl,  # 业务层实现
            FileType.javaBaseMapper,  # mapper层抽象接口
            FileType.javaMapper,  # mapper接口
            FileType.xmlBaseMapper,  # mapper抽象接口的xml
            FileType.xmlMapper,  # mapper接口的xml
            FileType.controller,  # web控制层
            # FileType.api,  # rpc对外服务层
            # FileType.domain,  # 领域接口
            # FileType.domainImpl,  # 领域实现
            # FileType.cache,  # 缓存层
            # FileType.repository,  # 仓库接口
            # FileType.repositoryImpl,  # 仓库实现
        ]

    def create_default_all_and_cache(self):
        """
        生成默认的全部文件
        """
        self.use_cache = True
        self.create_file = [
            FileType.entityBase,  # 抽象基础实体
            FileType.entity,  # 实体
            FileType.service,  # 业务层接口
            FileType.serviceImpl,  # 业务层实现
            FileType.javaBaseMapper,  # mapper层抽象接口
            FileType.javaMapper,  # mapper接口
            FileType.xmlBaseMapper,  # mapper抽象接口的xml
            FileType.xmlMapper,  # mapper接口的xml
            FileType.controller,  # web控制层
            # FileType.api,  # rpc对外服务层
            # FileType.domain,  # 领域接口
            # FileType.domainImpl,  # 领域实现
            FileType.cache,  # 缓存层
            # FileType.repository,  # 仓库接口
            # FileType.repositoryImpl,  # 仓库实现
        ]

    def create_domain_design_all_file(self):
        """
        生成领域驱动设计的全部文件
        """
        self.create_file = [
            FileType.entityBase,  # 抽象基础实体
            FileType.entity,  # 实体
            FileType.service,  # 业务层接口
            FileType.serviceImpl,  # 业务层实现
            FileType.javaBaseMapper,  # mapper层抽象接口
            FileType.javaMapper,  # mapper接口
            FileType.xmlBaseMapper,  # mapper抽象接口的xml
            FileType.xmlMapper,  # mapper接口的xml
            FileType.controller,  # web控制层
            FileType.api,  # rpc对外服务层
            FileType.domain,  # 领域接口
            FileType.domainImpl,  # 领域实现
            FileType.cache,  # 缓存层
            FileType.repository,  # 仓库接口
            FileType.repositoryImpl,  # 仓库实现
        ]
