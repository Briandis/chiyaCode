from src.service.mapper.xml.method.Block import CreateXmlBlock
from src.service.mapper.xml.method.configBlock import DatabaseNameConfig
from src.util import util


class CreateMethodInsert:
    """
    创建插入方法
    """

    # 创建插入块
    @staticmethod
    def __create_insert(config):
        """
        创建插入块
        :param config: 配置文件
        """
        className = config["className"]
        tableName = config["tableName"]
        attrs = []
        key = None
        if "key" in config:
            key = config["key"]["attr"]
            keyFiled = config["key"]["filed"]
            attrs.append(config["key"])
        for attr in config["attr"]:
            attrs.append(attr)
        attrs = {"attr": attrs}
        tag = "\t"
        if "key" in config:
            data = f'{tag}<insert id="insert{className}" useGeneratedKeys="true" keyProperty="{key}" keyColumn="{keyFiled}">\n'
        else:
            data = f'{tag}<insert id="insert{className}">\n'
        data += f'{tag * 2}INSERT INTO {DatabaseNameConfig.get_database_name(config)}{tableName} (\n'
        data += f'{tag * 2}<trim prefix="" suffixOverrides=",">\n'
        data += CreateXmlBlock.if_mod_1(attrs, 3)
        data += f'{tag * 2}</trim>\n'
        data += f'{tag * 2}) VALUES (\n'
        data += f'{tag * 2}<trim prefix="" suffixOverrides=",">\n'
        data += CreateXmlBlock.if_mod_2(attrs, 3)
        data += f"{tag * 2}</trim>\n"
        data += f'{tag * 2})\n'
        data += f'{tag}</insert>\n\n'
        return data

    # 创建批量插入块
    @staticmethod
    def __create_insert_list(config):
        """
        创建批量插入块
        :param config: 配置文件
        """
        className = config["className"]
        tableName = config["tableName"]
        attrs = []
        key = None
        if "key" in config:
            key = config["key"]["attr"]
            keyFiled = config["key"]["filed"]
            attrs.append(config["key"])
        for attr in config["attr"]:
            attrs.append(attr)
        i, max_len = 0, len(attrs)

        tag = "\t"
        if "key" in config:
            data = f'{tag}<insert id="insert{className}List" useGeneratedKeys="true" keyProperty="{key}" keyColumn="{keyFiled}">\n'
        else:
            data = f'{tag}<insert id="insert{className}List">\n'
        data += f'{tag * 2}INSERT INTO {DatabaseNameConfig.get_database_name(config)}{tableName} (\n'
        data += f'{tag * 3}'

        for attr in attrs:
            i += 1
            data += f'{attr["filed"]}'
            data += util.if_return(i == max_len, "\n", ",")

        data += f'{tag * 2}) VALUES\n'
        data += f'{tag * 2}<foreach collection="list" index="index" item="obj" separator=",">\n'
        data += f'{tag * 3}(\n'
        i = 0
        for attr in attrs:
            i += 1
            data += f'{tag * 4}#{{obj.{attr["attr"]}}}'
            data += util.if_return(i == max_len, "\n", ",\n")
        data += f'{tag * 3})\n'
        data += f'{tag * 2}</foreach>\n'
        data += f'{tag}</insert>\n\n'
        return data

    # 添加或更新,根据索引
    @staticmethod
    def __create_insert_or_update_unique(config):
        """
        添加或更新,根据索引
        :param config: 配置文件
        """
        className = config["className"]
        tableName = config["tableName"]
        attrs = []
        key = None
        if "key" in config:
            key = config["key"]["attr"]
            keyFiled = config["key"]["filed"]
            attrs.append(config["key"])
        for attr in config["attr"]:
            attrs.append(attr)
        attrs = {"attr": attrs}

        tag = "\t"
        if "key" in config:
            data = f'{tag}<insert id="insertOrUpdate{className}ByUnique" useGeneratedKeys="true" keyProperty="{key}" keyColumn="{keyFiled}">\n'
        else:
            data = f'{tag}<insert id="insertOrUpdate{className}ByUnique">\n'
        data += f'{tag * 2}INSERT INTO {DatabaseNameConfig.get_database_name(config)}{tableName} (\n'
        data += f'{tag * 2}<trim prefix="" suffixOverrides=",">\n'
        data += CreateXmlBlock.if_mod_1(attrs, 3)
        data += f'{tag * 2}</trim>\n'
        data += f'{tag * 2}) VALUE (\n'
        data += f'{tag * 2}<trim prefix="" suffixOverrides=",">\n'
        data += CreateXmlBlock.if_mod_2(attrs, 3)
        data += f"{tag * 2}</trim>\n\t\t) ON DUPLICATE KEY UPDATE \n"
        data += f'{tag * 2}<trim prefix="" suffixOverrides=",">\n'
        data += CreateXmlBlock.if_mod_3(config, 3)
        data += f'{tag * 2}</trim>\n'
        data += f'{tag}</insert>\n\n'
        return data

    # 添加或更新,根据查询
    @staticmethod
    def __create_insert_or_update_where(config):
        """
        添加或更新,根据查询
        :param config: 配置文件
        """
        if "key" not in config:
            return ""

        className = config["className"]
        key = config["key"]["attr"]
        keyFiled = config["key"]["filed"]
        tableName = config["tableName"]

        attrs = []
        attrs.append(config["key"])
        for attr in config["attr"]:
            attrs.append(attr)
        attrs = {"attr": attrs}

        tag = "\t"
        data = f'{tag}<insert id="insertOrUpdate{className}ByWhere">\n'
        data += f'{tag * 2}<selectKey keyProperty="condition{className}.{key}" keyColumn="{keyFiled}" resultType="int" order="BEFORE">\n'
        data += f'{tag * 3}SELECT IFNULL ((\n'
        data += f'{tag * 4}SELECT {keyFiled} FROM {DatabaseNameConfig.get_database_name(config)}{tableName}\n'
        data += f'{tag * 4}<where>\n'
        data += CreateXmlBlock.where_mod_2(config, 5, f'condition{className}', False)
        data += f'{tag * 4}</where>\n'
        data += f'{tag * 3}),NULL)\n'
        data += f'{tag * 2}</selectKey>\n'

        data += f'{tag * 2}<if test="condition{className}.{key}==null">\n'
        data += f'{tag * 3}INSERT INTO {DatabaseNameConfig.get_database_name(config)}{tableName} (\n'
        data += f'{tag * 3}<trim prefix="" suffixOverrides=",">\n'
        data += CreateXmlBlock.if_mod_1(attrs, 4, f'save{className}')
        data += f'{tag * 3}</trim>\n'
        data += f'{tag * 3}) VALUES (\n'
        data += f'{tag * 3}<trim prefix="" suffixOverrides=",">\n'
        data += CreateXmlBlock.if_mod_2(attrs, 4, f'save{className}')
        data += f"{tag * 3}</trim>\n{tag * 2})\n"
        data += f'{tag * 2}</if>\n'

        data += f'{tag * 2}<if test="condition{className}.{key}!=null">\n'
        data += f'{tag * 3}UPDATE {DatabaseNameConfig.get_database_name(config)}{tableName}\n'
        data += f'{tag * 3}<set>\n'
        data += CreateXmlBlock.if_mod_3(config, 4, f'save{className}')
        data += f'{tag * 3}</set>\n'
        data += f'{tag * 3}WHERE {keyFiled} = #{{condition{className}.{key}}}\n'
        data += f'{tag * 2}</if>\n'
        data += f'{tag}</insert>\n\n'
        return data

    # 查询到数据，则添加
    @staticmethod
    def __create_insert_by_exist(config):
        """
        根据查询条件存在下添加
        :param config: 配置文件
        """
        className = config["className"]
        tableName = config["tableName"]
        attrs = []
        key = None
        if "key" in config:
            key = config["key"]["attr"]
            keyFiled = config["key"]["filed"]
            attrs.append(config["key"])
        for attr in config["attr"]:
            attrs.append(attr)
        attrs = {"attr": attrs}

        tag = "\t"
        if "key" in config:
            data = f'{tag}<insert id="insert{className}ByExistWhere" useGeneratedKeys="true" keyProperty="save{className}.{key}" keyColumn="{keyFiled}">\n'
        else:
            data = f'{tag}<insert id="insert{className}ByExistWhere">\n'
        data += f'{tag * 2}INSERT INTO {DatabaseNameConfig.get_database_name(config)}{tableName} (\n'
        data += f'{tag * 2}<trim prefix="" suffixOverrides=",">\n'
        data += CreateXmlBlock.if_mod_1(attrs, 3, f'save{className}')
        data += f'{tag * 2}</trim>\n'
        data += f'{tag * 2}) SELECT \n'
        data += f'{tag * 2}<trim prefix="" suffixOverrides=",">\n'
        data += CreateXmlBlock.if_mod_2(attrs, 3, f'save{className}')
        data += f"{tag * 2}</trim>\n"
        data += f'{tag * 2}FROM DUAL WHERE EXISTS (\n'
        if "key" in config:
            data += f'{tag * 3}SELECT {keyFiled} FROM {DatabaseNameConfig.get_database_name(config)}{tableName}\n'
        else:
            data += f'{tag * 3}SELECT * FROM {DatabaseNameConfig.get_database_name(config)}{tableName}\n'
        data += f'{tag * 3}<where>\n'
        data += CreateXmlBlock.where_mod_2(config, 4, f'condition{className}', False)
        data += f'{tag * 3}</where>\n'
        data += f'{tag * 2})\n'
        data += f'{tag}</insert>\n\n'
        return data

    # 查询条件不存在下，则添加
    @staticmethod
    def __create_insert_by_not_exist(config):
        """
        根据查询条件存在下添加
        :param config: 配置文件
        """
        className = config["className"]
        tableName = config["tableName"]
        attrs = []
        key = None
        if "key" in config:
            key = config["key"]["attr"]
            keyFiled = config["key"]["filed"]
            attrs.append(config["key"])
        for attr in config["attr"]:
            attrs.append(attr)
        attrs = {"attr": attrs}

        tag = "\t"
        if "key" in config:
            data = f'{tag}<insert id="insert{className}ByNotExistWhere" useGeneratedKeys="true" keyProperty="save{className}.{key}" keyColumn="{keyFiled}">\n'
        else:
            data = f'{tag}<insert id="insert{className}ByNotExistWhere">\n'
        data += f'{tag * 2}INSERT INTO {DatabaseNameConfig.get_database_name(config)}{tableName} (\n'
        data += f'{tag * 2}<trim prefix="" suffixOverrides=",">\n'
        data += CreateXmlBlock.if_mod_1(attrs, 3, f'save{className}')
        data += f'{tag * 2}</trim>\n'
        data += f'{tag * 2}) SELECT \n'
        data += f'{tag * 2}<trim prefix="" suffixOverrides=",">\n'
        data += CreateXmlBlock.if_mod_2(attrs, 3, f'save{className}')
        data += f"{tag * 2}</trim>\n"
        data += f'{tag * 2}FROM DUAL WHERE NOT EXISTS (\n'
        if "key" in config:
            data += f'{tag * 3}SELECT {keyFiled} FROM {DatabaseNameConfig.get_database_name(config)}{tableName}\n'
        else:
            data += f'{tag * 3}SELECT * FROM {DatabaseNameConfig.get_database_name(config)}{tableName}\n'
        data += f'{tag * 3}<where>\n'
        data += CreateXmlBlock.where_mod_2(config, 4, f'condition{className}', False)
        data += f'{tag * 3}</where>\n'
        data += f'{tag * 2})\n'
        data += f'{tag}</insert>\n\n'
        return data

    @staticmethod
    def create(config):
        data = ""
        data += CreateMethodInsert.__create_insert(config)
        data += CreateMethodInsert.__create_insert_list(config)
        data += CreateMethodInsert.__create_insert_or_update_unique(config)
        data += CreateMethodInsert.__create_insert_or_update_where(config)
        data += CreateMethodInsert.__create_insert_by_exist(config)
        data += CreateMethodInsert.__create_insert_by_not_exist(config)
        return data
