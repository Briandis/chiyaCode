from src.util import StringUtil


class CreateFile:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config):
        data = '<?xml version="1.0" encoding="UTF-8"?>\n'
        data += '<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">\n'
        data += f'<mapper namespace="{config["mapperInterface"]["package"]}">\n'
        data += "\n"
        data += CreateMethod.create(config)
        data += "</mapper>\n"
        return data


class CreateSqlFragment:
    """
    创建resultMap块
    """

    @staticmethod
    def create(config: dict, tables):
        baseMapperXmlPackage = config["baseMapperXml"]["package"]
        string_block = ""
        for table in tables:
            string_block += f'\t<sql id="sql_filed_{table}"><include refid="{baseMapperXmlPackage}.sql_filed_{table}"/></sql>\n'
        string_block += "\n"
        return string_block


class CreateResultMap:
    """
    创建resultMap块
    """

    @staticmethod
    def create(config):
        lowClassName = StringUtil.first_char_lower_case(config["className"])
        className = config["className"]
        remark = config["remark"]
        method_str = ""
        key = config["key"]["attr"]
        upperKey = StringUtil.first_char_upper_case(key)
        keyType = config["key"]["type"]
        package = config["package"]
        resultMapName = config["config"]["xmlConfig"]["resultMapName"]
        baseMapperXmlPackage = config["baseMapperXml"]["package"]

        tag = "\t"
        data = ""
        data += f'{tag}<resultMap id="{resultMapName}{className}" type="{package}" extends="{baseMapperXmlPackage}.{resultMapName}{className}">\n'
        data += f'{tag}</resultMap>\n'
        obj_table = set()
        obj_table.add(f'{resultMapName}')

        if config.get("oneToOne"):
            for obj in config.get("oneToOne"):
                objClassName = obj["className"]
                objPackage = obj["package"]
                if f'{resultMapName}{className}OneToOne{objClassName}' not in obj_table:
                    data += f'{tag}<resultMap id="{resultMapName}{className}OneToOne{objClassName}" type="{package}" extends="{baseMapperXmlPackage}.{resultMapName}{className}OneToOne{objClassName}">\n'
                    data += f'{tag}</resultMap>\n'
                    obj_table.add(f'{resultMapName}{className}OneToOne{objClassName}')

                if f'{resultMapName}{objClassName}' not in obj_table:
                    data += f'{tag}<resultMap id="{resultMapName}{objClassName}" type="{objPackage}" extends="{baseMapperXmlPackage}.{resultMapName}{objClassName}">\n'
                    data += f'{tag}</resultMap>\n'
                    obj_table.add(f'{resultMapName}{objClassName}')

        if config.get("oneToMany"):
            for obj in config.get("oneToMany"):
                objClassName = obj["className"]
                objPackage = obj["package"]

                if f'{resultMapName}{className}OneToMany{objClassName}' not in obj_table:
                    data += f'{tag}<resultMap id="{resultMapName}{className}OneToMany{objClassName}" type="{package}" extends="{baseMapperXmlPackage}.{resultMapName}{className}OneToMany{objClassName}">\n'
                    data += f'{tag}</resultMap>\n'
                    obj_table.add(f'{resultMapName}{className}OneToMany{objClassName}')

                if f'{resultMapName}{objClassName}' not in obj_table:
                    data += f'{tag}<resultMap id="{resultMapName}{objClassName}" type="{objPackage}" extends="{baseMapperXmlPackage}.{resultMapName}{objClassName}">\n'
                    data += f'{tag}</resultMap>\n'
                    obj_table.add(f'{resultMapName}{objClassName}')

        if config.get("manyToMany"):
            for obj in config.get("manyToMany"):
                objClassName = obj["many"]["className"]
                objPackage = obj["many"]["package"]
                if f'{resultMapName}{className}ManyToMany{objClassName}' not in obj_table:
                    data += f'{tag}<resultMap id="{resultMapName}{className}ManyToMany{objClassName}" type="{package}" extends="{baseMapperXmlPackage}.{resultMapName}{className}ManyToMany{objClassName}">\n'
                    data += f'{tag}</resultMap>\n'
                    obj_table.add(f'{resultMapName}{className}ManyToMany{objClassName}')
                if f'{resultMapName}{objClassName}' not in obj_table:
                    data += f'{tag}<resultMap id="{resultMapName}{objClassName}" type="{objPackage}" extends="{baseMapperXmlPackage}.{resultMapName}{objClassName}">\n'
                    data += f'{tag}</resultMap>\n'
                    obj_table.add(f'{resultMapName}{objClassName}')
        data += "\n"
        return data


# 创建方法
class CreateMethod:
    """
    创建接口方法
    """

    @staticmethod
    def create(config: dict):
        data = ""
        data += CreateResultMap.create(config)
        return data


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
            "attr": XmlPretreatment.__attr_list(config),
            "className": config["className"],
            "path": config["path"],
            "foreignKey": config["foreignKey"]
        }

    @staticmethod
    def __check_res_filed_repeat(config: dict):
        resultMapName = config["config"]["xmlConfig"]["resultMapName"]
        # 封装临时数据，将所有属性变成列表形式
        tables = {
            config["tableName"]: {
                "attr": XmlPretreatment.__attr_list(config),
                "className": config["className"],
                "path": config["path"]
            }
        }
        one_to_one_list = []
        one_to_many_list = []
        many_to_many_list = []
        if config.get("oneToOne"):
            for obj in config.get("oneToOne"):
                tables[obj["tableName"]] = XmlPretreatment.__create_table(obj)
                one_to_one_list.append(obj["tableName"])

        if config.get("oneToMany"):
            for obj in config.get("oneToMany"):
                tables[obj["tableName"]] = XmlPretreatment.__create_table(obj)
                one_to_many_list.append(obj["tableName"])
        if config.get("manyToMany"):
            for obj in config.get("manyToMany"):
                if obj["many"]["tableName"] not in tables:
                    tables[obj["many"]["tableName"]] = XmlPretreatment.__create_table(obj["many"])
                    many_to_many_list.append(obj["many"]["tableName"])

        # 判断重复，只会在一对一，一对多，多对多的语句中出现，不会完全重复
        # 如果没有重复的，则直接跳过创建操作
        for table1 in tables:
            for attr1 in tables[table1]["attr"]:
                flag = False
                # 内循环
                for table2 in tables:
                    for attr2 in tables[table2]["attr"]:
                        if table1 != table2 and attr1["filed"] == attr2["filed"] and "filed_new" not in attr2:
                            flag = True
                            return_flag = False
                            # 是否在多表查询中用sql标签替换

                            attr2["fieldAlias"] = f'{table2}_temp_{attr2["filed"]}'
                if flag:
                    attr1["fieldAlias"] = f'{table1}_temp_{attr1["filed"]}'
