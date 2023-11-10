import copy
import json
import os
from typing import List, Dict

from src.analsis.AnalysisConfig import AnalysisConfig
from src.java.CodeConfig import CodeConfig, ManyToMany
from src.util.chiyaUtil import StringUtil, CollectionUtil, JsonUtil


class MultiTableParser:

    @staticmethod
    def parsing_relation(index_table: Dict[str, CodeConfig], source_table: Dict[str, CodeConfig], one_to_unknown: Dict[str, str], match_type):
        """
        解析关系
        :param index_table : 索引表结构
        :param source_table:原本表信息
        :param one_to_unknown:操作的对象
        :param match_type: 一对一或一对多
        """
        for one_key, other_key_set in one_to_unknown.items():
            for other_key in other_key_set:
                one_table, one_column = one_key.split(".")
                other_table, other_column = other_key.split(".")

                # 从原始副本中获取表,不然会无限
                config_json = JsonUtil.to_json(source_table.get(other_table))
                new_config = CodeConfig.get_code_config(json.loads(config_json))

                if match_type == "one_to_one":
                    new_config.baseInfo.foreignKey = one_column
                    index_table[one_table].baseInfo.oneToOne.append(new_config)
                if match_type == "ont_to_many":
                    new_config.baseInfo.foreignKey = other_column
                    index_table[one_table].baseInfo.oneToMany.append(new_config)

    @staticmethod
    def scan_relation(tables: List[CodeConfig], unknown_to_unknown):
        """
        扫描配置关系
        :param config:配置
        :param tables: 表
        :param unknown_to_unknown:扫描结果容器
        """
        for code_config in tables:
            key = code_config.baseInfo.key.field
            # 标准id起名补全，和非id起名
            if key.lower() in ["id", "id_"] or code_config.baseInfo.tableName not in key:
                # 下划线替换
                key = f'{code_config.baseInfo.tableName}_{key}'

            for other in tables:
                for attr in other.baseInfo.attr:
                    # 如果是主键在其他表中的字段出现，则键入待分类的关系中
                    if StringUtil.is_string_tail(attr.field, key, True):
                        CollectionUtil.dict_set(unknown_to_unknown, f"{code_config.baseInfo.tableName}.{code_config.baseInfo.key.field}", f"{other.baseInfo.tableName}.{attr.field}")

    @staticmethod
    def parsing_many_to_many(index_table: Dict[str, CodeConfig], source_table: Dict[str, CodeConfig]):
        """
        多对多关系映射处理
        :param index_table: 配置
        :param source_table:无侵入的配置
        """
        for table_name, code_config in index_table.items():

            # 只有一对一在1个以上才会有多对多关系
            if code_config.baseInfo.oneToOne and len(code_config.baseInfo.oneToOne) > 1:
                list_one_to_one = code_config.baseInfo.oneToOne
                # 双重循环遍历是否是真正的多对多
                for one_config in list_one_to_one:
                    for other_config in list_one_to_one:
                        if one_config.baseInfo.foreignKey != other_config.baseInfo.foreignKey:
                            # 如果i主键在j表中的字段出现，则键无法构成多对多关系
                            key = one_config.baseInfo.key.field
                            # id是默认id的情况
                            if key == "id":
                                key = f'{one_config.baseInfo.tableName}_{key}'
                            if other_config.baseInfo.check_key_in_attr(key):
                                continue

                            key = other_config.baseInfo.key.field
                            # id是默认id的情况
                            if key == "id":
                                key = f'{other_config.baseInfo.tableName}_{key}'
                            # 如果j主键在i表中的字段出现，则键无法构成多对多关系
                            if one_config.baseInfo.check_key_in_attr(key):
                                continue

                            # 装配
                            many_to_many = ManyToMany()
                            # 迭代的外层的是作TO表，只有TO表中存在两个以上的一对一关系，则肯定是中间表，
                            many_to_many.to = CodeConfig.get_code_config(json.loads(JsonUtil.to_json(source_table.get(code_config.baseInfo.tableName))))
                            # 在多个多表关系中，需要映射多个外键，故需要由to类进行管理
                            many_to_many.to.baseInfo.foreignKey = one_config.baseInfo.foreignKey
                            # 选择other当many一方
                            many_to_many.many = CodeConfig.get_code_config(json.loads(JsonUtil.to_json(source_table.get(other_config.baseInfo.tableName))))
                            many_to_many.many.baseInfo.foreignKey = other_config.baseInfo.foreignKey
                            # 添加关系，由于是双重循环，会在另一方为外层事，自动添加，不用担心只声明了一方的多对多关系
                            index_table.get(one_config.baseInfo.tableName).baseInfo.manyToMany.append(many_to_many)

    @staticmethod
    def create(tables: List[CodeConfig], config: AnalysisConfig):
        index_table = {}
        source_table = {}
        for table in tables:
            index_table[table.baseInfo.tableName] = table
            source_table[table.baseInfo.tableName] = CodeConfig.get_code_config(json.loads(JsonUtil.to_json(table)))

        # 那些表采用多表装配，不装配直接移除
        unknown_to_unknown = {}
        one_to_many = {}
        one_to_one = {}
        # 扫描表信息，开启关系扫描，扫描抉择在此
        MultiTableParser.scan_relation(tables, unknown_to_unknown)

        # 以上为自动扫描区
        # 转义配置中的一对一，一对一互相持有
        if config.one_to_one:
            for one, other in config.one_to_one.items():
                CollectionUtil.dict_set(one_to_one, one, other)
                CollectionUtil.dict_set(one_to_one, other, one)
        # 转义配置中的一对多
        if config.one_to_many:
            for one, other in config.one_to_many.items():
                CollectionUtil.dict_set(one_to_many, one, other)

        # 以上为配置文件装配
        # 如果在一对一中一配置，则去除查找到的
        for one in one_to_one:
            for other in one_to_one[one]:
                if unknown_to_unknown.get(one) and other in unknown_to_unknown.get(one):
                    unknown_to_unknown[one].remove(other)
        # 添加查找到的至一对多
        for one in unknown_to_unknown:
            for other in unknown_to_unknown[one]:
                CollectionUtil.dict_set(one_to_many, one, other)
                # 反向添加一对一
                CollectionUtil.dict_set(one_to_one, other, one)

        # 装配至配置中
        # 根据列表中的关系描述，查找属性并封装，如果修改查找决策在上面修改
        # 下面代码仅仅是解析a.key=b.a_key的
        # 原始副本，但是装配的对象关系是在原始对象中

        MultiTableParser.parsing_relation(index_table, source_table, one_to_one, "one_to_one")
        MultiTableParser.parsing_relation(index_table, source_table, one_to_many, "ont_to_many")

        # 多对多关系映射处理
        # 判断标准，在中间表存在两个以上一对一，即当作中间表
        MultiTableParser.parsing_many_to_many(index_table, source_table)
        result: List[CodeConfig] = []
        for table_name, code_config in index_table.items():
            result.append(code_config)
        return result
