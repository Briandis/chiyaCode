from src.constant.PublicConstant import Constant
from src.service.generate.generateAnalysis import FileType
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
        bean["baseEntity"]["path"] += f'.{lists[0]}'
        bean["path"] += f'.{lists[1]}'
        bean["serviceInterface"]["path"] += f'.{lists[2]}'
        bean["serviceImplements"]["path"] += f'.{lists[3]}'
        bean["baseMapperInterface"]["path"] += f'.{lists[4]}'
        bean["mapperInterface"]["path"] += f'.{lists[5]}'
        bean["baseMapperXml"]["path"] += f'.{lists[6]}'
        bean["mapperXml"]["path"] += f'.{lists[7]}'
        bean["controller"]["path"] += f'.{lists[8]}'

    @staticmethod
    def set_project_model(model: str, table_name: str, bean: dict):
        """
        生成模块
        :param model:模式
        :param table_name: 表名称
        :param bean: 配置信息
        :return:
        """
        l = ["entity", "entity", "service", "service.impl", "mapper", "mapper", "mapper", "mapper", "controller"]
        if model is None:
            ConditionalAssembly.set_model_value(bean, l)
            return

        if StringUtil.eq_not_case(model, "model"):
            # 表模块化
            suffix = table_name.replace("_", "").lower()
            l = [suffix, suffix, suffix, suffix, suffix, suffix, suffix, suffix, suffix]
        elif StringUtil.eq_not_case(model, "superModel"):
            # 表多级模块化
            suffix = table_name.replace("_", ".").lower()
            l = [suffix, suffix, suffix, suffix, suffix, suffix, suffix, suffix, suffix]
        elif StringUtil.eq_not_case(model, "XMLModel"):
            # 表多级模块化，XML独立
            suffix = table_name.replace("_", "").lower()
            l = [suffix, suffix, suffix, suffix, suffix, suffix, "xml", "xml", suffix]
        elif StringUtil.eq_not_case(model, "superXMLModel"):
            # 表多级模块化，XML独立
            suffix = table_name.replace("_", ".").lower()
            l = [suffix, suffix, suffix, suffix, suffix, suffix, "xml", "xml", suffix]
        elif StringUtil.eq_not_case(model, "mvcSuperModel"):
            # 表多级模块化，MVC模式
            suffix = table_name.replace("_", ".").lower()
            l = [
                f'{suffix}.entity', f'{suffix}.entity',
                f'{suffix}.service', f'{suffix}.service.impl',
                f'{suffix}.mapper', f'{suffix}.mapper',
                f'{suffix}.mapper', f'{suffix}.mapper',
                f'{suffix}.controller'
            ]
        elif StringUtil.eq_not_case(model, "mvcSuperXMLModel"):
            # 表多级模块化，MVC模式，XML独立
            suffix = table_name.replace("_", ".").lower()
            l = [
                f'{suffix}.entity', f'{suffix}.entity',
                f'{suffix}.service', f'{suffix}.service.impl',
                f'{suffix}.mapper', f'{suffix}.mapper',
                f'xml', f'xml',
                f'{suffix}.controller'
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
        bean["baseEntity"] = information_block(project, f'Base{className}', project)
        bean["serviceInterface"] = information_block(project, f'{className}Service', project)
        bean["serviceImplements"] = information_block(project, f'{className}ServiceImpl', project)
        bean["baseMapperInterface"] = information_block(project, f'Base{className}Mapper', project)
        bean["mapperInterface"] = information_block(project, f'{className}Mapper', project)
        bean["baseMapperXml"] = information_block(project, f'Base{className}Mapper', project)
        bean["mapperXml"] = information_block(project, f'{className}Mapper', project)
        bean["controller"] = information_block(project, f'{className}Controller', project)
        bean["Page"] = information_block("chiya.core.base.page", "Page", "chiya.core.base.page.Page")
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
                    FileType.entityBase, FileType.entity, FileType.service, FileType.serviceImpl,
                    FileType.javaBaseMapper, FileType.javaMapper,
                    FileType.xmlBaseMapper, FileType.xmlMapper,
                    FileType.controller,
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
        integrate_package(bean["baseEntity"])
        integrate_package(bean["serviceInterface"])
        integrate_package(bean["serviceImplements"])
        integrate_package(bean["baseMapperInterface"])
        integrate_package(bean["mapperInterface"])
        integrate_package(bean["baseMapperXml"])
        integrate_package(bean["mapperXml"])
        integrate_package(bean["controller"])

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
