import json
import os
import time
from datetime import datetime, date
from typing import List, Dict

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


class DifferenceTable:

    def __init__(self, list_new=None, list_update=None, list_delete=None):
        """
        差异化数据
        :param list_new: 新增的
        :param list_update: 修改的
        :param list_delete: 删除的
        """
        if list_delete is None:
            list_delete = []
        if list_update is None:
            list_update = []
        if list_new is None:
            list_new = []
        self.list_new = list_new
        """ 新增的 """
        self.list_update = list_update
        """ 修改的 """
        self.list_delete = list_delete
        """ 删除的 """

    def new(self, data: dict):
        """
        添加新增的数据
        :param data:数据
        """
        self.list_new.append(data)

    def update(self, data: dict):
        """
        新增修改的数据
        :param data:数据
        """
        self.list_update.append(data)

    def delete(self, data: dict):
        """
        新增删除的数据
        :param data:数据
        """
        self.list_delete.append(data)


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


class IndexDict:

    def __init__(self):
        """
        多重索引字典
        """
        self.data = {}

    def put(self, scope, key, value):
        """
        添加数据
        :param scope:域
        :param key: 键
        :param value: 值
        :return:
        """
        if scope not in self.data:
            self.data[scope] = {}
        self.data[scope][key] = value

    def get(self, scope, key):
        """
        根据域获取值
        :param scope:域
        :param key: 值
        """
        if scope in self.data:
            return self.data[scope].get(key)
        return None

    def any_scope_get(self, key):
        """
        从任意域中获取
        :param key:键
        """
        for scope, data in self.data.items():
            if key in data:
                return scope, data[key]
        return None, None


class TableMap:
    """
    表映射关系
    """

    def __init__(self):
        self.leftName = None
        """ 左表名 """
        self.leftMap = {}
        """ 左表映射字段 """
        self.rightName = None
        """ 右表名 """
        self.rightMap = {}
        """ 右表映射字段 """

    @staticmethod
    def create_table(left_table_name: str, right_table_name: str, field_dict: dict):
        """
        构建映射关系
        :param left_table_name:左表名
        :param right_table_name: 右表名
        :param field_dict: 映射关系
        """
        table_map = TableMap()
        table_map.leftName = left_table_name
        table_map.rightName = right_table_name
        for left_field, right_field in field_dict.items():
            table_map.leftMap[left_field] = right_field
            table_map.rightMap[right_field] = left_field
        return table_map

    def turn_over(self):
        """
        左右翻转
        """
        self.leftName, self.rightName = self.rightName, self.leftName
        self.leftMap, self.rightMap = self.rightMap, self.leftMap


