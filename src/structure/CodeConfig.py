from src.structure.CreateConfig import CreateConfig
from src.util import StringUtil


class Field:
    """
    字段属性
    """

    def __init__(self):
        # 数据库字段名称
        self.filed = None
        # 属性名称
        self.attr = None
        # 注释
        self.remark = None
        # 数据类型
        self.type = None

    @staticmethod
    def create_field(d: dict):
        """
        根据字段，生成对象
        :param d: 字段数据
        :return: 字段对象
        """
        field = Field()
        for i in field.__dict__:
            field.__setattr__(i, d.get(i))
        return field

    def set_field(self, d: dict):
        """

        :param d:
        :return:
        """
        for i in self.__dict__:
            self.__setattr__(i, d.get(i))

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


class ModuleInfo:
    """
    模块信息
    """

    def __init__(self, path: str = None, className: str = None, package: str = None):
        # 所在路径
        self.path = path
        # 类型名称
        self.className = className
        # 所在完整路径，包括自身
        self.package = package

    def set_field(self, d: dict):
        """

        :param d:
        :return:
        """
        for i in self.__dict__:
            self.__setattr__(i, d.get(i))

    def low_name(self):
        """
        获取小写的类名
        :return: 小写的类名
        """
        return StringUtil.first_char_lower_case(self.className)


class ModuleConfig:
    """
    模块配置
    """

    def __init__(self):
        # 分页信息
        self.Page = ModuleInfo()

        # 实体
        self.baseEntity = ModuleInfo()
        # 业务层
        self.serviceInterface = ModuleInfo()
        self.serviceImplements = ModuleInfo()
        # mapper层
        self.baseMapperInterface = ModuleInfo()
        self.mapperInterface = ModuleInfo()
        self.baseMapperXml = ModuleInfo()
        self.mapperXml = ModuleInfo()
        # 控制层
        self.controller = ModuleInfo()

        # 领域驱动设计相关
        # api接入层
        self.api = ModuleInfo()
        # 领域层
        self.domain = ModuleInfo()
        self.domainImpl = ModuleInfo()
        # 仓库层
        self.repository = ModuleInfo()
        self.repositoryImpl = ModuleInfo()
        # 缓存层
        self.cache = ModuleInfo()


class ManyToMany:

    def __init__(self):
        # 中间表
        self.to: CodeConfig = None
        # 另一方多的
        self.many: CodeConfig = None

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


class CodeConfig:
    """
    生成器依赖的配置实体
    """

    def __init__(self):
        # 表名称
        self.tableName: str = None
        # 备注
        self.remark: str = None
        # 类名
        self.className: str = None
        # 实体所在路径
        self.path: str = None
        # 实体所在完整路径，包括自身
        self.package: str = None

        # 主键信息
        self.key: Field = None
        # 其他字段
        self.attr: [Field] = []
        # 生成配置信息
        self.createConfig: CreateConfig = CreateConfig()
        # 模块配置信息
        self.module = ModuleConfig()
        # 一对一的配置
        self.oneToOne: [CodeConfig] = []
        # 一对多的配置
        self.oneToMany: [CodeConfig] = []
        # 多对多
        self.manyToMany: [ManyToMany] = []
        # 在多表关系中，充当的外键
        self.foreignKey = None

    def low_name(self):
        """
        获取小写的类名
        :return: 小写的类名
        """
        return StringUtil.first_char_lower_case(self.className)

    @staticmethod
    def get_code_config(config: dict):
        """
        根据配置字典，构造配置对象
        :param config:配置字典
        :return: 配置对象
        """

        code_config = CodeConfig()
        for i in code_config.__dict__:
            if code_config.__getattribute__(i) is None:
                code_config.__setattr__(i, config.get(i))
        # 主键数据处理
        code_config.key = Field.create_field(config.get("key"))
        for attr in config.get("attr"):
            code_config.attr.append(Field.create_field(attr))
        # 模块处理
        for module in config["module"]:
            code_config.module.__getattribute__(module).set_field(config["module"][module])
        # 生成配置处理
        for key in config["config"]:
            value = config["config"][key]
            base_config = code_config.createConfig.__getattribute__(key)
            base_config.set_field(value)
        # 一对一关系处理
        if "oneToOne" in config:
            for i in config["oneToOne"]:
                code_config.oneToOne.append(CodeConfig.get_code_config(i))
        # 一对多关系处理
        if "oneToMany" in config:
            for i in config["oneToMany"]:
                code_config.oneToMany.append(CodeConfig.get_code_config(i))
        # 多对多关系处理
        if "manyToMany" in config:
            for i in config["manyToMany"]:
                code_config.manyToMany.append(ManyToMany.get_many_to_many(i))
        return code_config
