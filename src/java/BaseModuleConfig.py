from src.util.chiyaUtil import StringUtil


class FileType:
    controller = "Controller"
    """ web控制层 """
    service = "Service"
    """ 业务层接口 """
    serviceImpl = "ServiceImpl"
    """ 业务层实现 """
    javaMapper = "JavaMapper"
    """ mapper接口 """
    javaBaseMapper = "JavaBaseMapper"
    """ mapper层抽象接口 """
    xmlMapper = "XmlMapper"
    """ mapper接口的xml """
    xmlBaseMapper = "XmlBaseMapper"
    """ mapper抽象接口的xml """
    entity = "Entity"
    """ 实体 """
    entityBase = "EntityBase"
    """ 抽象基础实体 """

    api = "API"
    """ rpc对外服务层 """
    domain = "Domain"
    """ 领域接口 """
    domainImpl = "DomainImpl"
    """ 领域实现 """
    cache = "Cache"
    """ 缓存层 """
    repository = "Repository"
    """ 仓库接口 """
    repositoryImpl = "RepositoryImpl"
    """ 仓库实现 """


# 配置基类
class BaseConfig:
    """
    通用基础配置
    """

    def __init__(self, enable: bool = True):
        """
        初始化类
        :param enable: 改配置默认是否启用
        """
        # 配置名称
        # self.name = None
        # 配置是否启用
        self.enable = enable
        # 传入的值
        self.value = None

    def set_field(self, d: dict):
        """
        根据字段反射字典装配数据
        :param d:字典
        """
        for i in self.__dict__:
            # 不允许覆盖默认值
            if i != "default":
                self.__setattr__(i, d.get(i))

    def get_value(self):
        """
        获取value
        :return: value,或者默认值
        """
        if self.value is not None:
            return self.value
        return self.__dict__.get("default")


# 模糊搜索配置
class FuzzySearch(BaseConfig):
    """
    模糊搜索配置
    """

    def __init__(self):
        super().__init__()
        # 模糊搜索的字段，与属性中的值一致
        self.data: [str] = None
        # 默认的值，在value无效时使用
        self.default = "keyWord"


# resultMap替换resultType
class ResultMap(BaseConfig):
    """
    resultMap替换resultType
    """

    def __init__(self):
        super().__init__()


# restful风格API
class Restful(BaseConfig):
    """
    restful风格API
    """

    def __init__(self):
        super().__init__()


# sql语句预留
class SplicingSQL(BaseConfig):
    """
    sql语句预留
    """

    def __init__(self):
        super().__init__()
        # 默认的值，在value无效时使用
        self.default = "splicingSQL"


# 额外的web-API
class ExtraAPI(BaseConfig):
    """
    额外的web-API
    """

    def __init__(self):
        super().__init__(False)
        # 默认的值，在value无效时使用
        self.default = "admin"


# 默认的web-api
class DefaultAPI(BaseConfig):
    """
    默认的web-api
    """

    def __init__(self):
        super().__init__()


# 重写toString方法
class ToJsonString(BaseConfig):
    """
    重写toString方法
    """

    def __init__(self):
        super().__init__()
        # 默认使用FAST JSON
        self.isFastJson = True


# 实体生成链式操作方法
class Chain(BaseConfig):
    """
    实体生成链式操作方法
    """

    def __init__(self):
        super().__init__()


# 本配置是基于某个实体进行的克隆
class EntityClone(BaseConfig):
    """
    本配置是基于某个实体进行的克隆
    """

    def __init__(self):
        # 默认为不启用
        super().__init__(False)


# 默认生成的增删改查前缀
class MethodName(BaseConfig):
    """
    默认生成的接口前缀
    """

    def __init__(self):
        # 默认为不启用
        super().__init__(False)
        # 默认的值，在value无效时使用
        self.default = "add,delete,update,getOne,list"

    def get(self, index: int):
        """
        获取选择的那个方法的前缀
        :param index: 对应下标
        :return: 前缀名称
        """
        if self.value is None:
            return self.default.split(",")[index]
        else:
            return self.value.split(",")[index]

    def get_upper(self, index: int):
        """
        获取大写的前缀
        :param index:对应下标
        :return: 大写的前缀
        """
        return StringUtil.first_char_upper_case(self.get(index))


# 该配置要生成的文件
class CreateFile(BaseConfig):
    """
    该配置要生成的文件
    """

    def __init__(self):
        # 默认为不启用
        super().__init__(False)
        # 默认的值，在value无效时使用
        self.default = [
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


# 不生成的文件
class NotCreateFile(BaseConfig):
    """
    不生成的文件
    """

    def __init__(self):
        # 默认为不启用
        super().__init__(False)
        # 默认的值，在value无效时使用
        self.default = []


# xml中字段别名配置
class XmlConfig(BaseConfig):
    """
    xml中字段别名配置
    """

    def __init__(self):
        # 默认为不启用
        super().__init__(False)
        # 默认的值，在value无效时使用
        self.default = []
        # 字段别名
        self.fieldAlias = "chiya"
        # 响应类型别名
        self.resultMapName = "result"


# 控制层中，是否使用权限
class ChiyaSecurity(BaseConfig):
    """
    是否在控制层中生成接口权限
    """

    def __init__(self):
        super().__init__()


# 仓库层中，是否使用缓存
class RepositoryUseCache(BaseConfig):
    """
    仓库层实现中，是否使用缓存
    """

    def __init__(self):
        super().__init__()


# 在表名前加入数据库名称
class DatabaseName(BaseConfig):
    """
    查询的语句中，指定统一的数据库名
    """

    def __init__(self):
        super().__init__(False)


class CodeTemplateFlow(BaseConfig):
    """
    模板生成流
    """

    def __init__(self):
        super().__init__()
        # 默认的模板流，基于DDD
        self.default = {
            "controller": "service",
            "service": "domain",
            "domain": "repository",
            "repository": "mapper"
        }


class CreateConfig:
    """
    构建的配置文件
    """

    def __init__(self):
        self.fuzzySearch = FuzzySearch()
        """ 模糊搜索配置 """
        self.resultMap = ResultMap()
        """ resultMap替换resultType """
        self.restful = Restful()
        """ restful风格API """
        self.splicingSQL = SplicingSQL()
        """ sql语句预留 """
        self.defaultAPI = DefaultAPI()
        """ 默认的api """
        self.extraAPI = ExtraAPI()
        """ 额外的API """
        self.toJsonString = ToJsonString()
        """ 是否在实体中生成toString方法 """
        self.chain = Chain()
        """ 实体生成链式操作方法 """
        self.entityClone = EntityClone()
        """ 本配置是基于某个实体进行的克隆 """
        self.methodName = MethodName()
        """ 默认生成的接口前缀 """
        self.createFile = CreateFile()
        """ 该配置要生成的文件 """
        self.notCreateFile = NotCreateFile()
        """ 不生成的文件 """
        self.xmlConfig = XmlConfig()
        """ xml配置 """
        self.chiyaSecurity = ChiyaSecurity()
        """ 是否生成接口权限 """
        self.repositoryUseCache = RepositoryUseCache()
        """ 仓库层实现，是否使用缓存 """
        self.databaseName = DatabaseName()
        """ 在xml中所有的表操作加入数据库名 """
        self.codeTemplateFlow = CodeTemplateFlow()
        """ 代码模板流 """
