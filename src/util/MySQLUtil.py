import json
import os
import time
from datetime import datetime, date
from typing import List

import pymysql
from _decimal import Decimal

from src.util.chiyaUtil import OSUtil


class DateTimeJson(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, Decimal):
            return f'{obj}'
        else:
            return json.JSONEncoder.default(self, obj)


class TableField:

    def __init__(self):
        self.name = None
        """ 字段名称 """
        self.type = None
        """ 字段类型 """
        self.key = None
        """ 是否为主键 """

    @staticmethod
    def create_field(field_dict: dict):
        table_field = TableField()
        table_field.name = field_dict["COLUMN_NAME"]
        table_field.type = field_dict["DATA_TYPE"]
        if field_dict["COLUMN_KEY"] != "":
            table_field.key = True
        return table_field


class TableInfo:

    def __init__(self):
        self.name = None
        """ 表名称 """
        self.field: List[TableField] = []
        """ 字段 """

    @staticmethod
    def create_table(table_dict):
        table_info = TableInfo()
        table_info.name = table_dict["TABLE_NAME"]
        for field_dict in table_dict["COLUMN"]:
            table_info.field.append(TableField.create_field(field_dict))
        return table_info

    @staticmethod
    def create_table_list(table_list):
        result: [TableInfo] = []
        for table_dict in table_list:
            table_info = TableInfo()
            table_info.name = table_dict["TABLE_NAME"]
            for field_dict in table_dict["COLUMN"]:
                table_info.field.append(TableField.create_field(field_dict))
            result.append(table_info)
        return result


class MySql:

    def __init__(self, database, cursor=pymysql.cursors.DictCursor,
                 host="127.0.0.1", name="root", password="123456", port=3306):
        self.conn = pymysql.connect(host=host, user=name, password=password, database=database, port=port)
        self.cursor_type = cursor
        self.database = database

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

    def select(self, sql_string) -> list:
        """
        执行查询语句并返回对象
        :param sql_string:
        :return  list对象集合
        """
        cursor = self.conn.cursor(self.cursor_type)
        cursor.execute(sql_string)
        lists = []
        for i in cursor.fetchall():
            lists.append(i)
        cursor.close()
        return lists

    def get_table_field(self, table_name):
        """
        查询表字段
        :param table_name:表名
        :return: 表中的字段
        """
        sql = f'SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = "{self.database}" AND TABLE_NAME = "{table_name}";'
        return self.select(sql)

    def get_all_table_and_field(self) -> list:
        """
        获取数据库中表和持有的字段
        :return: list集合
        """
        # 查询库中所有表数据
        sql = f'SELECT * FROM information_schema.TABLES WHERE table_schema = "{self.database}" AND TABLE_TYPE = "BASE TABLE";'
        tables = self.select(sql)
        res_data = []
        for table in tables:
            table["COLUMN"] = self.get_table_field(table["TABLE_NAME"])
            res_data.append(table)
        return res_data

    def get_all_table(self) -> list:
        """
        获取数据库中表和持有的字段
        :return: list集合
        """
        # 查询库中所有表数据
        sql = f'SELECT * FROM information_schema.TABLES WHERE table_schema = "{self.database}" AND TABLE_TYPE = "BASE TABLE";'
        return self.select(sql)

    def select_count_table(self, table_name) -> int:
        """
        查询该表中的数据数据量
        :param table_name:表名称
        :return: 数据行数
        """
        sql = f'SELECT COUNT(*) AS table_count FROM `{table_name}`;'
        return self.select(sql)[0]["table_count"]

    def save_database(self, tag_name=f'{int(time.time())}', limit_count=10000):
        """
        存储整个数据库
        :param tag_name:存储标记用的名称
        :param limit_count:存储时每页保存的记录数
        """

        save_path = OSUtil.is_not_dir_create(os.getcwd(), self.database)
        save_path = OSUtil.is_not_dir_create(save_path, tag_name)
        structure_path = OSUtil.is_not_dir_create(save_path, "structure")
        data_path = OSUtil.is_not_dir_create(save_path, "data")

        list_table = self.get_all_table_and_field()
        for table in list_table:
            table_name = table["TABLE_NAME"]
            table_count = self.select_count_table(table_name)
            with open(os.path.join(structure_path, table_name + ".structure.txt"), "w", encoding="utf-8") as file:
                file.write(json.dumps(table, indent=2, ensure_ascii=False, cls=DateTimeJson))

            for count_index in range(0, table_count, limit_count):
                sql = f'SELECT * FROM {table_name} LIMIT {limit_count} OFFSET {count_index};'
                table_data = self.select(sql)
                file_name = f'{table_name}.{count_index + 1}-{count_index + limit_count}.txt'
                with open(os.path.join(data_path, file_name), "w", encoding="utf-8") as file:
                    file.write(json.dumps(table_data, indent=2, ensure_ascii=False, cls=DateTimeJson))


