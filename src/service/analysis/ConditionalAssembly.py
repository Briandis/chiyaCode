from src.constant.ProtocolConstant import JsonKey
from src.constant.PublicConstant import Constant
from src.service.generate.generateAnalysis import FileType
from src.util import StringUtil
from src.util import JavaBaseObject


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
        bean[JsonKey.baseEntity.self][JsonKey.baseEntity.path] += f'.{lists[0]}'
        bean[JsonKey.path] += f'.{lists[1]}'
        bean[JsonKey.serviceInterface.self][JsonKey.serviceInterface.path] += f'.{lists[2]}'
        bean[JsonKey.serviceImplements.self][JsonKey.serviceImplements.path] += f'.{lists[3]}'
        bean[JsonKey.baseMapperInterface.self][JsonKey.baseMapperInterface.path] += f'.{lists[4]}'
        bean[JsonKey.mapperInterface.self][JsonKey.mapperInterface.path] += f'.{lists[5]}'
        bean[JsonKey.baseMapperXml.self][JsonKey.baseMapperXml.path] += f'.{lists[6]}'
        bean[JsonKey.mapperXml.self][JsonKey.mapperXml.path] += f'.{lists[7]}'
        bean[JsonKey.controller.self][JsonKey.controller.path] += f'.{lists[8]}'

    @staticmethod
    def set_project_model(model: str, table_name: str, bean: dict):
        """
        生成模块
        :param model:模式
        :param table_name: 表名称
        :param bean: 配置信息
        :return:
        """
        if model is None:
            l = ["entity", "entity", "service", "service.impl", "mapper", "mapper", "mapper", "mapper", "controller"]
            ConditionalAssembly.set_model_value(bean, l)
            return

        if StringUtil.eq_not_case(model, "model"):
            # 表模块化
            suffix = table_name.replace("_", "").lower()
            l = [suffix, suffix, suffix, suffix, suffix, suffix, suffix, suffix, suffix]
            ConditionalAssembly.set_model_value(bean, l)
        elif StringUtil.eq_not_case(model, "superModel"):
            # 表多级模块化
            suffix = table_name.replace("_", ".").lower()
            l = [suffix, suffix, suffix, suffix, suffix, suffix, suffix, suffix, suffix]
            ConditionalAssembly.set_model_value(bean, l)
        elif StringUtil.eq_not_case(model, "XMLModel"):
            # 表多级模块化，XML独立
            suffix = table_name.replace("_", "").lower()
            l = [suffix, suffix, suffix, suffix, suffix, suffix, "xml", "xml", suffix]
            ConditionalAssembly.set_model_value(bean, l)
        elif StringUtil.eq_not_case(model, "superXMLModel"):
            # 表多级模块化，XML独立
            suffix = table_name.replace("_", ".").lower()
            l = [suffix, suffix, suffix, suffix, suffix, suffix, "xml", "xml", suffix]
            ConditionalAssembly.set_model_value(bean, l)
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
            ConditionalAssembly.set_model_value(bean, l)
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
        else:
            l = ["entity", "entity", "service", "service.impl", "mapper", "mapper", "mapper", "mapper", "controller"]
            ConditionalAssembly.set_model_value(bean, l)

    @staticmethod
    def get_keyword_list(bean):
        """
        获取默认全部字符串
        :param bean: 配置
        :return: 是字符串的列表
        """
        lists = []
        for attr in bean[JsonKey.attr.self]:
            if attr[JsonKey.attr.type] == JavaBaseObject.Constant.STRING:
                lists.append(attr[JsonKey.attr.filed])
        return lists

    @staticmethod
    def table_init(bean: dict, config):
        """
        信息初始化装配
        :param bean: 容器
        :param config: 配置
        """
        className = bean[JsonKey.className]
        project = config[Constant.PROJECT]
        bean[JsonKey.utilPath] = f'{project}.util'
        bean[JsonKey.path] = project
        bean[JsonKey.package] = project
        bean[JsonKey.baseEntity.self] = {
            JsonKey.baseEntity.path: project,
            JsonKey.baseEntity.className: f'Base{className}',
            JsonKey.baseEntity.package: project}
        bean[JsonKey.serviceInterface.self] = {
            JsonKey.serviceInterface.path: project,
            JsonKey.serviceInterface.className: f'{className}Service',
            JsonKey.serviceInterface.package: project}
        bean[JsonKey.serviceImplements.self] = {
            JsonKey.serviceImplements.path: project,
            JsonKey.serviceImplements.className: f'{className}ServiceImpl',
            JsonKey.serviceImplements.package: project}
        bean[JsonKey.baseMapperInterface.self] = {
            JsonKey.baseMapperInterface.path: project,
            JsonKey.baseMapperInterface.className: f'Base{className}Mapper',
            JsonKey.baseMapperInterface.package: project}
        bean[JsonKey.mapperInterface.self] = {
            JsonKey.mapperInterface.path: project,
            JsonKey.mapperInterface.className: f'{className}Mapper',
            JsonKey.mapperInterface.package: project}
        bean[JsonKey.baseMapperXml.self] = {
            JsonKey.baseMapperXml.path: project,
            JsonKey.baseMapperXml.className: f'Base{className}Mapper',
            JsonKey.baseMapperXml.package: project}
        bean[JsonKey.mapperXml.self] = {
            JsonKey.mapperXml.path: project,
            JsonKey.mapperXml.className: f'{className}Mapper',
            JsonKey.mapperXml.package: project}
        bean[JsonKey.controller.self] = {
            JsonKey.controller.path: project,
            JsonKey.controller.className: f'{className}Controller',
            JsonKey.controller.package: project}
        bean[JsonKey.Page.self] = {
            JsonKey.Page.path: "chiya.core.base.page",
            JsonKey.Page.className: "Page",
            JsonKey.Page.package: "chiya.core.base.page.Page"}
        bean[JsonKey.config.self] = {
            JsonKey.config.fuzzySearch.self: {
                JsonKey.config.fuzzySearch.name: JsonKey.config.fuzzySearch.self,
                JsonKey.config.fuzzySearch.enable: True,
                JsonKey.config.fuzzySearch.value: "keyWord",
                JsonKey.config.fuzzySearch.default: "keyWord",
                JsonKey.config.fuzzySearch.data: ConditionalAssembly.get_keyword_list(bean),
            },
            JsonKey.config.resultMap.self: {
                JsonKey.config.resultMap.name: JsonKey.config.resultMap.self,
                JsonKey.config.resultMap.enable: True
            },
            JsonKey.config.restful.self: {
                JsonKey.config.restful.name: JsonKey.config.restful.self,
                JsonKey.config.restful.enable: True
            },
            JsonKey.config.splicingSQL.self: {
                JsonKey.config.splicingSQL.name: JsonKey.config.splicingSQL.self,
                JsonKey.config.splicingSQL.enable: True,
                JsonKey.config.splicingSQL.value: "splicingSQL",
                JsonKey.config.splicingSQL.default: "splicingSQL",
            },
            JsonKey.config.extraAPI.self: {
                JsonKey.config.extraAPI.name: JsonKey.config.extraAPI.self,
                JsonKey.config.extraAPI.enable: True,
                JsonKey.config.extraAPI.value: "admin",
                JsonKey.config.extraAPI.default: "admin",
            },
            JsonKey.config.defaultAPI.self: {
                JsonKey.config.defaultAPI.name: JsonKey.config.defaultAPI.self,
                JsonKey.config.defaultAPI.enable: True,
            },
            JsonKey.config.falseDelete.self: {
                JsonKey.config.falseDelete.name: JsonKey.config.falseDelete.self,
                JsonKey.config.falseDelete.enable: True,
                JsonKey.config.falseDelete.deleteKey: "delete_flag",
                JsonKey.config.falseDelete.default: "delete_flag",
                JsonKey.config.falseDelete.deleteValue: 1,
                JsonKey.config.falseDelete.isUpdate: True,
                JsonKey.config.falseDelete.updateKey: "update_time"
            },
            JsonKey.config.toJsonString.self: {
                JsonKey.config.toJsonString.name: JsonKey.config.toJsonString.self,
                JsonKey.config.toJsonString.enable: True,
                JsonKey.config.toJsonString.isFastJson: True
            },
            JsonKey.config.chain.self: {
                JsonKey.config.chain.name: JsonKey.config.chain.self,
                JsonKey.config.chain.enable: True,
            },
            JsonKey.config.entityClone.self: {
                JsonKey.config.entityClone.name: JsonKey.config.entityClone.self,
                JsonKey.config.entityClone.enable: False,
            },
            JsonKey.config.methodName.self: {
                JsonKey.config.methodName.name: JsonKey.config.methodName.self,
                JsonKey.config.methodName.enable: True,
                JsonKey.config.methodName.value: "add,delete,update,getOne,list",
                JsonKey.config.methodName.default: "add,delete,update,getOne,list",
            },
            JsonKey.config.createFile.self: {
                JsonKey.config.createFile.name: JsonKey.config.createFile.self,
                JsonKey.config.createFile.enable: True,
                JsonKey.config.createFile.value: [FileType.entityBase, FileType.javaBaseMapper, FileType.xmlBaseMapper],
                JsonKey.config.createFile.default: [
                    FileType.entityBase, FileType.entity, FileType.service, FileType.serviceImpl,
                    FileType.javaBaseMapper, FileType.javaMapper,
                    FileType.xmlBaseMapper, FileType.xmlMapper,
                    FileType.controller,
                ]
            },
            JsonKey.config.notCreateFile.self: {
                JsonKey.config.notCreateFile.name: JsonKey.config.notCreateFile.self,
                JsonKey.config.notCreateFile.enable: True,
                JsonKey.config.notCreateFile.value: [],
                JsonKey.config.notCreateFile.default: []
            },
            JsonKey.config.xmlConfig.self: {
                JsonKey.config.xmlConfig.fieldAlias: "chiya",
                JsonKey.config.xmlConfig.resultMapName: "result"
            },

        }
        bean[JsonKey.entityClone.self] = {
            JsonKey.entityClone.key.self: {},
            JsonKey.entityClone.attr.self: []
        }

    @staticmethod
    def set_model_package(bean: dict):
        """
        根据列表直接装配
        :param bean: 配置
        """
        bean[JsonKey.baseEntity.self][JsonKey.baseEntity.package] = \
            bean[JsonKey.baseEntity.self][JsonKey.baseEntity.path] + "." + bean[JsonKey.baseEntity.self][JsonKey.baseEntity.className]
        bean[JsonKey.package] = \
            bean[JsonKey.path] + "." + bean[JsonKey.className]
        bean[JsonKey.serviceInterface.self][JsonKey.serviceInterface.package] = \
            bean[JsonKey.serviceInterface.self][JsonKey.serviceInterface.path] + "." + bean[JsonKey.serviceInterface.self][JsonKey.serviceInterface.className]
        bean[JsonKey.serviceImplements.self][JsonKey.serviceImplements.package] = \
            bean[JsonKey.serviceImplements.self][JsonKey.serviceImplements.path] + "." + bean[JsonKey.serviceImplements.self][JsonKey.serviceImplements.className]
        bean[JsonKey.baseMapperInterface.self][JsonKey.baseMapperInterface.package] = \
            bean[JsonKey.baseMapperInterface.self][JsonKey.baseMapperInterface.path] + "." + bean[JsonKey.baseMapperInterface.self][JsonKey.baseMapperInterface.className]
        bean[JsonKey.mapperInterface.self][JsonKey.mapperInterface.package] = \
            bean[JsonKey.mapperInterface.self][JsonKey.mapperInterface.path] + "." + bean[JsonKey.mapperInterface.self][JsonKey.mapperInterface.className]
        bean[JsonKey.baseMapperXml.self][JsonKey.baseMapperXml.package] = \
            bean[JsonKey.baseMapperXml.self][JsonKey.baseMapperXml.path] + "." + bean[JsonKey.baseMapperXml.self][JsonKey.baseMapperXml.className]
        bean[JsonKey.mapperXml.self][JsonKey.mapperXml.package] = \
            bean[JsonKey.mapperXml.self][JsonKey.mapperXml.path] + "." + bean[JsonKey.mapperXml.self][JsonKey.mapperXml.className]
        bean[JsonKey.controller.self][JsonKey.controller.package] = \
            bean[JsonKey.controller.self][JsonKey.controller.path] + "." + bean[JsonKey.controller.self][JsonKey.controller.className]

    @staticmethod
    def assembly(tables: dict, config: dict):
        for table in tables:
            ConditionalAssembly.table_init(tables[table], config)
            if config.get("fuzzySearch"):
                if config.get("fuzzySearchList") and config["fuzzySearchList"].get(table):
                    tables[table][JsonKey.config.self][JsonKey.config.fuzzySearch.self][JsonKey.config.fuzzySearch.data] = config["fuzzySearchList"].get(table)
            else:
                tables[table][JsonKey.config.self][JsonKey.config.fuzzySearch.self][JsonKey.config.fuzzySearch.enable] = False
            if len(tables[table][JsonKey.config.self][JsonKey.config.fuzzySearch.self][JsonKey.config.fuzzySearch.data]) == 0:
                tables[table][JsonKey.config.self][JsonKey.config.fuzzySearch.self][JsonKey.config.fuzzySearch.enable] = False
            ConditionalAssembly.set_project_model(config.get(Constant.CREATE_MODEL), table, tables[table])
            ConditionalAssembly.set_model_package(tables[table])
