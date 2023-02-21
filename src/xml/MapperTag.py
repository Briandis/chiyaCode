from src.java.CodeConfig import CodeConfig, Field
from src.util.chiyaUtil import StringUtil
from src.xml.MapperUtil import MapperUtil
from src.xml.XmlCode import Tag


class Mapper(Tag):

    def __init__(self, namespace):
        """
        mapper的TAG
        :param namespace: 命名空间
        """
        super().__init__("mapper")
        self.add_attribute("namespace", namespace)


class XmlMapper:
    def __init__(self, mapper: Mapper):
        """
        构建XMLMapper
        :param mapper:
        """
        self.mapper = mapper

    def create(self):
        """
        生成完整的XML
        :return: XMLMapper格式
        """
        data = '<?xml version="1.0" encoding="UTF-8"?>\n'
        data += '<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">\n'
        data += self.mapper.create()
        return data


class Sql(Tag):

    def __init__(self, name):
        """
        SQL片段标签
        :param name: 名字
        """
        super().__init__("sql")
        self.add_attribute("id", name)


class Id(Tag):
    def __init__(self, field, attribute):
        """
        设置映射的字段
        :param field:数据库字段
        :param attribute:实体属性
        """
        super().__init__("id")
        self.add_attribute("column", field)
        self.add_attribute("property", attribute)
        self.line_tag = True


class Result(Tag):
    def __init__(self, field, attribute):
        """
        设置映射的字段
        :param field:数据库字段
        :param attribute:实体属性
        """
        super().__init__("result")
        self.add_attribute("column", field)
        self.add_attribute("property", attribute)
        self.line_tag = True


class ResultMap(Tag):

    def __init__(self, name, path):
        """
        ResultMap映射标签
        :param name: 名字
        :param path: 实体路径
        """
        super().__init__("resultMap")
        self.add_attribute("id", name)
        self.add_attribute("type", path)

    def set_id(self, field, attribute):
        """
        添加ID标签
        :param field:字段名称
        :param attribute: 属性
        :return: 自身
        """
        self.add_tag(Id(field, attribute))
        return self

    def set_result(self, field, attribute):
        """
        添加result标签
        :param field:字段名称
        :param attribute: 属性
        :return: 自身
        """
        self.add_tag(Result(field, attribute))
        return self

    def set_extends(self, extends):
        """
        添加继承属性
        :param extends:继承的类
        :return:自身
        """
        self.add_attribute("extends", extends)
        return self


class Collection(Tag):

    def __init__(self, name, path):
        """
        一对多的映射标签
        :param name: 属性名称
        :param path: 实体路径
        """
        super().__init__("collection")
        self.add_attribute("property", name)
        self.add_attribute("ofType", path)

    def set_id(self, field, attribute):
        """
        添加ID标签
        :param field:字段名称
        :param attribute: 属性
        :return: 自身
        """
        self.add_tag(Id(field, attribute))
        return self

    def set_result(self, field, attribute):
        """
        添加result标签
        :param field:字段名称
        :param attribute: 属性
        :return: 自身
        """
        self.add_tag(Result(field, attribute))
        return self


class Association(Tag):
    def __init__(self, name, path):
        """
        一对一的映射标签
        :param name: 属性名称
        :param path: 实体路径
        """
        super().__init__("association")
        self.add_attribute("property", name)
        self.add_attribute("javaType", path)

    def set_id(self, field, attribute):
        """
        添加ID标签
        :param field:字段名称
        :param attribute: 属性
        :return: 自身
        """
        self.add_tag(Id(field, attribute))
        return self

    def set_result(self, field, attribute):
        """
        添加result标签
        :param field:字段名称
        :param attribute: 属性
        :return: 自身
        """
        self.add_tag(Result(field, attribute))
        return self


class Insert(Tag):

    def __init__(self, name):
        """
        Insert标签块
        :param name:方法名称
        """
        super().__init__("insert")
        self.add_attribute("id", name)
        self.force_multiline = True

    def set_use_generated_keys(self, value):
        """
        useGeneratedKeys属性设置
        :param value: 值
        :return: 自身
        """
        self.add_attribute("useGeneratedKeys", value)
        return self

    def set_key_property(self, value):
        """
        keyProperty属性设置
        :param value:值
        :return:自身
        """
        self.add_attribute("keyProperty", value)
        return self

    def set_key_column(self, value):
        """
        keyColumn属性设置
        :param value:值
        :return:自身
        """
        self.add_attribute("keyColumn", value)
        return self


class If(Tag):
    def __init__(self, test, data=None):
        """
        Insert标签块
        :param test:判断条件
        :param data:标签内值
        """
        super().__init__("if")
        self.add_attribute("test", test)
        if data is not None:
            self.add_data(data)

    def set_if(self, test, data):
        """
        添加判断标签
        :param test:判断条件
        :param data: 内容
        :return: 自身
        """
        self.add_tag(If(test, data))
        return self


