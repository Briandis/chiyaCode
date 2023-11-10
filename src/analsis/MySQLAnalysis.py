from typing import List

from src.util.MySQLUtil import MySql


class Column:
    def __init__(self):
        """
        属性对象
        """
        self.name = None
        """ 字段名称 """
        self.data_type = None
        """ 数据类型 """
        self.column_key = None
        """ 字段主键类型 """
        self.column_comment = None
        """ 字段备注 """

    def __str__(self):
        return str(self.__dict__)


class DataBase:
    def __init__(self):
        """
        数据查询表对象
        """
        # 表名称
        self.table_name = None
        # 表备注
        self.table_comment = None
        # 持有的字段
        self.columns: List[Column] = []

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

    def get_all_table(self) -> List[DataBase]:
        """
        获取数据库中表和持有的字段
        :return: list集合
        """
        list_table = self.mysql.get_all_table_and_field()
        result = []
        for table in list_table:
            data_base = DataBase()
            data_base.table_name = table["TABLE_NAME"]
            data_base.table_comment = table["TABLE_COMMENT"]
            for field in table["COLUMN"]:
                column = Column()
                column.name = field["COLUMN_NAME"]
                column.data_type = field["DATA_TYPE"]
                column.column_comment = field["COLUMN_COMMENT"]
                column.column_key = field["COLUMN_KEY"]
                data_base.columns.append(column)
            result.append(data_base)
        return result