class TableMap:
    """
    表映射关系
    """

    def __init__(self):
        self.table = {}
        self.field = {}

    def set_table(self, left_table, right_table=None):
        if right_table is None:
            self.table[left_table] = left_table
        else:
            self.table[left_table] = right_table
            self.table[right_table] = left_table

    def set_field(self, left_field, right_field=None):
        self.field[left_field] = right_field

    @staticmethod
    def create_table(left_table_name: str, right_table_name: str, field_dict: dict):
        table_map = TableMap()
        table_map.set_table(left_table_name, right_table_name)
        for left_field, right_field in field_dict.items():
            table_map.set_field(left_field, right_field)
        return table_map


class FieldMap:
    """
    字段映射关系
    """

    def __init__(self):
        self.tableLeftName = None
        """ 左表名称 """
        self.tableLeftMap = {}
        """ 左表映射字段 """
        self.tableLeftKey = set()
        """ 左表主键 """

        self.tableRightName = None
        """ 右表名称 """
        self.tableRightMap = {}
        """ 右表映射字段 """
        self.tableRightKey = set()
        """ 右表主键 """
        self.key = {}
        """ 主键映射 """

    def init_table_map(self, table_filed: TableInfo, table_map: TableMap = None):
        """
        初始化表映射关系
        :param table_filed: 映射字段
        :param table_map:映射关系
        """
        if table_map is None:
            table_map = TableMap()
        key_set = set()
        for field in table_filed.field:
            self.tableLeftMap[field.name.lower()] = field.name.lower()
            self.tableRightMap[field.name.lower()] = field.name.lower()
            if field.key:
                key_set.add(field.name.lower())
                self.key[field.name.lower()] = field.name.lower()
                self.tableLeftKey.add(field.name.lower())
                self.tableRightKey.add(field.name.lower())

        for field_key, field_value in table_map.field.items():
            self.tableLeftMap[field_key.lower()] = field_value.lower()
            if field_key.lower() in key_set:
                self.key[field_key.lower()] = field_value.lower()
                self.key[field_value.lower()] = field_key.lower()
                self.tableRightKey.add(field_value.lower())
                self.tableRightKey.remove(field_key.lower())

            if field_key.lower() in self.tableRightMap:
                del self.tableRightMap[field_key.lower()]
            self.tableRightMap[field_value.lower()] = field_key.lower()

    def line_to_key(self, line_dict, line_index, is_left=True):
        """
        生成左表或者右表的唯一标识
        :param line_dict:当前数据
        :param line_index:当前数据下标
        :param is_left:是否是左表
        :return:当前数据唯一标识
        """
        line_str = ""
        if is_left:
            for line_key in self.tableLeftKey:
                line_str += f'| {line_dict[line_key]} |'
        else:
            for line_key in self.tableLeftKey:
                line_str += f'| {line_dict[self.key[line_key]]} |'
        if line_str == "":
            line_str = line_index
        return line_str

    def list_to_dict(self, list_data, is_left=True):
        """
        将list转换成字典以方便唯一标识符确认
        :param list_data: 列表
        :param is_left: 是否是左表
        :return: 字典
        """
        data_dict = {}
        count_index = 0
        for line_dict in list_data:
            count_index += 1
            data_key = self.line_to_key(line_dict, count_index, is_left)
            data_dict[data_key] = line_dict
        return data_dict

    def compare_line(self, left_dict: dict, right_dict: dict):
        """
        比较两者持有数据是否一致
        :param left_dict: 左表数据
        :param right_dict: 右表数据
        :return: True:一致/False:不一致
        """
        different_data = []
        different_flag = True
        for left_field, left_value in left_dict.items():
            right_field = self.tableLeftMap[left_field]
            right_value = right_dict[right_field]
            if right_value != left_value:
                different_flag = False
                different_data.append(f'{left_field} : {left_value} != {right_field} : {right_value}')
        return different_flag, different_data

    def get_key_data(self, data_line, is_left=True):
        """
        生成主键对应的字段列
        :param data_line:数据
        :param is_left: 是否是左表
        :return: 字符串
        """
        line_str = ""
        table_key = self.tableRightKey
        if is_left:
            table_key = self.tableLeftKey
        for key in table_key:
            line_str += f'{key} : {data_line[key]},'
        return line_str

    def compare_data(self, data_left, data_right):
        """
        比较两个数据不同之处
        :param data_left:左表的数据
        :param data_right: 右表的数据
        :return: 错误信息
        """
        error_list = []
        left_len = len(data_left)
        right_len = len(data_right)
        if left_len != right_len:
            error_list.append(f"双方数据行数不同，左行数：{left_len},右行数:{right_len}")

        left_dict = self.list_to_dict(data_left)
        right_dict = self.list_to_dict(data_right, False)

        for left_key, left_value in left_dict.items():
            right_value = right_dict.get(left_key)
            if right_value is not None:
                result, error_field = self.compare_line(left_value, right_value)
                if result is False:
                    error_list.append(f'左表与右表数据不同，左表主键\t{self.get_key_data(left_value)}\t 不同的字段{error_field}')
            else:
                error_list.append(f'左表构成的主键在右表不存在，构成的主键信息\t{self.get_key_data(left_value)}')

        for right_key, right_value in right_dict.items():
            left_value = left_dict.get(right_key)
            if left_value is not None:
                result, error_field = self.compare_line(left_value, right_value)
                if result is False:
                    error_list.append(f'右表与左表数据不同，右表主键\t{self.get_key_data(right_value, False)}\t 不同的字段{error_field}')
            else:
                error_list.append(f'右表构成的主键在左表不存在，构成的主键信息\t{self.get_key_data(right_value, False)}')

        return error_list


