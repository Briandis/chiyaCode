from typing import List

from src.java.BaseModuleConfig import CreateConfig
from src.util.chiyaUtil import StringUtil, ObjectUtil


class Field:
    """
    字段属性
    """

    def __init__(self):
        self.field = None
        """ 数据库字段名称 """
        self.attr = None
        """ 属性名称 """
        self.remark = None
        """ 注释 """
        self.type = None
        """ 数据类型 """
        self.alias = None
        """ 字段别名 """

    @staticmethod
    def create_field(attr_dict: dict):
        """
        根据字段，生成对象
        :param attr_dict: 字段数据
        :return: 字段对象
        """
        field = Field()
        if attr_dict is None:
            return None
        ObjectUtil.object_set_attr(field, attr_dict)
        return field

    def low_name(self):
        """
        获取小写的属性名
        :return:
        """
        return StringUtil.first_char_lower_case(self.attr)

    def upper_name(self):
        """
        获取大写的属性名
        :return:
        """
        return StringUtil.first_char_upper_case(self.attr)

    def get_field(self):
        """
        获取字段，如果别名存在，则使用别名
        :return: field或alias
        """
        if self.alias is None:
            return self.field
        return self.alias


class ModuleInfo:
    """
    模块信息
    """

    def __init__(self, path: str = None, class_name: str = None, remark: str = None):
        self.path = path
        """ 所在路径 """
        self.className = class_name
        """ 类型名称 """
        self.remark = remark
        """ 备注 """

    def low_name(self):
        """
        获取小写的类名
        :return: 小写的类名
        """
        return StringUtil.first_char_lower_case(self.className)

    def upper_name(self):
        """
        获取大写的类名
        :return: 大写的类名
        """
        return StringUtil.first_char_upper_case(self.className)

    def get_package(self):
        """
        获取全路径
        :return:全路径
        """
        return self.path + "." + self.className

    def set_module(self, module_path, module_class_name, module_remark):
        """
        设置模块信息
        @param module_path:类路径
        @param module_class_name:类名
        @param module_remark:类备注
        """
        self.path = module_path
        self.className = module_class_name
        self.remark = module_remark


class ModuleConfig:
    """
    模块配置
    """

    def __init__(self):
        self.entity = ModuleInfo()
        """ 实体 """
        self.baseEntity = ModuleInfo()
        """ 抽象实体 """
        self.serviceInterface = ModuleInfo()
        """ 业务层接口 """
        self.serviceImplements = ModuleInfo()
        """ 业务层实现 """
        self.baseMapperInterface = ModuleInfo()
        """ 基础mapper层接口 """
        self.mapperInterface = ModuleInfo()
        """ 用户mapper实现 """
        self.baseMapperXml = ModuleInfo()
        """ 基础mapper层XML """
        self.mapperXml = ModuleInfo()
        """ mapper层XML """
        self.controller = ModuleInfo()
        """ 控制层 """

        # 领域驱动设计相关
        self.api = ModuleInfo()
        """ api接入层 """
        self.domain = ModuleInfo()
        """ 领域层接口 """
        self.domainImpl = ModuleInfo()
        """ 领域层实现 """
        self.repository = ModuleInfo()
        """ 仓库层接口 """
        self.repositoryImpl = ModuleInfo()
        """ 仓库层实现 """
        self.cache = ModuleInfo()
        """ 缓存层 """

    @staticmethod
    def set_module(module: ModuleInfo, module_path, module_class_name, module_remark):
        """
        设置模块信息
        @param module：模块
        @param module_path:类路径
        @param module_class_name:类名
        @param module_remark:类备注
        """
        module.path = module_path
        module.className = module_class_name
        module.remark = module_remark


class ManyToMany:
    """
    多对多
    """

    def __init__(self):
        # 中间表
        self.to: CodeConfig | None = None
        # 另一方多的
        self.many: CodeConfig | None = None

    @staticmethod
    def get_many_to_many(config: dict):
        """
        多对多的配置字段转对象
        :param config: 配置字典
        :return: 对象
        """
        many_to_many = ManyToMany()
        many_to_many.to = CodeConfig.get_code_config(config.get("to"))
        many_to_many.many = CodeConfig.get_code_config(config.get("many"))
        return many_to_many


