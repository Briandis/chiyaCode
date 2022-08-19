from src.constant.PublicConstant import Constant
from src.structure.CreateConfig import FileType
from src.util import StringUtil
from src.util import JavaBaseObject


def information_block(path, className, package):
    """
    构建信息块
    :param path: 模块路径
    :param className: 类名
    :param package: 完整路径
    :return:
    """
    return {
        "path": path,
        "className": className,
        "package": package
    }


def integrate_package(bean):
    """
    整合bean中的[ackage
    :param bean:
    :return:
    """
    bean["package"] = f'{bean["path"]}.{bean["className"]}'


class ConditionalAssembly:
    """
    装配用户配置文件
    """

    @staticmethod
    def set_model_value(bean: dict, lists: list):
        """
        根据列表直接装配
        :param bean: 配置
        :param lists:路径集合
        """
        bean["module"]["baseEntity"]["path"] += f'.{lists[0]}'
        bean["path"] += f'.{lists[1]}'
        bean["module"]["serviceInterface"]["path"] += f'.{lists[2]}'
        bean["module"]["serviceImplements"]["path"] += f'.{lists[3]}'
        bean["module"]["baseMapperInterface"]["path"] += f'.{lists[4]}'
        bean["module"]["mapperInterface"]["path"] += f'.{lists[5]}'
        bean["module"]["baseMapperXml"]["path"] += f'.{lists[6]}'
        bean["module"]["mapperXml"]["path"] += f'.{lists[7]}'
        bean["module"]["controller"]["path"] += f'.{lists[8]}'
        # 领域驱动设计
        bean["module"]["api"]["path"] += f'.{lists[9]}'
        bean["module"]["domain"]["path"] += f'.{lists[10]}'
        bean["module"]["domainImpl"]["path"] += f'.{lists[11]}'
        bean["module"]["repository"]["path"] += f'.{lists[12]}'
        bean["module"]["repositoryImpl"]["path"] += f'.{lists[13]}'
        bean["module"]["cache"]["path"] += f'.{lists[14]}'

    @staticmethod
    def set_project_model(model: str, table_name: str, bean: dict):
        """
        生成模块
        :param model:模式
        :param table_name: 表名称
        :param bean: 配置信息
        :return:
        """
        l = ["entity", "entity",
             "service", "service.impl",
             "mapper", "mapper",
             "mapper", "mapper",
             "controller", "controller",
             "domain", "domain.impl",
             "repository", "repository.impl",
             "cache"
             ]
        if model is None:
            ConditionalAssembly.set_model_value(bean, l)
            return

        if StringUtil.eq_not_case(model, "model"):
            # 表模块化
            suffix = table_name.replace("_", "").lower()
            l = [suffix, suffix,  # 抽象实体、实体
                 suffix, suffix,  # 业务层、业务实现层
                 suffix, suffix,  # 抽象javaMapper、javaMapper
                 suffix, suffix,  # 抽象xmlMapper、xmlMapper
                 suffix, suffix,  # 控制层、RPC接入层
                 suffix, suffix,  # 领域层、领域层实现
                 suffix, suffix,  # 仓库层、仓库层实现
                 suffix, suffix,  # 缓存层
                 ]
        elif StringUtil.eq_not_case(model, "superModel"):
            # 表多级模块化
            suffix = table_name.replace("_", ".").lower()
            l = [suffix, suffix,  # 抽象实体、实体
                 suffix, suffix,  # 业务层、业务实现层
                 suffix, suffix,  # 抽象javaMapper、javaMapper
                 suffix, suffix,  # 抽象xmlMapper、xmlMapper
                 suffix, suffix,  # 控制层、RPC接入层
                 suffix, suffix,  # 领域层、领域层实现
                 suffix, suffix,  # 仓库层、仓库层实现
                 suffix, suffix,  # 缓存层
                 ]
        elif StringUtil.eq_not_case(model, "XMLModel"):
            # 表模块化,XML独立
            suffix = table_name.replace("_", "").lower()
            l = [suffix, suffix,  # 抽象实体、实体
                 suffix, suffix,  # 业务层、业务实现层
                 suffix, suffix,  # 抽象javaMapper、javaMapper
                 "xml", "xml",  # 抽象xmlMapper、xmlMapper
                 suffix, suffix,  # 控制层、RPC接入层
                 suffix, suffix,  # 领域层、领域层实现
                 suffix, suffix,  # 仓库层、仓库层实现
                 suffix, suffix,  # 缓存层
                 ]
        elif StringUtil.eq_not_case(model, "superXMLModel"):
            # 表多级模块化，XML独立
            suffix = table_name.replace("_", ".").lower()
            l = [suffix, suffix, suffix, suffix, suffix, suffix, "xml", "xml", suffix]
            l = [suffix, suffix,  # 抽象实体、实体
                 suffix, suffix,  # 业务层、业务实现层
                 suffix, suffix,  # 抽象javaMapper、javaMapper
                 "xml", "xml",  # 抽象xmlMapper、xmlMapper
                 suffix, suffix,  # 控制层、RPC接入层
                 suffix, suffix,  # 领域层、领域层实现
                 suffix, suffix,  # 仓库层、仓库层实现
                 suffix, suffix,  # 缓存层
                 ]
        elif StringUtil.eq_not_case(model, "mvcSuperModel"):
            # 表多级模块化，MVC模式
            suffix = table_name.replace("_", ".").lower()
            l = [
                f'{suffix}.entity', f'{suffix}.entity',  # 抽象实体、实体
                f'{suffix}.service', f'{suffix}.service.impl',  # 业务层、业务实现层
                f'{suffix}.mapper', f'{suffix}.mapper',  # 抽象javaMapper、javaMapper
                f'{suffix}.mapper', f'{suffix}.mapper',  # 抽象xmlMapper、xmlMapper
                f'{suffix}.controller', f'{suffix}.controller',  # 控制层、RPC接入层
                f'{suffix}.domain', f'{suffix}.domain.impl',  # 领域层、领域层实现
                f'{suffix}.repository', f'{suffix}.repository.impl',  # 仓库层、仓库层实现
                f'{suffix}.repository.cache'  # 缓存层
            ]
        elif StringUtil.eq_not_case(model, "mvcSuperXMLModel"):
            # 表多级模块化，MVC模式，XML独立
            suffix = table_name.replace("_", ".").lower()
            l = [
                f'{suffix}.entity', f'{suffix}.entity',  # 抽象实体、实体
                f'{suffix}.service', f'{suffix}.service.impl',  # 业务层、业务实现层
                f'{suffix}.mapper', f'{suffix}.mapper',  # 抽象javaMapper、javaMapper
                "xml", "xml",  # 抽象xmlMapper、xmlMapper
                f'{suffix}.controller', f'{suffix}.controller',  # 控制层、RPC接入层
                f'{suffix}.domain', f'{suffix}.domain.impl',  # 领域层、领域层实现
                f'{suffix}.repository', f'{suffix}.repository.impl',  # 仓库层、仓库层实现
                f'{suffix}.repository.cache'  # 缓存层
            ]
        elif StringUtil.eq_not_case(model, "ddd"):
            # 领域驱动设计
            suffix = table_name.replace("_", ".").lower()
            l = [
                f'{suffix}.entity', f'{suffix}.entity',  # 抽象实体、实体
                f'{suffix}.service', f'{suffix}.service',  # 业务层、业务实现层
                f'{suffix}.repository.mapper', f'{suffix}.repository.mapper',  # 抽象javaMapper、javaMapper
                f'{suffix}.repository.mapper', f'{suffix}.repository.mapper',  # 抽象xmlMapper、xmlMapper
                f'{suffix}.api', f'{suffix}.api',  # 控制层、RPC接入层
                f'{suffix}.domain', f'{suffix}.domain',  # 领域层、领域层实现
                f'{suffix}.repository', f'{suffix}.repository',  # 仓库层、仓库层实现
                f'{suffix}.repository.cache'  # 缓存层
            ]
        ConditionalAssembly.set_model_value(bean, l)

    @staticmethod
    def get_keyword_list(bean):
        """
        获取默认全部字符串
        :param bean: 配置
        :return: 是字符串的列表
        """
        lists = []
        for attr in bean["attr"]:
            if attr["type"] == JavaBaseObject.Constant.STRING:
                lists.append(attr["filed"])
        return lists

    @staticmethod
    def table_init(bean: dict, config):
        """
        信息初始化装配
        :param bean: 容器
        :param config: 配置
        """
        className = bean["className"]
        project = config[Constant.PROJECT]
        bean["utilPath"] = f'{project}.util'
        bean["path"] = project
        bean["package"] = project
        bean["module"] = {}
        bean["module"]["baseEntity"] = information_block(project, f'Base{className}', project)
        bean["module"]["serviceInterface"] = information_block(project, f'{className}Service', project)
        bean["module"]["serviceImplements"] = information_block(project, f'{className}ServiceImpl', project)
        bean["module"]["baseMapperInterface"] = information_block(project, f'Base{className}Mapper', project)
        bean["module"]["mapperInterface"] = information_block(project, f'{className}Mapper', project)
        bean["module"]["baseMapperXml"] = information_block(project, f'Base{className}Mapper', project)
        bean["module"]["mapperXml"] = information_block(project, f'{className}Mapper', project)
        bean["module"]["controller"] = information_block(project, f'{className}Controller', project)
        bean["module"]["Page"] = information_block("chiya.core.base.page", "Page", "chiya.core.base.page.Page")

        bean["module"]["api"] = information_block(project, f'{className}Api', project)
        bean["module"]["domain"] = information_block(project, f'{className}Domain', project)
        bean["module"]["domainImpl"] = information_block(project, f'{className}DomainImpl', project)
        bean["module"]["repository"] = information_block(project, f'{className}Repository', project)
        bean["module"]["repositoryImpl"] = information_block(project, f'{className}RepositoryImpl', project)
        bean["module"]["cache"] = information_block(project, f'{className}Cache', project)

        bean["config"] = {
            "fuzzySearch": {
                "name": "fuzzySearch",
                "enable": True,
                "value": "keyWord",
                "default": "keyWord",
                "data": ConditionalAssembly.get_keyword_list(bean),
            },
            "resultMap": {
                "name": "resultMap",
                "enable": True
            },
            "restful": {
                "name": "restful",
                "enable": True
            },
            "splicingSQL": {
                "name": "splicingSQL",
                "enable": True,
                "value": "splicingSQL",
                "default": "splicingSQL",
            },
            "extraAPI": {
                "name": "extraAPI",
                "enable": True,
                "value": "admin",
                "default": "admin",
            },
            "defaultAPI": {
                "name": "defaultAPI",
                "enable": True,
            },
            "falseDelete": {
                "name": "falseDelete",
                "enable": True,
                "deleteKey": "delete_flag",
                "default": "delete_flag",
                "deleteValue": 1,
                "isUpdate": True,
                "updateKey": "update_time"
            },
            "toJsonString": {
                "name": "toJsonString",
                "enable": True,
                "isFastJson": True
            },
            "chain": {
                "name": "chain",
                "enable": True,
            },
            "entityClone": {
                "name": "entityClone",
                "enable": False,
            },
            "methodName": {
                "name": "methodName",
                "enable": True,
                "value": "add,delete,update,getOne,list",
                "default": "add,delete,update,getOne,list",
            },
            "createFile": {
                "name": "createFile",
                "enable": True,
                "value": [FileType.entityBase, FileType.javaBaseMapper, FileType.xmlBaseMapper],
                "default": [
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
            },
            "notCreateFile": {
                "name": "notCreateFile",
                "enable": True,
                "value": [],
                "default": []
            },
            "xmlConfig": {
                "fieldAlias": "chiya",
                "resultMapName": "result"
            },

        }
        bean["entityClone"] = {
            "key": {},
            "attr": []
        }

    @staticmethod
    def set_model_package(bean: dict):
        """
        根据列表直接装配
        :param bean: 配置
        """
        integrate_package(bean)
        integrate_package(bean["module"]["baseEntity"])
        integrate_package(bean["module"]["serviceInterface"])
        integrate_package(bean["module"]["serviceImplements"])
        integrate_package(bean["module"]["baseMapperInterface"])
        integrate_package(bean["module"]["mapperInterface"])
        integrate_package(bean["module"]["baseMapperXml"])
        integrate_package(bean["module"]["mapperXml"])
        integrate_package(bean["module"]["controller"])

        integrate_package(bean["module"]["api"])
        integrate_package(bean["module"]["domain"])
        integrate_package(bean["module"]["domainImpl"])
        integrate_package(bean["module"]["repository"])
        integrate_package(bean["module"]["repositoryImpl"])
        integrate_package(bean["module"]["cache"])

    @staticmethod
    def assembly(tables: dict, config: dict):
        """
        初始化配置，并且装配用户自定义配置
        :param tables: 全部的表
        :param config: 用户自定义配置
        """
        for table in tables:
            # 初始化配置
            ConditionalAssembly.table_init(tables[table], config)
            # 模糊搜索
            if config.get("fuzzySearch"):
                if config.get("fuzzySearchList") and config["fuzzySearchList"].get(table):
                    tables[table]["config"]["fuzzySearch"]["data"] = config["fuzzySearchList"].get(table)
            else:
                tables[table]["config"]["fuzzySearch"]["enable"] = True
            if len(tables[table]["config"]["fuzzySearch"]["data"]) == 0:
                tables[table]["config"]["fuzzySearch"]["enable"] = False
            # 生成模式
            ConditionalAssembly.set_project_model(config.get(Constant.CREATE_MODEL), table, tables[table])
            # 设置包
            ConditionalAssembly.set_model_package(tables[table])
            # 装配配置
            # 额外接口
            if Constant.EXTRA_API in config:
                tables[table]["config"]["extraAPI"]["enable"] = config.get(Constant.EXTRA_API)
            # 额外的名称
            if Constant.EXTRA_API_NAME in config:
                tables[table]["config"]["extraAPI"]["value"] = config.get(Constant.EXTRA_API_NAME)
            # 默认接口
            if Constant.DEFAULT_API in config:
                tables[table]["config"]["defaultAPI"]["enable"] = config.get(Constant.DEFAULT_API)
            # 生成的文件
            if Constant.CREATE_FILE in config:
                tables[table]["config"]["createFile"]["value"] = config.get(Constant.CREATE_FILE)
            # 不生成的文件
            if Constant.NOT_CREATE_FILE in config:
                tables[table]["config"]["notCreateFile"]["value"] = config.get(Constant.NOT_CREATE_FILE)
            # 假删配置
            deleteKey = False
            updateKey = False
            for attr in tables[table]["attr"]:
                if tables[table]["config"]["falseDelete"]["deleteKey"] in attr["filed"]:
                    deleteKey = True
                    tables[table]["config"]["falseDelete"]["deleteKey"] = attr["filed"]
                if tables[table]["config"]["falseDelete"]["updateKey"] in attr["filed"]:
                    updateKey = True
                    tables[table]["config"]["falseDelete"]["updateKey"] = attr["filed"]
            tables[table]["config"]["falseDelete"]["enable"] = deleteKey
            tables[table]["config"]["falseDelete"]["isUpdate"] = updateKey