class NodeDatabase:
    """
    节点下的表信息
    """

    def __init__(self, node_path):
        self.node_path = node_path
        """ 当前节点所在的路径信息 """
        self.table = {}
        """ 当前节点下持有的表 """
        self.structure = {}
        """ 当前节点下的表结构 """

        # 获取表数据
        data_path = os.path.join(node_path, "data")
        for node_file in os.listdir(data_path):
            file_path = os.path.join(data_path, node_file)
            if os.path.isfile(file_path):
                file_info = node_file.split(".")
                if len(file_info) == 3:
                    if file_info[0] not in self.table:
                        self.table[file_info[0]] = []
                    self.table[file_info[0]].append(file_path)
        # 获取表结构
        structure_path = os.path.join(node_path, "structure")
        for node_file in os.listdir(structure_path):
            file_path = os.path.join(structure_path, node_file)
            if os.path.isfile(file_path):
                file_info = node_file.split(".")
                if len(file_info) == 3:
                    self.structure[file_info[0]] = file_path

    def load_data(self, table_name) -> (list, TableInfo):
        """
        读取文件中的数据
        :param table_name: 表名称
        :return: 文件中的列表
        """
        table_data = []
        for path in self.table.get(table_name):
            data = open(path, "r", encoding="utf-8").read().lower()
            table_data.extend(json.loads(data))
        structure = json.load(open(self.structure.get(table_name), "r", encoding="utf-8"))
        return table_data, TableInfo.create_table(structure)

    def get_table(self) -> (str, list, TableInfo):
        """
        迭代获取吧表信息
        :return: 表名称，表数据，结构
        """
        for table_name, table_data in self.table.items():
            yield table_name, *self.load_data(table_name)

    def compared_table(self, table_name, node_info, table_map: TableMap = None):
        """
        比较两表
        :param table_name:表名称
        :param node_info: 另一节点
        :param table_map:映射关系
        :return: 自身
        """
        node_data_1, table_info_1 = self.load_data(table_name)

        if table_map is None:
            if table_name not in node_info.table:
                return [f'{table_name}该表另一方不存']
            node_data_2, table_info_2 = node_info.load_data(table_name)
        else:
            if table_map.table.get(table_name) not in node_info.table:
                return [f'{table_map.table.get(table_name)}该表另一方不存']
            node_data_2, table_info_2 = node_info.load_data(table_map.table.get(table_name))
        table_map_obj = FieldMap()
        table_map_obj.init_table_map(table_info_1, table_map)
        result = table_map_obj.compare_data(node_data_1, node_data_2)
        if len(result) > 0:
            result.insert(0, f'{table_name}存在不一致行为')
        return result


class JsonDatabase:
    """
    存储化的json处理
    """

    def __init__(self, root_path):
        """
        :param root_path:跟路径
        """
        path_list = os.path.split(root_path)
        self.database = path_list[-1]
        """ 数据库名称 """
        self.node_tag = {}
        for node_dir in os.listdir(root_path):
            if os.path.isdir(os.path.join(root_path, node_dir)):
                self.node_tag[node_dir] = NodeDatabase(os.path.join(root_path, node_dir))

    def compared_node(self, tag_1, tag_2):
        """
        对比两个节点
        :param tag_1:节点1
        :param tag_2:节点2
        :return:对比信息
        """
        left_tag = self.node_tag.get(tag_1)
        right_tag = self.node_tag.get(tag_2)
        if left_tag is None or right_tag is None:
            return [f'{tag_1},{tag_2} 这些节点中其中一个不存在']

        error_list = []
        for left_table_name, left_data_list in left_tag.table.items():
            error_list.extend(left_tag.compared_table(left_table_name, right_tag))
        return error_list

    def compared_database(self, tag_1: str, database_2, tag_2: str, table_map_all: dict):
        """
        对比两个库
        :param tag_1:要对比的版本
        :param database_2: 另一方要对比的库
        :param tag_2: 另一方要对比的版本
        :param table_map_all: 映射关系
        :return: 不同信息
        """
        left_tag = self.node_tag.get(tag_1)
        right_tag = database_2.node_tag.get(tag_2)
        if left_tag is None or right_tag is None:
            return [f'{tag_1},{tag_2} 这些节点中其中一个不存在']
        error_list = []
        for left_table_name, left_data_list in left_tag.table.items():
            error_list.extend(left_tag.compared_table(left_table_name, right_tag, table_map_all.get(left_table_name)))
        return error_list
