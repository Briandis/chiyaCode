import copy
import json
import os

from src.constant.ProtocolConstant import JsonKey
from src.constant.PublicConstant import Constant
from src.util import util, StringUtil


class CreateConfig:

    @staticmethod
    def check_key_in_attr(listAttribute, key):
        for attr in listAttribute:
            if StringUtil.is_string_tail_not_case(attr[JsonKey.attr.filed], key):
                return True
        return False

    @staticmethod
    def parsing_relation(tables, old_tables, one_to_unknown, type):
        """
        解析关系
        :param tables:操作表
        :param old_tables: 备份的表
        :param one_to_unknown:操作的对象
        :param type: 一对一或一对多
        """
        for myKey in one_to_unknown:
            myTable, myColumn = myKey.split(".")
            for otherForeignKey in one_to_unknown[myKey]:
                otherTable, otherColumn = otherForeignKey.split(".")

                table = tables.get(myTable)
                if table.get(type) is None:
                    table[type] = []

                # 从原始副本中获取表,不然会无限
                obj = copy.deepcopy(old_tables[otherTable])
                if type == JsonKey.oneToOne:
                    obj[JsonKey.foreignKey] = myColumn
                if type == JsonKey.oneToMany:
                    obj[JsonKey.foreignKey] = otherColumn
                table[type].append(obj)

    @staticmethod
    def scan_relation(config, tables, unknown_to_unknown):
        """
        扫描配置关系
        :param config:配置
        :param tables: 表
        :param unknown_to_unknown:扫描结果容器
        """
        if config.get(Constant.MULTI_TABLE):
            for table in tables:
                if JsonKey.key.self not in tables[table]:
                    continue
                key = tables[table][JsonKey.key.self][JsonKey.key.filed]
                # 标准id起名补全，和非id起名

                if key.lower() in ["id", "id_"] or tables[table][JsonKey.tableName] not in key:
                    key = util.if_return(config.get(Constant.UNDERSCORE_REPLACE), f'{table}_{key}', f'{table}{key}')

                for i in tables:
                    toTable = tables[i]
                    for attr in toTable[JsonKey.attr.self]:
                        # 如果是主键在其他表中的字段出现，则键入待分类的关系中
                        if StringUtil.is_string_tail_not_case(attr[JsonKey.attr.filed], key):
                            util.dict_set(unknown_to_unknown, f"{table}.{key}", f"{i}.{attr[JsonKey.attr.filed]}")

    @staticmethod
    def parsing_many_to_many(config, tables, old_tables):
        """
        多对多关系映射处理
        :param config: 配置
        :param tables: 表
        :param old_tables:备份的原始表
        """
        for tableName in tables:
            table = tables[tableName]
            # 只有一对一在1个以上才会有多对多关系
            if JsonKey.oneToOne in table and len(table[JsonKey.oneToOne]) > 1:
                listOneToOne = table[JsonKey.oneToOne]
                # 双重循环便利是否是真正的多对多
                for i in listOneToOne:
                    for j in listOneToOne:
                        if i[JsonKey.foreignKey] != j[JsonKey.foreignKey]:
                            # Id补全
                            i_table = tables[i[JsonKey.tableName]]
                            j_table = tables[j[JsonKey.tableName]]

                            # 如果i主键在j表中的字段出现，则键无法构成多对多关系
                            key = i_table[JsonKey.key.self][JsonKey.key.filed]
                            # id是默认id的情况
                            if key == "id":
                                key = util.if_return(config.get(Constant.UNDERSCORE_REPLACE),
                                                     f'{i_table[JsonKey.tableName]}_{key}',
                                                     f'{i_table[JsonKey.tableName]}{key}')
                            continue_flag = CreateConfig.check_key_in_attr(j_table[JsonKey.attr.self], key)
                            if continue_flag:
                                continue

                            key = j_table[JsonKey.key.self][JsonKey.key.filed]
                            # id是默认id的情况
                            if key == "id":
                                key = util.if_return(config.get(Constant.UNDERSCORE_REPLACE),
                                                     f'{j_table[JsonKey.tableName]}_{key}',
                                                     f'{i_table[JsonKey.tableName]}{key}')
                            # 如果j主键在i表中的字段出现，则键无法构成多对多关系
                            continue_flag = CreateConfig.check_key_in_attr(i_table[JsonKey.attr.self], key)
                            if continue_flag:
                                continue

                            bean_info = i_table
                            if bean_info.get(JsonKey.oneToMany) is None:
                                bean_info[JsonKey.oneToMany] = []
                            # 保存外键
                            to_obj = copy.deepcopy(old_tables.get(tableName))
                            to_obj[JsonKey.foreignKey] = i[JsonKey.foreignKey]
                            # 装配
                            if bean_info.get(JsonKey.manyToMany) is None:
                                bean_info[JsonKey.manyToMany] = []
                            bean_info[JsonKey.manyToMany].append({"to": to_obj, "many": copy.deepcopy(j)})

    @staticmethod
    def create(tables: dict, config: dict):
        # 那些表采用多表装配，不装配直接移除
        if config.get(Constant.MULTI_SCOPE):
            multi_scope = config.get(Constant.MULTI_SCOPE)
            for table in list(tables.keys()):
                if table not in multi_scope:
                    del tables[table]

        unknown_to_unknown = {}
        one_to_many = {}
        one_to_one = {}
        many_to_many = {}
        # 扫描表信息，开启关系扫描，扫描抉择在此
        CreateConfig.scan_relation(config, tables, unknown_to_unknown)

        # 以上为自动扫描区
        # 转义配置中的一对一，一对一互相持有
        if config.get(JsonKey.oneToOne):
            for i in config[JsonKey.oneToOne]:
                a, b = i.split("->")
                util.dict_set(one_to_one, a, b)
                util.dict_set(one_to_one, b, a)
        # 转义配置中的一对多
        if config.get(JsonKey.oneToMany):
            for i in config[JsonKey.oneToMany]:
                a, b = i.split("->")
                util.dict_set(one_to_many, a, b)

        # 以上为配置文件装配
        # 如果在一对一中一配置，则去除查找到的
        for i in one_to_one:
            for j in one_to_one[i]:
                if unknown_to_unknown.get(i) and j in unknown_to_unknown.get(i):
                    unknown_to_unknown[i].remove(j)
        # 添加查找到的至一对多
        for i in unknown_to_unknown:
            for j in unknown_to_unknown[i]:
                util.dict_set(one_to_many, i, j)
                # 反向添加一对一
                util.dict_set(one_to_one, j, i)
        # 装配至配置中
        # 根据列表中的关系描述，查找属性并封装，如果修改查找决策在上面修改
        # 下面代码仅仅是解析a.key=b.a_key的
        # 原始副本，但是装配的对象关系是在原始对象中
        old_tables = copy.deepcopy(tables)

        CreateConfig.parsing_relation(tables, old_tables, one_to_one, JsonKey.oneToOne)
        CreateConfig.parsing_relation(tables, old_tables, one_to_many, JsonKey.oneToMany)

        # 多对多关系映射处理
        # 判断标准，在中间表存在两个以上一对一，即当作中间表
        CreateConfig.parsing_many_to_many(config, tables, old_tables)

    @staticmethod
    def save_model_json(tables: dict, create_list=None, not_create=None):
        """
        保存模型
        :param tables: 全部的配置
        :param create_list 生成列表
        :param not_create 不生成的
        """
        path = os.path.join(os.getcwd(), "config")
        if not os.path.exists(path):
            os.mkdir(path)

        if create_list is None:
            create_list = list(tables.keys())
        if not_create is None:
            not_create = []
        print("生成：", create_list)
        print("不生成：", not_create)
        for i in tables:
            if i in create_list and i not in not_create:
                with open(os.path.join(path, f"{i}.json"), "w", encoding="utf-8") as file:
                    file.write(json.dumps(tables[i], indent=2))
                print(f"{i}.json已保存")
