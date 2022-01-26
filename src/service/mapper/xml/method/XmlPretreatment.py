from src.constant.ProtocolConstant import JsonKey
from src.util import StringUtil
import copy


class XmlPretreatment:
    """
    config预处理
    """

    @staticmethod
    def __attr_list(config: dict) -> list:
        """
        将key和attr转换成list
        :param config: 配置对象
        :return: list 属性参数列表
        """
        lists = [config["key"].copy()]
        for i in config["attr"]:
            lists.append(i.copy())
        return lists

    @staticmethod
    def __create_table(config: dict):
        return {
            JsonKey.attr.self: XmlPretreatment.__attr_list(config),
            JsonKey.className: config[JsonKey.className],
            JsonKey.path: config[JsonKey.path],
            JsonKey.foreignKey: config[JsonKey.foreignKey],
            JsonKey.package: config[JsonKey.package]
        }

    @staticmethod
    def pretreatment(config: dict):
        className = config["className"]
        lowClassName = StringUtil.first_char_lower_case(className)
        remark = config["remark"]
        key = config["key"]["attr"]
        upperKey = StringUtil.first_char_upper_case(key)
        keyType = config["key"]["type"]
        package = config["package"]
        resultMapName = config["config"]["xmlConfig"]["resultMapName"]
        baseMapperXmlPackage = config["baseMapperXml"]["package"]
        tableName = config["tableName"]
        path = config["path"]

        # 封装临时数据，将所有属性变成列表形式
        tables = {
            config["tableName"]: {
                JsonKey.attr.self: XmlPretreatment.__attr_list(config),
                JsonKey.className: className,
                JsonKey.path: path,
                JsonKey.package: config[JsonKey.package]
            }
        }
        table_my = False
        one_to_one_list = []
        one_to_many_list = []
        many_to_many_list = []
        # 如果遇到同名表，则开启特殊模式
        one_to_one_dict = {}
        one_to_many_dict = {}
        many_to_many_dict = {}
        if config.get("oneToOne"):
            for obj in config.get("oneToOne"):
                tables[obj["tableName"]] = XmlPretreatment.__create_table(obj)
                one_to_one_list.append(obj["tableName"])
                one_to_one_dict[obj["tableName"]] = XmlPretreatment.__create_table(obj)
                if obj["tableName"] == tableName:
                    table_my = True

        if config.get("oneToMany"):
            for obj in config.get("oneToMany"):
                tables[obj["tableName"]] = XmlPretreatment.__create_table(obj)
                one_to_many_list.append(obj["tableName"])
                one_to_many_dict[obj["tableName"]] = XmlPretreatment.__create_table(obj)
                if obj["tableName"] == tableName:
                    table_my = True
        # 此处装配的多对多会出现一种情况，多对多的一方属于自身，则需要启用sql替换策略
        if config.get("manyToMany"):
            for obj in config.get("manyToMany"):
                if obj["many"]["tableName"] not in tables:
                    tables[obj["many"]["tableName"]] = XmlPretreatment.__create_table(obj["many"])
                    # 此处会出现在字典中，本表面和多的一方是同一张表，则导致本表被覆盖
                    many_to_many_list.append(obj["many"]["tableName"])
                    many_to_many_dict[obj["many"]["tableName"]] = XmlPretreatment.__create_table(obj["many"])
                    if obj["many"]["tableName"] == tableName:
                        table_my = True

        # 重复判断，如果没有重复则直接返回空，没必要生成
        # 重写碰撞逻辑
        # 查询原则，只查询具有一对一、一对多、多对多关联的表
        # 一对一 存在自己关联自己的情况 单链表结构
        # 一对多 存在自己关联自己的情况 父子结构
        # 多对多 存在自己关联自己的情况 图状结构
        # 收集全部字段、判断碰撞，如果碰撞为自己，则有专门的解决自身碰撞情况
        # 碰撞后替换的数据，应该同步到，各个字典中
        for table1 in tables:
            for attr1 in tables[table1]["attr"]:
                flag = False
                # 内循环
                for table2 in tables:
                    for attr2 in tables[table2]["attr"]:
                        # 此处会在本表和多的一方也为本表的情况下，无法建立替换
                        if table1 != table2 and attr1["filed"] == attr2["filed"] and "fieldAlias" not in attr2:
                            flag = True
                            attr2["fieldAlias"] = f'{table2}_temp_{attr2["filed"]}'
                if flag:
                    attr1["fieldAlias"] = f'{table1}_temp_{attr1["filed"]}'
        resTable = copy.deepcopy(tables)
        # 只有return_flag为真的情况下，才会在结尾出添加只字符串
        # 将替换后的数据存入次，方便查找替换的字段
        bean_info = {
            "resultMapName": f'{resultMapName}{className}',
            "oneToMany": [],
            "oneToOne": [],
            "manyToMany": [],
            # 装配默认自身数据
            # 在多对多中，如果映射自身，则必须启动替换，但是映射表是自己，则不会装配默认信息，需要在再次申明
            "path": path,
            # "attr": copy.deepcopy(config["attr"]),
            # "key": copy.deepcopy(config["key"]),
            "className": className,
            "tableName": tableName,
            "package": package,
            "config": copy.deepcopy(config["config"])
        }
        for table in tables:

            # 提取主键并从中移除
            obj = {"key": tables[table]["attr"][0]}
            del tables[table]["attr"][0]
            if table == tableName:
                bean_info["key"] = obj["key"]

            obj["attr"] = tables[table]["attr"]
            obj["className"] = tables[table]["className"]
            obj["path"] = tables[table]["path"]
            obj["tableName"] = table
            obj[JsonKey.path] = tables[table][JsonKey.path]
            obj[JsonKey.package] = tables[table][JsonKey.package]
            if table == tableName:
                bean_info["attr"] = obj["attr"]
            # 按照关系进行装配，只有出现在MN关系中，才会添加进去

            if table in one_to_one_list:
                obj["foreignKey"] = one_to_one_dict[table]["foreignKey"]
                for ct in config.get(JsonKey.oneToOne):
                    if ct[JsonKey.tableName] == table:
                        obj[JsonKey.config.self] = ct[JsonKey.config.self]

                bean_info["oneToOne"].append(obj)
            if table in one_to_many_list:
                obj["foreignKey"] = one_to_many_dict[table]["foreignKey"]
                for ct in config.get(JsonKey.oneToMany):
                    if ct[JsonKey.tableName] == table:
                        obj["config"] = ct[JsonKey.config.self]
                bean_info["oneToMany"].append(obj)
            # if table in many_to_many_list:
            #     obj["foreignKey"] = many_to_many_dict[table]["foreignKey"]
            #     for ct in config.get(JsonKey.manyToMany):
            #         if ct["many"][JsonKey.tableName] == table:
            #             obj["config"] = ct["many"][JsonKey.config.self]
            #     bean_info["manyToMany"].append({"many": obj})
        bean_info["manyToMany"] = copy.deepcopy(config.get("manyToMany"))
        return bean_info, resTable, table_my
