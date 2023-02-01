from src.constant.ProtocolConstant import JsonKey
from src.util.CollectionUtil import dict_set
from src.util.JavaBaseObject import mysql_to_java_object
from src.util.MySQLUtil import MySql
from src.util import StringUtil


class DataBase:
    def __init__(self):
        """
        数据查询表对象
        """
        # 表名称
        self.TABLE_NAME = None
        # 表备注
        self.TABLE_COMMENT = None
        # 表记录数
        self.TABLE_ROWS = 0
        # 持有的字段
        self.columns = []

    def __str__(self):
        return str(self.__dict__)


class Column:
    def __init__(self):
        """
        属性对象
        """
        # 字段名
        self.COLUMN_NAME = None
        # 表中的位置
        self.ORDINAL_POSITION = None
        # 数据类型
        self.DATA_TYPE = None
        # 是否为空
        self.IS_NULLABLE = None
        # 字段键类型
        self.COLUMN_KEY = None
        # 其他信息
        self.EXTRA = None
        # 字段备注
        self.COLUMN_COMMENT = None
        # 字段数据类型
        self.COLUMN_TYPE = None

    def __str__(self):
        return str(self.__dict__)


class AnalysisConfig:
    def __init__(self):
        # 驼峰命名
        self.hump = True
        # 统一移除表前缀
        self.tablePrefix = True
        # 要统一移除的前缀名称
        self.tablePrefixString = None
        # 将类名转成大驼峰
        self.classNameIsBigHump = True
        # 移除字段前缀
        self.columnPrefix = True
        # 要移除的字段前缀名称，空则是以表字段名称为主
        self.columnPrefixString = None
        # 自动映射多表关系
        self.multiTable = True
        # 一对一关系的表
        self.oneToOne = {}
        # 一对多的关系表
        self.oneToMany = {}
        # 多对多关系的表
        self.manyToMany = {}

    def assembly_config(self, config: dict):
        """
        装配配置文件中的内容到该对象
        :param config: 配置文件
        """
        attributes = self.__dict__
        for attribute in attributes:
            if attribute in config:
                setattr(self, attribute, config[attribute])
        # 转移一对一配置
        one_to_one = {}
        for i in self.oneToOne:
            me, you = i.split("->")
            dict_set(one_to_one, me, you)
            # 一对一进行双向绑定
            dict_set(one_to_one, you, me)
        self.oneToOne = one_to_one
        # 转义配置中的一对多
        one_to_many = {}
        for i in self.oneToMany:
            me, you = i.split("->")
            dict_set(one_to_many, me, you)
        self.oneToMany = one_to_many
        self.manyToMany = {}

    def __str__(self):
        return str(self.__dict__)


class JavaConfigBean:
    class Attribute:
        def __init__(self):
            # 属性名
            self.attribute = None
            # 字段名
            self.column = None
            # java数据类型
            self.javaDataType = None
            # 字段名称
            self.columnComment = None
            # 是主键
            self.isPrimaryKey = False

        def __str__(self):
            return str(self.__dict__)

    def __init__(self):
        """
        java结构化对象
        """
        # 表名称
        self.tableName = None
        # 中文名
        self.tableComment = None
        # 类名
        self.className = None
        # 持有的属性
        self.listAttribute = {}
        # 只有的主键
        self.key = None

    def __str__(self):
        return str(self.__dict__)


class MySQLAnalysis:
    def __init__(self, database, host="127.0.0.1", name="root", password="123456", port=3306):
        self.database = database
        self.mysql = MySql(database, host=host, name=name, password=password, port=port)

    def get_all_table(self) -> list:
        """
        获取数据库中表和持有的字段
        :return: list集合
        """
        # 查询库中所有表数据
        sql = f'SELECT * FROM information_schema.TABLES WHERE table_schema = "{self.database}" AND TABLE_TYPE = "BASE TABLE";'
        tables = self.mysql.select_to_dict(sql, DataBase())
        res_data = []
        for table in tables:
            sql = f'SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = "{self.database}" AND TABLE_NAME = "{table["TABLE_NAME"]}";'
            table["COLUMN"] = self.mysql.select_to_dict(sql, Column())
            res_data.append(table)
        self.mysql.close()
        return res_data