class FieldMap:
    """
    字段映射关系
    """

    def __init__(self, who_is_left):
        """
        字段映射关系
        :param who_is_left:那张是左表
        """
        self.leftName = None
        """ 左表名称 """
        self.leftMap = {}
        """ 左表映射字段 """
        self.leftKey = set()
        """ 左表主键 """

        self.rightName = None
        """ 右表名称 """
        self.rightMap = {}
        """ 右表映射字段 """
        self.rightKey = set()
        """ 右表主键 """
        self.rightToLeftKey = {}
        """ 右表到左表主键映射 """

        self.base_table_name = who_is_left
        """ 基准表 """

    @staticmethod
    def __init_table(left_map, right_map, key, left_key, right_key, table_filed: TableInfo, table_map: TableMap = None):
        """
        初始化表
        :param left_map: 左表字段
        :param right_map: 右表字段
        :param key: 主键
        :param left_key:左表主键
        :param right_key: 右表主键
        :param table_filed: 表字段
        :param table_map: 表映射关系
        """
        if table_map is None:
            table_map = TableMap()
        key_set = set()
        # 初始化映射关系，根据表结构初始化
        for field in table_filed.field:
            field_name = field.name.lower()
            left_map[field_name] = field_name
            right_map[field_name] = field_name
            if field.key:
                key[field_name] = field_name
                key_set.add(field_name)
                left_key.add(field_name)
                right_key.add(field_name)

        # 根据字段映射关系进行剔除
        for field_key, field_value in table_map.leftMap.items():
            left_name = field_key.lower()
            right_name = field_value.lower()
            left_map[left_name] = right_name
            # 是主键就双向装配，右表剔除之前初始化的主键名称
            if left_name in key_set:
                key[left_name] = right_name
                key[right_name] = left_name
                right_key.remove(left_name)
                right_key.add(right_name)
            # 删除初始化左表于右表的映射
            if left_name in right_map:
                del right_map[left_name]
            right_map[right_name] = left_name

    def _left_init(self, table_filed: TableInfo, table_map: TableMap = None):
        """
        键值对是左表的初始化
        :param table_filed: 表字段
        :param table_map:表映射
        :return:
        """
        self.__init_table(self.leftMap, self.rightMap, self.rightToLeftKey, self.leftKey, self.rightKey, table_filed, table_map)

    def _right_init(self, table_filed: TableInfo, table_map: TableMap = None):
        """
        键值对是左表的初始化
        :param table_filed: 表字段
        :param table_map:表映射
        :return:
        """
        self.__init_table(self.rightMap, self.leftMap, self.rightToLeftKey, self.rightKey, self.leftKey, table_filed, table_map)

    def init_table_map(self, table_filed: TableInfo, table_map: TableMap = None):
        """
        初始化表映射关系
        :param table_filed: 映射字段
        :param table_map:映射关系
        """
        if table_filed.name == self.base_table_name:
            self._left_init(table_filed, table_map)
        else:
            self._right_init(table_filed, table_map)

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
            for line_key in self.leftKey:
                line_str += f'<{line_dict[line_key]}>'
        else:
            for line_key in self.leftKey:
                # 需要根据左表的主键遍历，以保证获取顺序相同
                line_str += f'<{line_dict[self.rightToLeftKey[line_key]]}>'
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
            right_field = self.leftMap[left_field]
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
        table_key = self.rightKey
        if is_left:
            table_key = self.leftKey
        for key in table_key:
            line_str += f'{key} : {data_line[key]},'
        return line_str

    def get_difference_data(self, data_left, data_right) -> DifferenceTable:
        """
        比较两个数据不同之处
        :param data_left:左表的数据
        :param data_right: 右表的数据
        :return: 差异数据
        """
        difference_table = DifferenceTable()

        left_dict = self.list_to_dict(data_left)
        right_dict = self.list_to_dict(data_right, False)
        # 基于左表对比右表
        for left_key, left_value in left_dict.items():
            right_value = right_dict.get(left_key)
            if right_value is not None:
                result, error_field = self.compare_line(left_value, right_value)
                if result is False:
                    difference_table.update(right_value)
            else:
                difference_table.delete(left_value)

        for right_key, right_value in right_dict.items():
            left_value = left_dict.get(right_key)
            if left_value is None:
                difference_table.new(right_value)

        return difference_table


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
        :return: (表数据列表，表结构)
        """
        table_data = []
        for path in self.table.get(table_name):
            data = open(path, "r", encoding="utf-8").read().lower()
            table_data.extend(json.loads(data))
        structure = json.load(open(self.structure.get(table_name), "r", encoding="utf-8"))
        return table_data, TableInfo.create_table(structure)

    def get_table(self) -> (str, list, TableInfo):
        """
        迭代获取表信息
        :return: 表名称，表数据，结构
        """
        for table_name, table_data in self.table.items():
            yield table_name, *self.load_data(table_name)

    def difference_data(self, table_name, right_node_info, table_map: TableMap = None):
        """
        保存前后差异数据
        :param table_name:表名称
        :param right_node_info:另一个节点
        :param table_map:映射关系
        :return:NodeDatabase 存储信息
        """
        left_table_data, left_table_info = None, None
        table_map_obj = FieldMap(table_name)

        if table_name in self.table:
            left_table_data, left_table_info = self.load_data(table_name)
            table_map_obj.init_table_map(left_table_info, table_map)

        right_table_name = table_name
        if table_map is not None:
            right_table_name = table_map.rightName
        if right_table_name not in right_node_info.table:
            if left_table_data is None:
                raise ValueError(f'{table_name}表在双方节点中均不存在！！！')
            # 如果右表不存在与左表，说明删除
            return DifferenceTable(list_delete=left_table_data)

        right_table_data, right_table_info = right_node_info.load_data(right_table_name)
        if left_table_data is None:
            # 左表不存在，但右表存在，则是新增
            return DifferenceTable(list_new=right_table_data)

        difference = table_map_obj.get_difference_data(left_table_data, right_table_data)
        return difference


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

    def difference_node(self, tag_1, tag_2):
        """
        对比两个节点差异
        :param tag_1:节点1
        :param tag_2:节点2
        :return:对比信息
        """
        left_tag = self.node_tag.get(tag_1)
        right_tag = self.node_tag.get(tag_2)
        if left_tag is None or right_tag is None:
            raise ValueError(f'{tag_1}或{tag_2}其中一个或多个不存在')

        difference: Dict[str, DifferenceTable] = {}
        # 基于左侧对比右侧，得到删除的表
        for left_table_name, left_data_list in left_tag.table.items():
            difference[left_table_name] = left_tag.difference_data(left_table_name, right_tag)
        # 基于右侧对比左侧，得到新增的表
        for right_table_name, right_data_list in right_tag.table.items():
            if right_table_name not in left_tag.table:
                difference[right_table_name] = left_tag.difference_data(right_table_name, right_tag)
        return difference

    def difference_database(self, tag_1: str, database_2, tag_2: str, table_map_all: Dict[str, TableMap]):
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
            raise ValueError(f'{tag_1}或{tag_2}其中一个或多个不存在')

        index_dict = IndexDict()
        for table_name, table_map in table_map_all.items():
            index_dict.put("left", table_map.leftName, table_map)
            index_dict.put("right", table_map.rightName, table_map)

        difference: Dict[str, DifferenceTable] = {}
        right_difference = set()
        # 基于左侧对比右侧，得到删除的表
        for left_table_name, left_data_list in left_tag.table.items():
            scope, table_map = index_dict.any_scope_get(left_table_name)
            right_table_name = left_table_name
            if table_map is not None:
                right_difference.add(right_table_name)
                if scope == "right":
                    table_map.turn_over()
                # 等待翻转后再赋值
                right_table_name = table_map.rightName
            difference[right_table_name] = left_tag.difference_data(left_table_name, right_tag, table_map)
        # 根据右表映射左表
        for right_table_name, right_data_list in right_tag.table.items():
            scope, table_map = index_dict.any_scope_get(right_table_name)
            left_table_name = right_table_name
            if table_map is not None:
                left_table_name = table_map.leftName
            difference[right_table_name] = left_tag.difference_data(left_table_name, right_tag, table_map)
        return difference

    def save_difference(self, difference: Dict[str, DifferenceTable], save_tag_name):
        """
        保存差异
        :param difference: 差异集
        :param save_tag_name: 保存的标签名称
        """
        save_path = OSUtil.is_not_dir_create(os.getcwd(), self.database)
        save_path = OSUtil.is_not_dir_create(save_path, save_tag_name)
        data_path = OSUtil.is_not_dir_create(save_path, "data")
        OSUtil.is_not_dir_create(save_path, "structure")

        for table_name, data in difference.items():
            all_data = []
            all_data.extend(data.list_new)
            all_data.extend(data.list_update)
            all_data.extend(data.list_delete)
            file_name = f'{table_name}.{0}-{len(all_data)}.txt'
            with open(os.path.join(data_path, file_name), "w", encoding="utf-8") as file:
                file.write(json.dumps(all_data, indent=2, ensure_ascii=False, cls=DateTimeJson))
