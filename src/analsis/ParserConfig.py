import os
from typing import List, Dict

from src.analsis.AnalysisConfig import AnalysisConfig
from src.analsis.MultiTableParser import MultiTableParser
from src.analsis.MySQLAnalysis import DataBase, MySQLAnalysis
from src.java.CodeConfig import CodeConfig, Field
from src.project.createProject import ProjectInit
from src.util.chiyaUtil import StringUtil, SQLTypeDict, TypeConstant, JsonUtil


class ParserConfig:
    """
    解析类
    """

    @staticmethod
    def code_config_init(tables: List[DataBase], config: AnalysisConfig) -> Dict[str, CodeConfig]:
        """
        解析字段
        @return 表名与配置映射
        """
        javabean = {}

        for table in tables:
            code_config = CodeConfig()
            code_config.baseInfo.tableName = table.table_name
            code_config.module.entity.className = table.table_name
            code_config.module.entity.remark = table.table_comment
            code_config.baseInfo.databaseType = config.database_type

            # 统一移除表前缀
            if config.class_name_table_prefix_string:
                code_config.module.entity.className = StringUtil.remove_prefix(code_config.module.entity.className, config.class_name_table_prefix_string)
            # 类名转大驼峰
            if config.class_name_is_big_hump:
                code_config.module.entity.className = StringUtil.underscore_to_big_hump(code_config.module.entity.className)

            # 解析字段
            for column in table.columns:
                attribute = Field()
                attribute.attr = column.name
                attribute.field = column.name
                attribute.type = column.data_type
                attribute.remark = column.column_comment
                # 移除统一字段前缀
                if config.column_prefix_string:
                    attribute.attr = StringUtil.remove_prefix(attribute.attr, config.column_prefix_string)
                # 移除表统一字段前缀
                if config.column_prefix_table:
                    attribute.attr = StringUtil.remove_prefix(attribute.attr, f'{table.table_name}_')
                # 属性名驼峰
                if config.colum_need_hump:
                    attribute.attr = StringUtil.underscore_to_small_hump(attribute.attr)
                # JAVA类型转换
                attribute.type = SQLTypeDict.get(column.data_type)
                # 模糊搜索处理
                if attribute.type == TypeConstant.STRING:
                    code_config.createConfig.fuzzySearch.enable = True
                    code_config.createConfig.fuzzySearch.data.append(attribute.field)
                if column.column_key == "PRI" and code_config.baseInfo.key is None:
                    code_config.baseInfo.key = attribute
                else:
                    code_config.baseInfo.attr.append(attribute)

            # 装配生成和非生成信息
            if config.create_file:
                code_config.createConfig.createFile.value = config.create_file
            if config.not_create_file:
                code_config.createConfig.notCreateFile.value = config.not_create_file
            # 工程模板流
            code_config.createConfig.codeTemplateFlow.value = config.code_flow
            # toString方法设置
            code_config.createConfig.toJsonString.isFastJson = config.fast_json_to_string
            # 是否使用缓存
            code_config.createConfig.repositoryUseCache.enable = config.use_cache

            javabean[table.table_name] = code_config
        return javabean

    @staticmethod
    def create(config: AnalysisConfig):
        # 需要初始化工程
        if config.init_project:
            ProjectInit.init(config.project_name)

        mysql = MySQLAnalysis(config.database_name, config.database_host, config.database_user, config.database_password, config.database_port)
        list_table = mysql.get_all_table()
        tables = ParserConfig.parser(list_table, config)

        path = os.path.join(os.getcwd(), "config")
        if not os.path.exists(path):
            os.mkdir(path)

        print("解析但不生成的表：", config.analysis_not_create_table)

        for table in tables:
            # 生成的表和不生成的表
            if (table.baseInfo.tableName in config.analysis_table or not config.analysis_table) and table.baseInfo.tableName not in config.analysis_not_create_table:
                config_json = JsonUtil.to_json(table)
                open(f"config\\{table.baseInfo.tableName}.json", "w", encoding="utf-8").write(config_json)

        return list_table

    @staticmethod
    def parser(tables: List[DataBase], config: AnalysisConfig):
        """
        解析
        @param tables: 数据库表结构
        @param config: 配置信息
        @return codeConfig 生成配置信息
        """
        dict_config = ParserConfig.code_config_init(tables, config)
        list_config = []
        for table_name, config_code in dict_config.items():
            list_config.append(config_code)
            ParserConfig.set_project_model(config_code, config)
        list_config = MultiTableParser.create(list_config, config)
        return list_config

    @staticmethod
    def set_model_value(lists: List[str], code_config: CodeConfig, config: AnalysisConfig):
        """
        根据列表直接装配
        :param lists:路径集合
        :param code_config:生成配置
        :param config:配置信息
        """
        # 自动添加只module包下
        module_name = "."
        if config.add_to_module_package:
            module_name = ".module."

        class_name = code_config.module.entity.className
        remark = code_config.module.entity.remark
        code_config.module.baseEntity.set_module(f'{config.project_name}{module_name}{lists[0]}', f'Base{class_name}', f'{remark}基础抽象类')
        code_config.module.entity.path = f'{config.project_name}{module_name}{lists[1]}'
        code_config.module.serviceInterface.set_module(f'{config.project_name}{module_name}{lists[2]}', f'{class_name}Service', f'{remark}业务接口')
        code_config.module.serviceImplements.set_module(f'{config.project_name}{module_name}{lists[3]}', f'{class_name}ServiceImpl', f'{remark}业务默认实现类')
        code_config.module.baseMapperInterface.set_module(f'{config.project_name}{module_name}{lists[4]}', f'Base{class_name}Mapper', f'{remark}Mapper层基础抽象接口')
        code_config.module.mapperInterface.set_module(f'{config.project_name}{module_name}{lists[5]}', f'{class_name}Mapper', f'{remark}Mapper扩展接口')
        code_config.module.baseMapperXml.set_module(f'{config.project_name}{module_name}{lists[6]}', f'Base{class_name}Mapper', f'{remark}Mapper层基础抽象接口')
        code_config.module.mapperXml.set_module(f'{config.project_name}{module_name}{lists[7]}', f'{class_name}Mapper', f'{remark}Mapper扩展接口')
        code_config.module.controller.set_module(f'{config.project_name}{module_name}{lists[8]}', f'{class_name}Controller', f'{remark}控制层')
        # 领域驱动设计
        code_config.module.api.set_module(f'{config.project_name}{module_name}{lists[9]}', f'{class_name}API', f'{remark}扩展API接口')
        code_config.module.domain.set_module(f'{config.project_name}{module_name}{lists[10]}', f'{class_name}Domain', f'{remark}领域层接口')
        code_config.module.domainImpl.set_module(f'{config.project_name}{module_name}{lists[11]}', f'{class_name}DomainImpl', f'{remark}领域层默认实现')
        code_config.module.repository.set_module(f'{config.project_name}{module_name}{lists[12]}', f'{class_name}Repository', f'{remark}仓库层接口')
        code_config.module.repositoryImpl.set_module(f'{config.project_name}{module_name}{lists[13]}', f'{class_name}RepositoryImpl', f'{remark}仓库层默认实现')
        code_config.module.cache.set_module(f'{config.project_name}{module_name}{lists[14]}', f'{class_name}Cache', f'{remark}缓存层')

    @staticmethod
    def set_project_model(code_config: CodeConfig, config: AnalysisConfig):
        """
        生成模块
        :param code_config: 配置信息
        :param config:模式类型
        """

        # 表多级模块化，MVC模式，默认
        suffix = StringUtil.replace_keyword(code_config.baseInfo.tableName, "_", ".").lower()
        module_data = [
            f'{suffix}.entity', f'{suffix}.entity',  # 抽象实体、实体
            f'{suffix}.service', f'{suffix}.service',  # 业务层、业务实现层
            f'{suffix}.mapper', f'{suffix}.mapper',  # 抽象javaMapper、javaMapper
            f'{suffix}.mapper', f'{suffix}.mapper',  # 抽象xmlMapper、xmlMapper
            f'{suffix}.controller', f'{suffix}.controller',  # 控制层、RPC接入层
            f'{suffix}.domain', f'{suffix}.domain',  # 领域层、领域层实现
            f'{suffix}.repository', f'{suffix}.repository',  # 仓库层、仓库层实现
            f'{suffix}.cache'  # 缓存层
        ]

        if StringUtil.eq(config.project_structure, "领域驱动设计模式", True):
            # 领域驱动设计
            suffix = StringUtil.replace_keyword(code_config.baseInfo.tableName, "_", ".").lower()
            module_data = [
                f'{suffix}.entity', f'{suffix}.entity',  # 抽象实体、实体
                f'{suffix}.service', f'{suffix}.service',  # 业务层、业务实现层
                f'{suffix}.repository.mapper', f'{suffix}.repository.mapper',  # 抽象javaMapper、javaMapper
                f'{suffix}.repository.mapper', f'{suffix}.repository.mapper',  # 抽象xmlMapper、xmlMapper
                f'{suffix}.api', f'{suffix}.api',  # 控制层、RPC接入层
                f'{suffix}.domain', f'{suffix}.domain',  # 领域层、领域层实现
                f'{suffix}.repository', f'{suffix}.repository',  # 仓库层、仓库层实现
                f'{suffix}.repository.cache'  # 缓存层
            ]
        ParserConfig.set_model_value(module_data, code_config, config)