class Trim(Tag):
    def __init__(self, prefix="", suffix=","):
        """
        Insert标签块
        :param prefix:替换的字符
        :param suffix:后缀
        """
        super().__init__("trim")
        self.add_attribute("prefix", prefix)
        self.add_attribute("suffixOverrides", suffix)

    def set_if(self, test, data):
        """
        添加判断标签
        :param test:判断条件
        :param data: 内容
        :return: 自身
        """
        self.add_tag(If(test, data))
        return self


class Foreach(Tag):

    def __init__(self, param="list", index="index", item="obj", opens=None, separator=",", close=None):
        """
        Foreach标签块
        :param param:传入的参数名称
        :param index: 下标
        :param item: 当前迭代对象
        :param opens: 左闭合
        :param separator: 要清除的后缀
        :param close: 右闭合
        """
        super().__init__("foreach")
        self.add_attribute("collection", param)
        self.add_attribute("index", index)
        self.add_attribute("item", item)
        self.add_attribute("separator", separator)
        if opens is not None:
            self.add_attribute("open", opens)
        if close is not None:
            self.add_attribute("close", close)


class SelectKey(Tag):

    def __init__(self, key_property, key_column, result_type, order="BEFORE"):
        """
        SelectKey标签
        :param key_property:关联的字段
        :param key_column:表中的主键
        :param result_type:返回类型
        :param order:点前点后
        """
        super().__init__("selectKey")
        self.add_attribute("keyProperty", key_property)
        self.add_attribute("keyColumn", key_column)
        self.add_attribute("resultType", result_type)
        self.add_attribute("order", order)


class Where(Tag):
    def __init__(self):
        """
        where标签
        """
        super().__init__("where")

    def set_if(self, test, data):
        """
        添加判断标签
        :param test:判断条件
        :param data: 内容
        :return: 自身
        """
        self.add_tag(If(test, data))
        return self


class Delete(Tag):
    def __init__(self, name):
        """
        Delete标签
        :param name:方法名称
        """
        super().__init__("delete")
        self.add_attribute("id", name)
        self.force_multiline = True


class Update(Tag):
    def __init__(self, name):
        """
        Update标签
        :param name:方法名称
        """
        super().__init__("update")
        self.add_attribute("id", name)
        self.force_multiline = True


class Set(Tag):
    def __init__(self):
        """
        Set标签
        """
        super().__init__("set")

    def set_if(self, test, data):
        """
        添加判断标签
        :param test:判断条件
        :param data: 内容
        :return: 自身
        """
        self.add_tag(If(test, data))
        return self


class Select(Tag):
    def __init__(self, name):
        """
        select标签
        :param name:方法名称
        """
        super().__init__("select")
        self.add_attribute("id", name)
        self.force_multiline = True

    def set_result_map(self, value):
        """
        设置返回的映射
        :param value:映射名称
        :return: 自身
        """
        self.add_attribute("resultMap", value)
        return self

    def set_result_type(self, value):
        """
        设置返回的类型
        :param value:映射名称
        :return: 自身
        """
        self.add_attribute("resultType", value)
        return self


class Include(Tag):
    def __init__(self, ref):
        """
        Include标签
        :param ref:引用的SQL标签
        """
        super().__init__("include")
        self.add_attribute("refid", ref)
        self.line_tag = True


class LineNote(Tag):
    def __init__(self, data):
        """
        单行注释块
        :param data: 注释内容
        """
        super().__init__("")
        self.is_note = True
        self.add_data(data)


