import pymysql


class MySql:

    def __init__(self, database, cursor=pymysql.cursors.DictCursor,
                 host="127.0.0.1", name="root", password="123456", port=3306):
        self.conn = pymysql.connect(host=host, user=name, password=password, database=database, port=port)
        self.cursor_type = cursor

    def execute_select(self, sql_string: str, obj_class=None) -> list:
        """
        执行查询语句并返回对象
        :param sql_string:
        :param obj_class:
        :return: list对象集合
        """
        cursor = self.conn.cursor(self.cursor_type)
        cursor.execute(sql_string)
        lists = []
        for i in cursor.fetchall():
            if obj_class is None:
                lists.append(i)
            else:
                lists.append(self.__create_object(i, obj_class))
        cursor.close()
        return lists

    def execute_dml(self, sql_string: str) -> int:
        """
        执行DML型操作，返回受影响行数，并自带回滚
        :param sql_string: 说受影响行数
        :return: 受影响行数
        """
        cursor = self.conn.cursor(self.cursor_type)
        res = 0
        try:
            res = cursor.execute(sql_string)
            self.conn.commit()
        except:
            self.conn.rollback()
        cursor.close()
        return res

    def close(self):
        """
        关闭链接
        :return: None
        """
        self.conn.close()

    def __create_object(self, dict_data: dict, obj_class):
        """
        创建对象
        :param dict_data: 字典对象
        :param obj_class: 类型对象
        :return: obj_class的对象
        """
        obj = obj_class()
        column = obj.__dict__
        for i in dict_data:
            if i in column and i is not None:
                setattr(obj, i, dict_data[i])
        return obj

    def __create_dict(self, dict_data: dict, obj_class):
        """
        创建字典
        :param dict_data: 字典对象
        :param obj_class: 类型对象
        :return: obj_class的对象
        """
        column = obj_class.__dict__
        for k in list(dict_data.keys()):
            if k not in column:
                del dict_data[k]
        return dict_data

    def select(self, sql_string) -> list:
        """
        执行查询语句并返回对象
        :param sql_string:
        :param obj_class:
        :return: list对象集合
        """
        cursor = self.conn.cursor(self.cursor_type)
        cursor.execute(sql_string)
        lists = []
        for i in cursor.fetchall():
            lists.append(i)
        cursor.close()
        return lists

    def select_to_dict(self, sql_string: str, obj_class):
        """
        返回列表型字典，按照对象参数筛选
        :param sql_string: 字典对象
        :param obj_class: 类型对象
        :return:
        """
        cursor = self.conn.cursor(self.cursor_type)
        cursor.execute(sql_string)
        lists = []
        for i in cursor.fetchall():
            lists.append(self.__create_dict(i, obj_class))
        cursor.close()
        return lists
