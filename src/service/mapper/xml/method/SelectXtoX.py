from src.constant.ProtocolConstant import JsonKey
from src.service.mapper.xml.method.Block import CreateXmlBlock
from src.service.mapper.xml.method.Select import CreateMethodSelect
from src.util import StringUtil, util


class CreateMethodSelectXToX:
    """
    创建查询方法
    """

    @staticmethod
    def get_filed(config: dict, bean: dict, indent: int):
        """
        获取查询的字段
        :param config:本表
        :param bean: 当前表
        :param indent: 缩进
        """
        tag = "\t" * indent
        tableName = config["tableName"]
        objTableName = bean[JsonKey.tableName]
        select_filed = "* "
        suffix = util.if_return(objTableName == tableName, "1", "")
        if True:
            select_filed = f'\n{tag}<include refid="sql_filed_{tableName}"/>,\n'
            select_filed += f'{tag}<include refid="sql_filed_{objTableName}{suffix}"/>\n'
            select_filed += f'{tag}'
        return select_filed

    # 创建查询块
    @staticmethod
    def __create_select_inline(config, one_to_x):
        """
        创建查询块
        :param config: 配置文件
        """
        className = config["className"]
        lowClassName = StringUtil.first_char_lower_case(className)
        key = config["key"]["attr"]
        upperKey = StringUtil.first_char_upper_case(key)
        keyFiled = config["key"]["filed"]
        # if "fieldAlias" in config["key"]:
        # keyFiled = config["key"]["fieldAlias"]
        tableName = config["tableName"]
        resultMapName = config["config"]["xmlConfig"]["resultMapName"]

        ONE_TO_X = StringUtil.first_char_upper_case(one_to_x)
        tag = "\t"
        method_str = ""
        if config.get(one_to_x):
            # 一张表被多次关联
            obj_table = set()
            for obj in config[one_to_x]:
                objKey = obj[JsonKey.key.self][JsonKey.key.attr]
                objUpperKey = StringUtil.first_char_upper_case(objKey)
                objKeyFiled = obj[JsonKey.key.self][JsonKey.key.filed]
                objClassName = obj[JsonKey.className]
                lowObjClassName = StringUtil.first_char_lower_case(objClassName)
                objTableName = obj[JsonKey.tableName]
                objForeignKey = obj[JsonKey.foreignKey]
                # if "fieldAlias" in obj[JsonKey.key.self]:
                #     objForeignKey = obj[JsonKey.key.self]["fieldAlias"]

                join = util.if_return(objClassName in obj_table, f'On{objUpperKey}', "")
                obj_table.add(objClassName)
                # 两个表有无重复字段，有导入sql标签，否则*替代
                select_filed = CreateMethodSelectXToX.get_filed(config, obj, 3)
                data = f'{tag}<select id="find{className}{ONE_TO_X}{objClassName}{join}" resultMap="{resultMapName}{className}{ONE_TO_X}{objClassName}">\n'
                # 内联形式
                table_alias = util.if_return(objTableName == tableName, f' AS {objTableName}1', "")
                data += f'{tag * 2}SELECT {select_filed}FROM {tableName} , {objTableName}{table_alias}\n'
                data += f'{tag * 2}<where>\n'
                if one_to_x == JsonKey.oneToOne:
                    data += f'{tag * 3}{tableName}.{objForeignKey} = {objTableName}.{objKeyFiled}\n'
                if one_to_x == JsonKey.oneToMany:
                    data += f'{tag * 3}{tableName}.{keyFiled} = {objTableName}.{objForeignKey}\n'

                data += CreateXmlBlock.where_mod_1(config, 3, lowClassName, False)
                data += CreateXmlBlock.where_mod_1(obj, 3, lowObjClassName, False)

                if config[JsonKey.config.self][JsonKey.config.fuzzySearch.self][JsonKey.config.fuzzySearch.enable]:
                    lists = config[JsonKey.config.self][JsonKey.config.fuzzySearch.self][JsonKey.config.fuzzySearch.data]
                    keyword = config[JsonKey.config.self][JsonKey.config.fuzzySearch.self][JsonKey.config.fuzzySearch.value]
                    data += CreateXmlBlock.compulsory_fuzzy_search(lists, keyword, 3, tableName)
                if obj[JsonKey.config.self][JsonKey.config.fuzzySearch.self][JsonKey.config.fuzzySearch.enable]:
                    lists = obj[JsonKey.config.self][JsonKey.config.fuzzySearch.self][JsonKey.config.fuzzySearch.data]
                    keyword = obj[JsonKey.config.self][JsonKey.config.fuzzySearch.self][JsonKey.config.fuzzySearch.value]
                    data += CreateXmlBlock.compulsory_fuzzy_search(lists, keyword + "1", 3, objTableName)

                data += f'{tag * 2}</where>\n'
                data += CreateXmlBlock.splicing_sql(config)
                data += CreateXmlBlock.page()
                data += f'{tag}</select>\n'
                method_str += data + '\n'
        return method_str

    # 根据id获取多个对象
    @staticmethod
    def __create_select_join(config, one_to_x):
        """
        根据id获取多个对象
        :param config: 配置文件
        """
        className = config["className"]
        lowClassName = StringUtil.first_char_lower_case(className)
        key = config["key"]["attr"]
        upperKey = StringUtil.first_char_upper_case(key)
        keyFiled = config["key"]["filed"]
        if "fieldAlias" in config["key"]:
            keyFiled = config["key"]["fieldAlias"]

        tableName = config["tableName"]
        resultMapName = config["config"]["xmlConfig"]["resultMapName"]

        ONE_TO_X = StringUtil.first_char_upper_case(one_to_x)
        tag = "\t"
        method_str = ""
        if config.get(one_to_x):
            obj_table = set()
            for obj in config[one_to_x]:
                objKey = obj[JsonKey.key.self][JsonKey.key.attr]
                objUpperKey = StringUtil.first_char_upper_case(objKey)
                objKeyFiled = obj[JsonKey.key.self][JsonKey.key.filed]
                objClassName = obj[JsonKey.className]
                lowObjClassName = StringUtil.first_char_lower_case(objClassName)
                objTableName = obj[JsonKey.tableName]
                objForeignKey = obj[JsonKey.foreignKey]
                for at in obj[JsonKey.attr.self]:
                    if at[JsonKey.attr.filed] == objKeyFiled:
                        if "fieldAlias" in at:
                            objForeignKey = at["fieldAlias"]

                join = util.if_return(objClassName in obj_table, f'On{objUpperKey}', "")
                obj_table.add(objClassName)

                data = f'{tag}<select id="query{className}{ONE_TO_X}{objClassName}{join}" resultMap="{resultMapName}{className}{ONE_TO_X}{objClassName}">\n'
                suffix = util.if_return(objTableName == tableName, "1", "")

                if True:
                    select_filed_left = f'\n{tag * 4}<include refid="sql_filed_{tableName}"/>\n{tag * 3}'
                    select_filed_right = f'\n{tag * 4}<include refid="sql_filed_{objTableName}{suffix}"/>\n{tag * 3}'
                else:
                    select_filed_left = select_filed_right = "* "

                left = f'{tag * 3}SELECT {select_filed_left}FROM {tableName}\n'
                left += f'{tag * 3}<where>\n'
                left += CreateXmlBlock.where_mod_1(config, 4, lowClassName, False)
                left += f'{tag * 3}</where>\n'
                left += CreateXmlBlock.page(3)

                table_alias = util.if_return(objTableName == tableName, f' AS {objTableName}1', "")

                right = f'{tag * 3}SELECT {select_filed_right}FROM {objTableName}{table_alias}\n'
                right += f'{tag * 3}<where>\n'
                right += CreateXmlBlock.where_mod_1(obj, 4, lowClassName, False)
                right += f'{tag * 3}</where>\n'
                right += CreateXmlBlock.page(3, "page1")

                data += f'{tag * 2}SELECT * FROM (\n'
                data += left
                data += f'{tag * 2}) AS temp_{tableName} LEFT JOIN (\n'
                data += right
                data += f'{tag * 2}) AS temp_{objTableName}{suffix}\n'

                if one_to_x == JsonKey.oneToOne:
                    data += f'{tag * 2}ON temp_{tableName}.{objForeignKey} = temp_{objTableName}{suffix}.{objKeyFiled}{suffix}\n'
                if one_to_x == JsonKey.oneToMany:
                    data += f'{tag * 2}ON temp_{tableName}.{keyFiled} = temp_{objTableName}{suffix}.{objForeignKey}{suffix}\n'

                data += CreateXmlBlock.splicing_sql(config)
                data += f'{tag}</select>\n'
                method_str += data + '\n'
        return method_str

    # 查询一个
    @staticmethod
    def __create_link_one(config, one_to_x):
        """
        根据主键条件删除
        :param config: 配置文件
        """
        className = config["className"]
        lowClassName = StringUtil.first_char_lower_case(className)
        key = config["key"]["attr"]
        keyFiled = config["key"]["filed"]
        tableName = config["tableName"]
        ONE_TO_X = StringUtil.first_char_upper_case(one_to_x)

        tag = "\t"
        method_str = ""
        if config.get(one_to_x):
            obj_table = set()
            for obj in config[one_to_x]:
                objKey = obj[JsonKey.key.self][JsonKey.key.attr]
                objUpperKey = StringUtil.first_char_upper_case(objKey)
                objKeyFiled = obj[JsonKey.key.self][JsonKey.key.filed]
                objClassName = obj[JsonKey.className]
                lowObjClassName = StringUtil.first_char_lower_case(objClassName)
                objTableName = obj[JsonKey.tableName]
                objForeignKey = obj[JsonKey.foreignKey]
                resultMapName = obj[JsonKey.config.self][JsonKey.config.xmlConfig.self][JsonKey.config.xmlConfig.resultMapName]

                join = util.if_return(objClassName in obj_table, f'On{objUpperKey}', "")
                obj_table.add(objClassName)

                select_filed = f'{objTableName}.*'

                data = f'{tag}<select id="link{ONE_TO_X}{objClassName}{join}" resultMap="{resultMapName}{objClassName}">\n'
                # 内联形式
                table_alias = util.if_return(objTableName == tableName, f' AS {objTableName}1', "")
                data += f'{tag * 2}SELECT {select_filed} FROM {tableName} ,{objTableName}{table_alias}\n'
                data += f'{tag * 2}<where>\n'

                if one_to_x == JsonKey.oneToOne:
                    data += f'{tag * 3}{tableName}.{objForeignKey} = {objTableName}.{objKeyFiled}\n'
                if one_to_x == JsonKey.oneToMany:
                    data += f'{tag * 3}{tableName}.{keyFiled} = {objTableName}.{objForeignKey}\n'

                data += CreateXmlBlock.where_mod_1(config, 3, lowClassName, False)
                data += CreateXmlBlock.where_mod_1(obj, 3, lowObjClassName, False)

                if config[JsonKey.config.self][JsonKey.config.fuzzySearch.self][JsonKey.config.fuzzySearch.enable]:
                    lists = config[JsonKey.config.self][JsonKey.config.fuzzySearch.self][JsonKey.config.fuzzySearch.data]
                    keyword = config[JsonKey.config.self][JsonKey.config.fuzzySearch.self][JsonKey.config.fuzzySearch.value]
                    data += CreateXmlBlock.compulsory_fuzzy_search(lists, keyword, 3, tableName)
                if obj[JsonKey.config.self][JsonKey.config.fuzzySearch.self][JsonKey.config.fuzzySearch.enable]:
                    lists = obj[JsonKey.config.self][JsonKey.config.fuzzySearch.self][JsonKey.config.fuzzySearch.data]
                    keyword = obj[JsonKey.config.self][JsonKey.config.fuzzySearch.self][JsonKey.config.fuzzySearch.value]
                    data += CreateXmlBlock.compulsory_fuzzy_search(lists, keyword + "1", 3, objTableName)

                data += f'{tag * 2}</where>\n'
                data += CreateXmlBlock.splicing_sql(config)
                data += CreateXmlBlock.page()
                data += f'{tag}</select>\n'
                method_str += data + '\n'
        return method_str

    # 查询记录
    @staticmethod
    def __create_count(config, one_to_x):
        """
        查询记录
        :param config: 配置文件
        """
        className = config["className"]
        lowClassName = StringUtil.first_char_lower_case(className)
        key = config["key"]["attr"]
        upperKey = StringUtil.first_char_upper_case(key)
        keyFiled = config["key"]["filed"]
        tableName = config["tableName"]
        resultMapName = config["config"]["xmlConfig"]["resultMapName"]

        ONE_TO_X = StringUtil.first_char_upper_case(one_to_x)

        tag = "\t"
        method_str = ""
        if config.get(one_to_x):
            obj_table = set()
            for obj in config[one_to_x]:
                objKey = obj[JsonKey.key.self][JsonKey.key.attr]
                objUpperKey = StringUtil.first_char_upper_case(objKey)
                objKeyFiled = obj[JsonKey.key.self][JsonKey.key.filed]
                objClassName = obj[JsonKey.className]
                lowObjClassName = StringUtil.first_char_lower_case(objClassName)
                objTableName = obj[JsonKey.tableName]
                objForeignKey = obj[JsonKey.foreignKey]
                resultMapName = obj[JsonKey.config.self][JsonKey.config.xmlConfig.self][JsonKey.config.xmlConfig.resultMapName]

                join = util.if_return(objClassName in obj_table, f'On{objUpperKey}', "")
                suffix = util.if_return(objTableName == tableName, "1", "")

                select_filed_left = f'{tableName}.{keyFiled}'
                select_filed_right = f'{objTableName}{suffix}.{objForeignKey}{suffix}'

                data = f'{tag}<select id="count{ONE_TO_X}{className}OneToMany{obj["className"]}{join}" resultType="int">\n'

                left = f'{tag * 3}SELECT {select_filed_left} FROM {tableName}\n'
                left += f'{tag * 3}<where>\n'
                left += CreateXmlBlock.where_mod_1(config, 4, lowClassName, False)
                left += f'{tag * 3}</where>\n'
                left += CreateXmlBlock.page(3)

                table_alias = util.if_return(objTableName == tableName, f' AS {objTableName}1', "")

                right = f'{tag * 3}SELECT {select_filed_right} FROM {objTableName}{table_alias}\n'
                right += f'{tag * 3}<where>\n'
                right += CreateXmlBlock.where_mod_1(obj, 4, lowClassName, False)
                right += f'{tag * 3}</where>\n'
                right += CreateXmlBlock.page(3, "page1")

                data += f'{tag * 2}SELECT COUNT(DISTINCT temp_{tableName}.{keyFiled}) FROM (\n'
                data += left
                data += f'{tag * 2}) AS temp_{tableName} LEFT JOIN (\n'
                data += right
                data += f'{tag * 2}) AS temp_{objTableName}{suffix}\n'
                data += f'{tag * 2}ON temp_{tableName}.{keyFiled} = temp_{objTableName}{suffix}.{objForeignKey}{suffix}\n'

                data += f'{tag}</select>\n'
                method_str += data + '\n'
        return method_str

    @staticmethod
    def __create_many_to_many(config: dict, select_type: str, inline=True):

        className = config["className"]
        lowClassName = StringUtil.first_char_lower_case(className)
        key = config["key"]["attr"]
        upperKey = StringUtil.first_char_upper_case(key)
        keyFiled = config["key"]["filed"]
        if "fieldAlias" in config["key"]:
            keyFiled = config["key"]["fieldAlias"]

        tableName = config["tableName"]
        resultMapName = config["config"]["xmlConfig"]["resultMapName"]

        tag = "\t"
        method_str = ""
        if config.get(JsonKey.manyToMany):
            obj_table = set()
            for obj in config[JsonKey.manyToMany]:
                objKey = obj["many"][JsonKey.key.self][JsonKey.key.attr]
                objUpperKey = StringUtil.first_char_upper_case(objKey)
                objKeyFiled = obj["many"][JsonKey.key.self][JsonKey.key.filed]
                objClassName = obj["many"][JsonKey.className]
                lowObjClassName = StringUtil.first_char_lower_case(objClassName)
                objTableName = obj["many"][JsonKey.tableName]
                objForeignKey = obj["many"][JsonKey.foreignKey]
                for at in obj["many"][JsonKey.attr.self]:
                    if at[JsonKey.attr.filed] == objKeyFiled:
                        if "fieldAlias" in at:
                            objForeignKey = at["fieldAlias"]

                manny_table = ""
                if f'{obj["to"]["className"]}On{obj["many"]["className"]}' in obj_table:
                    manny_table = f'Join{StringUtil.underscore_to_big_hump(obj["to"]["foreign_key"])}'
                obj_table.add(f'{obj["to"]["className"]}On{objClassName}')

                suffix = util.if_return(objTableName == tableName, "1", "")

                if True:
                    select_filed_main = f'\n{tag * 4}<include refid="sql_filed_{tableName}"/>\n{tag * 3}'
                    select_filed_join = f'\n{tag * 4}<include refid="sql_filed_{objTableName}{suffix}"/>\n{tag * 3}'
                else:
                    select_filed_main = "* "
                    select_filed_join = "* "

                data = f'{tag}<select id="{select_type}{className}ManyToManyLink{obj["to"]["className"]}On{objClassName}{manny_table}" resultMap="{resultMapName}{className}ManyToMany{objClassName}">\n'
                subquery = f'{tag * 3}select {select_filed_main}from {config["tableName"]}\n'
                subquery += f'{tag * 3}<where>\n'
                subquery += CreateXmlBlock.where_mod_1(config, 4)
                subquery += f'{tag * 3}</where>\n'
                subquery += f'{tag * 3}<if test="page!=null">\n'
                subquery += f'{tag * 4}limit #{{page.start}},#{{page.count}}\n'
                subquery += f'{tag * 3}</if>\n'

                temp_sql = ""
                temp_sql2 = ""
                if config.get("table_my") and obj["many"]["tableName"] == config["tableName"]:
                    temp_sql = f' AS {obj["many"]["tableName"]}1'
                    temp_sql2 = "1"

                if inline:
                    data += f'{tag * 2}select {select_filed_join}from (\n{subquery}{tag * 2}) AS temp_{tableName},{obj["to"]["tableName"]},{objTableName}{temp_sql}\n'
                    data += f'{tag * 2}where temp_{tableName}.{keyFiled} = {obj["to"]["tableName"]}.{obj["to"][JsonKey.foreignKey]}\n'
                    data += f'{tag * 2}AND {obj["to"]["tableName"]}.{objForeignKey} = {objTableName}{temp_sql2}.{objKeyFiled}\n'
                else:
                    data += f'{tag * 2}select {select_filed_join}from (\n{subquery}{tag * 2}) AS temp_{tableName} LEFT JOIN {obj["to"]["tableName"]}\n'
                    data += f'{tag * 2}ON temp_{tableName}.{keyFiled} = {obj["to"]["tableName"]}.{obj["to"][JsonKey.foreignKey]}\n'
                    data += f'{tag * 2}LEFT JOIN {objTableName}{temp_sql} On {obj["to"]["tableName"]}.{objForeignKey} = {objTableName}{temp_sql2}.{objKeyFiled}\n'
                data += CreateXmlBlock.splicing_sql(config)
                data += f'{tag}</select>\n'
                method_str += data + '\n'
        return method_str

    @staticmethod
    def __create_select_in_foreign_key(config: dict):
        """
         根据外键获取多个对象
         :param config: 配置文件
         """
        className = config["className"]
        key = config["key"]["attr"]
        upperKey = StringUtil.first_char_upper_case(key)
        keyFiled = config["key"]["filed"]
        tableName = config["tableName"]
        lowClassName = StringUtil.first_char_lower_case(className)
        data = ""
        tag = "\t"
        if config.get(JsonKey.oneToOne):
            obj_fk = set()
            for obj in config.get(JsonKey.oneToOne):
                if obj[JsonKey.foreignKey] not in obj_fk:
                    attr = None
                    for i in config[JsonKey.attr.self]:
                        if i[JsonKey.attr.filed] == obj[JsonKey.foreignKey]:
                            attr = i
                            break
                    if attr is None:
                        continue
                    res_type = CreateMethodSelect.getResult(config)
                    data += f'{tag}<select id="select{className}In{StringUtil.first_char_upper_case(attr[JsonKey.attr.attr])}AndWhere" {res_type}>\n'
                    data += f'{tag * 2}SELECT * FROM {tableName}\n'
                    data += f'{tag * 2}<where>\n'
                    data += f'{tag * 3}{obj[JsonKey.foreignKey]} IN\n'
                    data += f'{tag * 3}<foreach item="item" index="index" collection="list" open="(" separator="," close=")">#{{item}}</foreach>\n'
                    data += CreateXmlBlock.where_mod_1(config, 3, lowClassName)
                    data += f'{tag * 2}</where>\n'
                    data += f'{tag}</select>\n\n'
                    obj_fk.add(obj[JsonKey.foreignKey])
        return data

    @staticmethod
    def create(config):
        data = ""
        data += CreateMethodSelectXToX.__create_select_inline(config, JsonKey.oneToOne)
        data += CreateMethodSelectXToX.__create_select_inline(config, JsonKey.oneToMany)
        data += CreateMethodSelectXToX.__create_select_join(config, JsonKey.oneToOne)
        data += CreateMethodSelectXToX.__create_select_join(config, JsonKey.oneToMany)
        data += CreateMethodSelectXToX.__create_link_one(config, JsonKey.oneToOne)
        data += CreateMethodSelectXToX.__create_link_one(config, JsonKey.oneToMany)
        data += CreateMethodSelectXToX.__create_count(config, JsonKey.oneToOne)
        data += CreateMethodSelectXToX.__create_count(config, JsonKey.oneToMany)
        data += CreateMethodSelectXToX.__create_many_to_many(config, "find")
        data += CreateMethodSelectXToX.__create_many_to_many(config, "query", False)
        data += CreateMethodSelectXToX.__create_select_in_foreign_key(config)
        return data