class BlockTag:
    """
    常见可复用的结构标签
    """

    @staticmethod
    def field_if(field: Field, var_name=None, is_field=False, is_attr=True, start="", alias="", end=",", need_date=False) -> If:
        """
        根据字段生成IF块
        :param field:字段
        :param var_name:别名
        :param is_field: 内容是字段
        :param is_attr: 内容是属性
        :param start: 内容前置字符
        :param alias:别名
        :param end:内容结尾字符
        :param need_date:需要对日期处理
        :return: IF标签块
        """
        test = f'{field.attr}!=null'
        data = ""
        if var_name is not None:
            var_name += "."
            test = var_name + test
        else:
            var_name = ""
        if is_field:
            # <if test="x!=null">field,</if>
            data = f'{start}{alias}{field.field}{end}'
        if is_attr:
            # <if test="x!=null">#{attr},</if>
            data = f'{start}#{{{var_name}{field.attr}}}{end}'
        if is_field and is_attr:
            # <if test="x!=null">field = #{attr},</if>
            data = f'{start}{alias}{field.field} = #{{{var_name}{field.attr}}}{end}'
            if need_date and field.type == "Date":
                data = f'{start}DATE({alias}{field.field}) = DATE(#{{{var_name}{field.attr}}}{end})'

        return If(test, data)

    @staticmethod
    def field_if_tag(tag: Tag, code_config: CodeConfig, var_name=None, is_field=False, is_attr=True, start="", alias="", end=",", need_key=True):
        """
        生成if块
        :param tag: 标签
        :param code_config:配置文件
        :param var_name:别名
        :param is_field: 内容是字段
        :param is_attr: 内容是属性
        :param start: 内容前置字符
        :param alias:别名
        :param end:内容结尾字符
        :param need_key: 需要主键
        """
        now_tag = tag
        if var_name is not None:
            var_tag = If(f'{var_name}!=null', None)
            tag.add_tag(var_tag)
            now_tag = var_tag
        if code_config.baseInfo.key is not None and need_key:
            now_tag.add_tag(BlockTag.field_if(code_config.baseInfo.key, var_name, is_field, is_attr, start, alias, end))
        for field in code_config.baseInfo.attr:
            now_tag.add_tag(BlockTag.field_if(field, var_name, is_field, is_attr, start, alias, end))

    @staticmethod
    def if_var_block(code_config: CodeConfig, var_name=None, is_field=False, is_attr=True, start="", alias="", end=",", need_key=True, need_date=False) -> If:
        """
        构建一个IF标签，并且加入IF判断空，当IF标签判断字段的时候
        <if test="attr!=null"> field, </if>
        :param code_config:配置文件
        :param var_name:别名
        :param is_field: 内容是字段
        :param is_attr: 内容是属性
        :param start: 内容前置字符
        :param alias:别名
        :param end:内容结尾字符
        :param need_key: 需要主键
        :param need_date:需要进行日期处理
        :return:IF块
        """
        if var_name is None:
            var_name = code_config.module.entity.low_name()
        now_tag = If(f'{var_name}!=null', None)
        if code_config.baseInfo.key is not None and need_key:
            now_tag.add_tag(BlockTag.field_if(code_config.baseInfo.key, var_name, is_field, is_attr, start, alias, end, need_date))
        for field in code_config.baseInfo.attr:
            now_tag.add_tag(BlockTag.field_if(field, var_name, is_field, is_attr, start, alias, end, need_date))
        return now_tag

    @staticmethod
    def trim_if_block(code_config: CodeConfig, var_name=None, is_field=False, is_attr=True, start="", end=",", need_key=True) -> Trim:
        """
        构建一个Trim标签，并且加入IF判断空，当IF标签判断字段的时候
        <if test="attr!=null"> field, </if>
        :param code_config:配置文件
        :param var_name:别名
        :param is_field: 内容是字段
        :param is_attr: 内容是属性
        :param start: 内容前置字符
        :param end:内容结尾字符
        :param need_key: 需要主键
        :return:Trim块
        """

        trim = Trim()
        BlockTag.field_if_tag(trim, code_config, var_name, is_field, is_attr, start, "", end, need_key)
        return trim

    @staticmethod
    def set_if_block(code_config: CodeConfig, var_name=None, is_field=True, is_attr=True, start="", end=",", need_key=False) -> Set:
        """
        构建一个Set标签，并且加入IF判断空，当IF标签判断字段的时候
        <if test="attr!=null"> field, </if>
        :param code_config:配置文件
        :param var_name:别名
        :param is_field: 内容是字段
        :param is_attr: 内容是属性
        :param start: 内容前置字符
        :param end:内容结尾字符
        :param need_key:需要主键
        :return:Set块
        """
        set_tag = Set()
        BlockTag.field_if_tag(set_tag, code_config, var_name, is_field, is_attr, start, "", end, need_key)
        return set_tag

    @staticmethod
    def foreach_block(code_config: CodeConfig, param="list", index="index", item="obj", separator=",", need_key=True) -> Foreach:
        """
        生成迭代块
        :param code_config:配置
        :param param: 参数名称
        :param index: 下标
        :param item: 迭代对象名称
        :param separator: 拼接符
        :param need_key:需要主键
        :return: 迭代标签
        """
        foreach = Foreach(param, index, item, separator=separator)
        foreach.add_data("(")
        if code_config.baseInfo.key is not None and need_key:
            foreach.add_data(f'\t#{{{item}.{code_config.baseInfo.key.attr}}},')
        for field in code_config.baseInfo.attr:
            foreach.add_data(f'\t#{{{item}.{field.attr}}},')
        foreach.add_data(")")
        return foreach

    @staticmethod
    def where_if_block(code_config: CodeConfig, var_name=None, need_var=False, alias="", need_data=True) -> Where:
        """
        构建一个Where标签，并且加入IF判断空，当IF标签判断字段的时候
        <if test="attr!=null"> field, </if>
        :param code_config:配置文件
        :param var_name:别名
        :param need_var:自动生成var_name的名称
        :param alias:表别名
        :param need_data:需要日期处理
        :return:where块
        """
        if need_var and var_name is None:
            var_name = code_config.module.entity.low_name()
        where = Where()
        where.add_tag(BlockTag.if_select_block(code_config, var_name, need_var, alias, need_data=need_data))
        return where

    @staticmethod
    def fuzzy_search(code_config: CodeConfig, sql_tag: Tag, table="", suffix=""):
        """
        添加sql块
        :param code_config:配置
        :param sql_tag: 要添加的tag
        :param table: 表前缀
        :param suffix: 关键字后缀
        """
        if code_config.createConfig.fuzzySearch.enable:
            if code_config.createConfig.fuzzySearch.data is None or len(code_config.createConfig.fuzzySearch.data) == 0:
                return
            if StringUtil.is_not_null(table):
                table += "."

            if_tag = If(f'{code_config.createConfig.fuzzySearch.get_value()}{suffix}!=null', "AND (").indent_increase()
            flag = 0
            for field in code_config.createConfig.fuzzySearch.data:
                if flag == 0:
                    if_tag.add_data(f'{table}{field} LIKE #{{{code_config.createConfig.fuzzySearch.get_value()}{suffix}}}')
                    flag = 1
                else:
                    if_tag.add_data(f'OR {table}{field} LIKE #{{{code_config.createConfig.fuzzySearch.get_value()}{suffix}}}')
            if_tag.indent_decrease()
            if_tag.add_data(")")
            if_tag.force_multiline = True
            sql_tag.add_tag(if_tag)

    @staticmethod
    def if_select_block(code_config: CodeConfig, var_name=None, need_var=False, alias="", need_data=True):
        """
        查询专用的if块
        :param code_config:配置
        :param var_name: 变量名称
        :param need_var: 需要变量
        :param alias: 指定表的名称
        :param need_data:需要日期处理
        :return: if标签块
        """
        if need_var and var_name is None:
            var_name = code_config.module.entity.low_name()
        if StringUtil.is_not_null(alias):
            alias += "."
        return BlockTag.if_var_block(code_config, var_name, True, True, f"AND ", alias, "", need_date=need_data)

    @staticmethod
    def splicing_sql(code_config: CodeConfig, sql_tag: Tag, suffix=""):
        """
        SQL注入项
        :param code_config:配置
        :param sql_tag: 添加的tag
        :param suffix: 后缀
        """
        if code_config.createConfig.splicingSQL.enable:
            sql_tag.add_tag(If(
                f'{code_config.createConfig.splicingSQL.get_value()}{suffix}!=null',
                f'${{{code_config.createConfig.splicingSQL.get_value()}{suffix}}}'
            ))

    @staticmethod
    def page_block(page="page"):
        """
        分页
        :param page: 名称
        :return 分页if块
        """
        return If(f'{page}!=null', f'LIMIT #{{{page}.count}} OFFSET #{{{page}.start}}')

    @staticmethod
    def set_result(sql_Tag: Select, code_config: CodeConfig, other_config: CodeConfig = None, one_to_one=False, one_to_many=False, many_to_many=False):
        """
        设置返回类型
        :param sql_Tag:标签
        :param code_config:基础配置
        :param other_config: 其他配置
        :param one_to_one: 是否一对一
        :param one_to_many: 是否一对多
        :param many_to_many: 是否多对多
        """
        if code_config.createConfig.resultMap.enable:
            sql_Tag.set_result_map(MapperUtil.result_map_name(code_config, other_config, one_to_one, one_to_many, many_to_many))
        else:
            sql_Tag.set_result_type(code_config.module.entity.get_package())

    @staticmethod
    def add_include_tag(sql_tag: Tag, code_config: CodeConfig, other_config: CodeConfig = None):
        """
        添加多表查询中的参数
        :param sql_tag: 要添加的tag
        :param code_config: 本表配置
        :param other_config: 其他表配置
        """
        # 如果只引入一方的情况下
        if other_config is None:
            if code_config.baseInfo.need_sql_block():
                sql_tag.add_tag(Include(MapperUtil.sql_tag_name(code_config)))
            else:
                sql_tag.add_data("*")
        else:
            # 需要同时引入双方
            if other_config.baseInfo.need_sql_block():
                sql_tag.add_data(f'{code_config.baseInfo.tableName}.*,')
                sql_tag.add_tag(Include(MapperUtil.sql_tag_name(other_config)))
            else:
                sql_tag.add_data("*")