class StructureAnalysis:
    def __init__(self, tables: list, config: AnalysisConfig):
        """
        解析生成映射关系
        :param tables:
        :param config:
        """
        self.tables = tables
        self.config = config

    def parsing_field(self) -> dict:
        javabean = {}
        for table in self.tables:
            bean = {JsonKey.tableName: table["TABLE_NAME"], JsonKey.remark: table["TABLE_COMMENT"], JsonKey.className: table["TABLE_NAME"]}
            # 统一移除表前缀
            if self.config.tablePrefix and StringUtil.is_not_null(self.config.tablePrefixString):
                bean[JsonKey.className] = StringUtil.remove_prefix(bean[JsonKey.className], self.config.tablePrefixString)
            # 类名转大驼峰
            if self.config.classNameIsBigHump:
                bean[JsonKey.className] = StringUtil.underscore_to_big_hump(bean[JsonKey.className])
            # 解析字段

            attr = []
            for column in table["COLUMN"]:
                attribute = {JsonKey.attr.filed: column["COLUMN_NAME"], JsonKey.attr.attr: column["COLUMN_NAME"], JsonKey.attr.remark: column["COLUMN_COMMENT"]}
                # 移除字段前缀
                if self.config.columnPrefix:
                    el = self.config.columnPrefixString
                    if StringUtil.is_null(el):
                        el = table["TABLE_NAME"] + "_"
                    attribute[JsonKey.attr.attr] = StringUtil.remove_prefix(attribute[JsonKey.attr.attr], el)
                if self.config.hump:
                    attribute[JsonKey.attr.attr] = StringUtil.underscore_to_small_hump(attribute[JsonKey.attr.attr])

                attribute[JsonKey.attr.type] = mysql_to_java_object(column["DATA_TYPE"])
                if column["COLUMN_KEY"] == "PRI":
                    bean[JsonKey.key.self] = attribute
                    continue
                attr.append(attribute)
                # attr[attribute[JsonKey.attr.filed]] = attribute
            # if JsonKey.key.self not in bean:
            #     raise Exception(f'{table["TABLE_NAME"]}表缺少主键！！！')
            # bean[JsonKey.key.self] = {
            #     JsonKey.attr.filed: None,
            #     JsonKey.attr.attr: None,
            #     JsonKey.attr.remark: None,
            #     JsonKey.attr.type:None,
            # }
            bean[JsonKey.attr.self] = attr
            javabean[bean[JsonKey.tableName]] = bean
        return javabean


def parsing_field(tables, config: dict) -> dict:
    """
    根据配置解析字段，生成基础的javaBean
    :param tables:
    :param config:
    :return:
    """
    javabean = {}
    for table in tables:
        bean = {
            JsonKey.tableName: table["TABLE_NAME"],
            JsonKey.remark: table["TABLE_COMMENT"],
            JsonKey.className: table["TABLE_NAME"]
        }
        # 统一移除表前缀
        if config["tablePrefix"] and StringUtil.is_not_null(config["tablePrefixString"]):
            bean[JsonKey.className] = StringUtil.remove_prefix(bean[JsonKey.className], config["tablePrefixString"])
        # 类名转大驼峰
        if config["classNameIsBigHump"]:
            bean[JsonKey.className] = StringUtil.underscore_to_big_hump(bean[JsonKey.className])
        # 解析字段

        attr = []
        for column in table["COLUMN"]:
            attribute = {
                JsonKey.attr.filed: column["COLUMN_NAME"],
                JsonKey.attr.attr: column["COLUMN_NAME"],
                JsonKey.attr.remark: column["COLUMN_COMMENT"]
            }
            # 移除字段前缀
            if config["columnPrefix"]:
                el = config["columnPrefixString"]
                if StringUtil.is_null(el):
                    el = table["TABLE_NAME"] + "_"
                attribute[JsonKey.attr.attr] = StringUtil.remove_prefix(attribute[JsonKey.attr.attr], el)
            if config["hump"]:
                attribute[JsonKey.attr.attr] = StringUtil.underscore_to_small_hump(attribute[JsonKey.attr.attr])

            attribute[JsonKey.attr.type] = mysql_to_java_object(column["DATA_TYPE"])
            if column["COLUMN_KEY"] == "PRI":
                bean[JsonKey.key.self] = attribute
                continue
            attr.append(attribute)
            # attr[attribute[JsonKey.attr.filed]] = attribute
        bean[JsonKey.attr.self] = attr
        javabean[bean[JsonKey.tableName]] = bean
    return javabean
