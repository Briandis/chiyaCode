from src.ddd.util.XmlCode import Tag


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
        :param namespace:
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
    def __init__(self, test, data):
        """
        Insert标签块
        :param test:判断条件
        :param data:标签内值
        """
        super().__init__("if")
        self.add_attribute("test", test)
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

    def __init__(self, param="list", index="index", item="obj", separator=","):
        """
        Foreach标签块
        :param param:传入的参数名称
        :param index: 下标
        :param item: 当前迭代对象
        :param separator: 要清除的后缀
        """
        super().__init__("foreach")
        self.add_attribute("collection", param)
        self.add_attribute("index", index)
        self.add_attribute("item", item)
        self.add_attribute("separator", separator)


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


class Update(Tag):
    def __init__(self, name):
        """
        Update标签
        :param name:方法名称
        """
        super().__init__("update")
        self.add_attribute("id", name)


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
        self.add_attribute("resultMap", value)
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