class BaseInfo:
    """
    基础信息
    """

    def __init__(self):
        self.tableName: str | None = None
        """ 表名称 """
        self.databaseType: str | None = None
        """ 数据库类型 """
        self.key: Field | None = None
        """ 主键信息 """
        self.attr: List[Field] = []
        """ 其他字段 """
        self.oneToOne: List[CodeConfig] = []
        """ 一对一的配置 """
        self.oneToMany: List[CodeConfig] = []
        """ 一对多的配置 """
        self.manyToMany: List[ManyToMany] = []
        """ 多对多 """
        self.foreignKey: str | None = None
        """ 在多表关系中，充当的外键 """
        self.aliasTable: str | None = None
        """ 表的别名 """

    def init(self, config: dict):
        """
        初始化基础信息
        :param config:配置的字典
        """
        # 迭代当前属性，将null的初始值，进行赋值，
        for i in self.__dict__:
            if self.__getattribute__(i) is None:
                self.__setattr__(i, config.get(i))
        # 装配主键信息，可能没没有key
        self.key = Field.create_field(config.get("key"))
        # 装配其他属性信息
        for attr in config.get("attr"):
            self.attr.append(Field.create_field(attr))
        # 一对一关系处理
        if "oneToOne" in config:
            for i in config["oneToOne"]:
                self.oneToOne.append(CodeConfig.get_code_config(i))
        # 一对多关系处理
        if "oneToMany" in config:
            for i in config["oneToMany"]:
                self.oneToMany.append(CodeConfig.get_code_config(i))
        # 多对多关系处理
        if "manyToMany" in config:
            for i in config["manyToMany"]:
                self.manyToMany.append(ManyToMany.get_many_to_many(i))

    def need_sql_block(self):
        """
        该类需要字段别名
        :return: True:需要SQL块/False:不需要
        """
        if self.aliasTable is not None:
            return True
        for field in self.attr:
            if field.alias is not None:
                return True
        return False

    def get_table_alias(self):
        """
        获取表的别名，如果不存在，则获取本名
        :return: 别名，存在则本名
        """
        if self.aliasTable is None:
            return self.tableName
        return self.aliasTable

    def check_key_in_attr(self, key: str):
        """
        检查key是否在属性列表中
        :param key:属性
        """
        for attr in self.attr:
            if StringUtil.is_string_tail(attr.field, key):
                return True
        return False


class CodeConfig:
    """
    生成器依赖的配置实体
    """

    def __init__(self):
        self.baseInfo = BaseInfo()
        """ 基础信息 """
        self.createConfig: CreateConfig = CreateConfig()
        """ 生成配置信息 """
        self.module = ModuleConfig()
        """ 模块配置信息 """

    @staticmethod
    def get_code_config(config: dict):
        """
        根据配置字典，构造配置对象
        :param config:配置字典
        :return: 配置对象
        """

        code_config = CodeConfig()
        # 基础数据处理
        code_config.baseInfo.init(config.get("baseInfo"))
        # 模块处理
        if "module" in config:
            for module in config["module"]:
                ObjectUtil.object_set_attr(code_config.module.__getattribute__(module), config["module"][module])
        # 生成配置处理
        if "createConfig" in config:
            for key in config["createConfig"]:
                ObjectUtil.object_set_attr(code_config.createConfig.__getattribute__(key), config["createConfig"][key])
        MultiTableParsing.parsing(code_config)
        return code_config

    def get_class_name(self, condition=False, save=False):
        """
        获取其他类名
        :return: 条件的类名称
        """
        if condition:
            return f'condition{self.module.entity.className}'
        if save:
            return f'save{self.module.entity.className}'
        return self.module.entity.className


class MultiTableParsing:

    @staticmethod
    def field_in_object(new_name, code_config: CodeConfig):
        """
        新的字段是否存在对象的字段种
        :param new_name: 新的字段名称
        :param code_config: 要比较的对象配置
        :return: True:是/False不是
        """
        if new_name == code_config.baseInfo.key.field:
            return True
        for field in code_config.baseInfo.attr:
            if new_name == field.field:
                return True
        return False

    @staticmethod
    def alias_replace(code_config: CodeConfig, replace: CodeConfig):
        """
        替换配置
        :param code_config: 原配置
        :param replace: 要替换的配置
        :return:
        """
        # 如果是表自身，更改表别名
        if replace.baseInfo.tableName == code_config.baseInfo.tableName:
            replace.baseInfo.aliasTable = f'{replace.baseInfo.tableName}_alias'

        # 检查主键是否重复
        if replace.baseInfo.key is not None:
            if MultiTableParsing.field_in_object(replace.baseInfo.key.field, code_config):
                replace.baseInfo.key.alias = f'{replace.baseInfo.tableName}_temp_{replace.baseInfo.key.field}'
        # 判断其他字段是否重复
        for field in replace.baseInfo.attr:
            if MultiTableParsing.field_in_object(field.field, code_config):
                field.alias = f'{replace.baseInfo.tableName}_temp_{field.field}'

    @staticmethod
    def parsing(code_config: CodeConfig):
        """
        多表解析，用于xml时的信息
        :param code_config:
        :return:
        """
        # 判断一对一重复
        for one_to_one in code_config.baseInfo.oneToOne:
            MultiTableParsing.alias_replace(code_config, one_to_one)
        # 判断一对多重复
        for one_to_many in code_config.baseInfo.oneToMany:
            # 如果是表自身，更改表别名
            MultiTableParsing.alias_replace(code_config, one_to_many)
        # 判断多对多重复
        for many_to_many in code_config.baseInfo.manyToMany:
            MultiTableParsing.alias_replace(code_config, many_to_many.many)
