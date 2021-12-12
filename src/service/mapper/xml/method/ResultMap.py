from src.util import StringUtil


class CreateResultMap:
    """
    创建resultMap块
    """

    # 创建result完整块
    @staticmethod
    def create_result(config: dict, indent: int, alias=True):
        """
        创建result完整块
        :param config: 配置文件
        :param indent: 缩进
        :param alias: 开启别名替换
        :return: 完整块
        """
        tag = "\t" * indent
        data = ""
        data += CreateResultMap.__create_result_id(config["key"], indent, alias)
        data += CreateResultMap.__create_result_column(config["attr"], indent, alias)
        return data

    # 创建result id块
    @staticmethod
    def __create_result_id(key: dict, indent: int, alias=True) -> str:
        """
        创建result id块
        :param key: 主键配置
        :param indent:  缩进范围
        :param alias: 开启别名替换
        :return: <id column="user_id" property="userId"/>形式的字符串
        """
        tag = "\t" * indent
        if "fieldAlias" in key and alias:
            data = f'{tag}<id column="{key["fieldAlias"]}" property="{key["attr"]}"/>\n'
        else:
            data = f'{tag}<id column="{key["filed"]}" property="{key["attr"]}"/>\n'
        return data

    # 生成 result 字段块
    @staticmethod
    def __create_result_column(attrs: list, indent: int, alias=True) -> str:
        """
        生成 result 字段块
        :param attrs:  属性列表
        :param indent: 缩进范围
        :param alias: 开启别名替换
        :return: <result column="user_id" property="userId"/>形式的字符串
        """
        tag = "\t" * indent
        data = ""
        for attr in attrs:
            if "fieldAlias" in attr and alias:
                data += f'{tag}<result column="{attr["fieldAlias"]}" property="{attr["attr"]}"/>\n'
            else:
                data += f'{tag}<result column="{attr["filed"]}" property="{attr["attr"]}"/>\n'
        return data

    # 生成 result 一对一块
    @staticmethod
    def create_result_association(obj: dict, indent: int) -> str:
        """
        生成一对一块
        :param obj: 配置对象
        :param indent: 缩进
        :return: 一对一块
        """
        tag = '\t' * indent
        className = obj["className"]
        lowClassName = StringUtil.first_char_lower_case(className)
        data = ""
        data += f'{tag}<association property="{lowClassName}" javaType="{obj["package"]}">\n'
        data += CreateResultMap.create_result(obj, indent + 1)
        data += f'{tag}</association>\n'
        return data

    # 生成 result 一对多块
    @staticmethod
    def create_result_collection(obj: dict, indent: int) -> str:
        """
        生成 result 一对多块
        :param obj: 配置对象
        :param indent: 缩进
        :return: 一对一块
        """
        tag = '\t' * indent
        className = obj["className"]
        data = ""
        data += f'{tag}<collection property="list{className}" ofType="{obj["package"]}">\n'
        data += CreateResultMap.create_result(obj, indent + 1)
        data += f'{tag}</collection>\n'
        return data

    # 自我复制
    @staticmethod
    def table_increasing(obj: dict):
        """
        一对一或一对多下，自我递增复制
        :param obj: 配置文件
        """
        obj["tableName"] += "1"
        obj["key"]["filed"] += "1"
        for attr in obj["attr"]:
            attr["filed"] += "1"

    @staticmethod
    def create(config):
        """
        创建文件
        :param config: 配置文件
        """
        className = config["className"]
        package = config["package"]
        resultMapName = config["config"]["xmlConfig"]["resultMapName"]
        tableName = config["tableName"]

        tag = "\t"
        data = ""
        data += f'{tag}<resultMap id="{resultMapName}{className}" type="{package}">\n'
        data += CreateResultMap.create_result(config, 2, False)
        data += f'{tag}</resultMap>\n\n'

        obj_table = set()
        obj_table.add(f'{resultMapName}{className}')

        if config.get("oneToOne"):
            for obj in config.get("oneToOne"):
                objClassName = obj["className"]
                objPackage = obj["package"]
                # 是重复表则需要自我映射
                if obj["tableName"] == tableName:
                    CreateResultMap.table_increasing(obj)
                # 一对一
                if f'{resultMapName}{className}OneToOne{objClassName}' not in obj_table:
                    data += f'{tag}<resultMap id="{resultMapName}{className}OneToOne{objClassName}" type="{package}">\n'
                    data += CreateResultMap.create_result(config, 2)
                    data += CreateResultMap.create_result_association(obj, 2)
                    data += f'{tag}</resultMap>\n\n'
                    obj_table.add(f'{resultMapName}{className}OneToOne{objClassName}')
                # 另一方独立获取
                if f'res{objClassName}' not in obj_table:
                    data += f'{tag}<resultMap id="{resultMapName}{objClassName}" type="{objPackage}">\n'
                    data += CreateResultMap.create_result(obj, 2, False)
                    data += f'{tag}</resultMap>\n\n'
                    obj_table.add(f'{resultMapName}{objClassName}')

        if config.get("oneToMany"):
            for obj in config.get("oneToMany"):
                objClassName = obj["className"]
                objPackage = obj["package"]
                if obj["tableName"] == tableName:
                    CreateResultMap.table_increasing(obj)
                # 一对多
                if f'{resultMapName}{className}OneToMany{objClassName}' not in obj_table:
                    data += f'{tag}<resultMap id="{resultMapName}{className}OneToMany{objClassName}" type="{package}">\n'
                    data += CreateResultMap.create_result(config, 2)
                    data += CreateResultMap.create_result_collection(obj, 2)
                    data += f'{tag}</resultMap>\n\n'
                    obj_table.add(f'{resultMapName}{className}OneToMany{objClassName}')
                # 另一方独立获取
                if f'{resultMapName}{objClassName}' not in obj_table:
                    data += f'{tag}<resultMap id="{resultMapName}{objClassName}" type="{objPackage}">\n'
                    data += CreateResultMap.create_result(obj, 2, False)
                    data += f'{tag}</resultMap>\n\n'
                    obj_table.add(f'{resultMapName}{objClassName}')

        if config.get("manyToMany"):
            for obj in config.get("manyToMany"):
                obj = obj["many"]
                objClassName = obj["className"]
                objPackage = obj["package"]
                if obj["tableName"] == tableName:
                    CreateResultMap.table_increasing(obj)
                # 一对多
                if f'{resultMapName}{className}ManyToMany{objClassName}' not in obj_table:
                    data += f'{tag}<resultMap id="{resultMapName}{className}ManyToMany{objClassName}" type="{package}">\n'
                    data += CreateResultMap.create_result(config, 2)
                    data += CreateResultMap.create_result_collection(obj, 2)
                    data += f'{tag}</resultMap>\n\n'
                    obj_table.add(f'{resultMapName}{className}ManyToMany{objClassName}')
                # 另一方独立获取
                if f'{resultMapName}{objClassName}' not in obj_table:
                    data += f'{tag}<resultMap id="{resultMapName}{objClassName}" type="{objPackage}">\n'
                    data += CreateResultMap.create_result(obj, 2, False)
                    data += f'{tag}</resultMap>\n\n'
                    obj_table.add(f'{resultMapName}{objClassName}')
        data += "\n"
        return data
