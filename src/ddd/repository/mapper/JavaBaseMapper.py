from src.ddd.util import JavaCode
from src.structure.CodeConfig import CodeConfig


class Page:
    """
    分页信息
    """

    @staticmethod
    def attribute(index="", msg=""):
        """
        方法参数
        :param index:下标
        :param msg:消息
        :return: None|方法参数字符串
        """

        return JavaCode.Attribute(f'@Param("page{index}") Page', f'page{index}', f"{msg}分页对象")

    @staticmethod
    def param(name, msg=""):
        """
        方法参数
        :param name:参数名
        :param msg:消息
        :return: None|方法参数字符串
        """

        return JavaCode.Attribute(f'@Param("{name}") Page', f'{name}', f"{msg}分页对象")


class ThisObject:
    """
    指代本类的信息
    """

    @staticmethod
    def attribute(config: CodeConfig, not_param=False):
        """
        方法参数
        :param config: 配置
        :param not_param :不需要@Param
        :return: None|方法参数字符串
        """
        if not_param:
            return JavaCode.Attribute(config.className, config.low_name(), f'{config.remark}对象')
        return JavaCode.Attribute(f'@Param("{config.low_name()}") {config.className}', f'{config.low_name()}', f'{config.remark}对象')


class ThisKey:
    """
    指代本类的信息
    """

    @staticmethod
    def attribute(config: CodeConfig, not_param=False):
        """
        方法参数
        :param config: 配置
        :param not_param :不需要@Param
        :return: None|方法参数字符串
        """
        if not_param:
            return JavaCode.Attribute(config.key.type, config.key.attr, f'{config.remark}的{config.key.remark}')
        return JavaCode.Attribute(f'@Param("{config.key.attr}") {config.key.type}', config.key.attr, f'{config.remark}的{config.key.remark}')


class InKey:
    """
    指代本类的信息
    """

    @staticmethod
    def attribute(config: CodeConfig):
        """
        方法参数
        :param config: 配置
        :return: None|方法参数字符串
        """
        return JavaCode.Attribute(f'@Param("list") List<{config.key.type}>', 'list', f'{config.remark}的{config.key.remark}列表')


class SaveObject:
    """
    指代本类的信息
    """

    @staticmethod
    def attribute(config: CodeConfig):
        """
        方法参数
        :param config: 配置
        :return: None|方法参数字符串
        """
        return JavaCode.Attribute(f'@Param("save{config.className}") {config.className}', f'save{config.className}', f'要保存的{config.remark}对象')


class ConditionObject:
    """
    指代本类的信息
    """

    @staticmethod
    def attribute(config: CodeConfig):
        """
        方法参数
        :param config: 配置
        :return: None|方法参数字符串
        """
        return JavaCode.Attribute(f'@Param("condition{config.className}") {config.className}', f'condition{config.className}', f'查询的{config.remark}条件对象')


class FuzzySearch:
    """
    模糊搜索处理类
    """

    @staticmethod
    def attribute(config: CodeConfig, index=""):
        """
        获取模糊搜索的方法参数
        :param config: 配置
        :param index : 参数索引
        :return: None|方法参数字符串
        """
        if config.createConfig.fuzzySearch.enable:
            if len(config.createConfig.fuzzySearch.data) != 0:
                return JavaCode.Attribute(f'@Param("{config.createConfig.fuzzySearch.value}{index}") String', f'{config.createConfig.fuzzySearch.value}{index}', f'模糊搜索内容')
        return None


class SplicingSQL:
    """
    sql语句注入项
    """

    @staticmethod
    def attribute(config: CodeConfig):
        """
        SQL语句拼接项参数
        :param config:配置
        :return: None|方法参数
        """
        if config.createConfig.splicingSQL.enable:
            return JavaCode.Attribute(f'@Param("{config.createConfig.splicingSQL.value}") String', f'{config.createConfig.splicingSQL.value}', f'拼接的SQL语句')
        return None


class CreateFile:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig):
        code = JavaCode.JavaCode(
            config.module.baseMapperInterface.path,
            config.module.baseMapperInterface.className,
            f'{config.remark}自动生成的mapper层，请勿在该接口进行新增修改'
        )
        code.is_class = False
        code.add_mate("@Mapper")
        code.add_import(config.package)
        code.add_import(f'java.util.List')
        code.add_import(f'chiya.core.base.page.Page')

        Insert.create(code, config)
        Delete.create(code, config)
        Update.create(code, config)
        Select.create(code, config)
        SelectOneToOne.create(code, config)
        SelectOneToMany.create(code, config)
        SelectManyToMany.create(code, config)
        SelectForeignKey.create(code, config)
        return code.create()


# 添加方法接口
class Insert:
    """
    插入的方法
    """

    @staticmethod
    def create(code: JavaCode.JavaCode, config: CodeConfig):
        """
        构建方法对象
        :param code:源码
        :param config: 配置
        """
        code.add_function(Insert.insert(config))
        code.add_function(Insert.insert_list(config))
        code.add_function(Insert.insert_or_update_by_unique(config))
        code.add_function(Insert.insert_or_update_by_where(config))
        code.add_function(Insert.insert_by_exist_where(config))
        code.add_function(Insert.insert_by_not_exist_where(config))

    @staticmethod
    def insert(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute("Integer", "i", "受影响行数"),
            f'insert{config.className}',
            f'添加{config.remark}',
            ThisObject.attribute(config, True)
        )
        function.is_interface = True
        return function

    @staticmethod
    def insert_list(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute("Integer", "i", "受影响行数"),
            f'insert{config.className}List',
            f'添加多个{config.remark}',
            JavaCode.Attribute(f'@Param("list") List<{config.className}>', 'list', f'{config.remark}列表'),
        )
        function.is_interface = True
        return function

    @staticmethod
    def insert_or_update_by_unique(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute("Integer", "i", "受影响行数"),
            f'insertOrUpdate{config.className}ByUnique',
            f'添加或更新{config.remark}，根据唯一性索引',
            ThisObject.attribute(config, True)
        )
        function.is_interface = True
        return function

    @staticmethod
    def insert_or_update_by_where(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute("Integer", "i", "受影响行数"),
            f'insertOrUpdate{config.className}ByWhere',
            f'添加或更新{config.remark}，根据查询条件',
            SaveObject.attribute(config),
            ConditionObject.attribute(config),
        )
        function.is_interface = True
        return function

    @staticmethod
    def insert_by_exist_where(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute("Integer", "i", "受影响行数"),
            f'insert{config.className}ByExistWhere',
            f'条件添加{config.remark}，查询条件存在的情况下',
            SaveObject.attribute(config),
            ConditionObject.attribute(config),
        )
        function.is_interface = True
        return function

    @staticmethod
    def insert_by_not_exist_where(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute("Integer", "i", "受影响行数"),
            f'insert{config.className}ByNotExistWhere',
            f'条件添加{config.remark}，查询条件不存在的情况下',
            SaveObject.attribute(config),
            ConditionObject.attribute(config),
        )
        function.is_interface = True
        return function


# 删除方法接口
class Delete:
    """
    删除的方法
    """

    @staticmethod
    def create(code: JavaCode.JavaCode, config: CodeConfig):
        """
        构建方法对象
        :param code:源码
        :param config: 配置
        """
        code.add_function(Delete.delete_by_id(config))
        code.add_function(Delete.delete_in_id(config))
        code.add_function(Delete.delete_by_id_and_where(config))
        code.add_function(Delete.delete(config))
        code.add_function(Delete.false_delete(config))

    @staticmethod
    def delete_by_id(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute("Integer", "i", "受影响行数"),
            f'delete{config.className}By{config.key.upper_name()}',
            f'根据{config.key.attr}真删{config.remark}',
            ThisKey.attribute(config, True)
        )
        function.is_interface = True
        return function

    @staticmethod
    def delete_in_id(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute("Integer", "i", "受影响行数"),
            f'delete{config.className}In{config.key.upper_name()}',
            f'根据{config.key.attr}列表真删{config.remark}',
            InKey.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def delete_by_id_and_where(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute("Integer", "i", "受影响行数"),
            f'delete{config.className}By{config.key.upper_name()}AndWhere',
            f'根据{config.key.attr}和其他条件真删{config.remark}',
            ThisKey.attribute(config),
            ThisObject.attribute(config),
            FuzzySearch.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def delete(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute("Integer", "i", "受影响行数"),
            f'delete{config.className}',
            f'根据条件真删{config.key.attr}',
            ThisObject.attribute(config),
            FuzzySearch.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def false_delete(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute("Integer", "i", "受影响行数"),
            f'falseDelete{config.className}By{config.key.upper_name()}',
            f'根据{config.key.attr}假删{config.remark}',
            ThisKey.attribute(config, True)
        )
        function.is_interface = True
        return function


# 更新方法接口
class Update:
    """
    更新的方法
    """

    @staticmethod
    def create(code: JavaCode.JavaCode, config: CodeConfig):
        """
        构建方法对象
        :param code:源码
        :param config: 配置
        """
        code.add_function(Update.update_by_id(config))
        code.add_function(Update.update_by_id_and_where(config))
        code.add_function(Update.update_by_not_repeat_where(config))
        code.add_function(Update.update(config))
        code.add_function(Update.update_set_null_by_id(config))

    @staticmethod
    def update_by_id(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute("Integer", "i", "受影响行数"),
            f'update{config.className}By{config.key.upper_name()}',
            f'根据{config.key.attr}修改{config.remark}',
            ThisObject.attribute(config, True)
        )
        function.is_interface = True
        return function

    @staticmethod
    def update_by_not_repeat_where(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute("Integer", "i", "受影响行数"),
            f'update{config.className}ByNotRepeatWhere',
            f'根据{config.key.attr}和查询条件不满足的情况下更新{config.remark}。说明：查询的记录不存在则更新',
            SaveObject.attribute(config),
            ConditionObject.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def update_by_id_and_where(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute("Integer", "i", "受影响行数"),
            f'update{config.className}By{config.key.upper_name()}AndWhere',
            f'根据{config.key.attr}和其他的条件更新{config.remark}',
            SaveObject.attribute(config),
            ConditionObject.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def update(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute("Integer", "i", "受影响行数"),
            f'update{config.className}',
            f'根据条件更新{config.remark}',
            SaveObject.attribute(config),
            ConditionObject.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def update_set_null_by_id(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute("Integer", "i", "受影响行数"),
            f'update{config.className}',
            f'记录{config.key.attr}设置其他字段为null，对象中字段不为Null则是要设置成null的字段',
            ThisObject.attribute(config, True)
        )
        function.is_interface = True
        return function


# 单表查接口
class Select:
    """
    单表查接口
    """

    @staticmethod
    def create(code: JavaCode.JavaCode, config: CodeConfig):
        """
        构建方法对象
        :param code:源码
        :param config: 配置
        """
        code.add_function(Select.select_by_id(config))
        code.add_function(Select.select_in_id(config))
        code.add_function(Select.select_in_id_and_where(config))
        code.add_function(Select.select_one(config))
        code.add_function(Select.select(config))
        code.add_function(Select.count(config))

    @staticmethod
    def select_by_id(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute(config.className, config.low_name(), config.remark),
            f'select{config.className}By{config.key.upper_name()}',
            f'根据{config.key.attr}查询{config.remark}',
            ThisKey.attribute(config, True)
        )
        function.is_interface = True
        return function

    @staticmethod
    def select_in_id(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute(f'List<{config.className}>', "list", f'{config.remark}列表'),
            f'select{config.className}In{config.key.upper_name()}',
            f'根据{config.key.attr}列表查询{config.remark}',
            InKey.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def select_in_id_and_where(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute(f'List<{config.className}>', "list", f'{config.remark}列表'),
            f'select{config.className}In{config.key.upper_name()}AndWhere',
            f'根据{config.key.attr}列表和其他条件查询{config.remark}',
            InKey.attribute(config),
            ThisObject.attribute(config),
            FuzzySearch.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def select_one(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute(config.className, config.low_name(), f'{config.remark}对象'),
            f'selectOne{config.className}',
            f'只查询一个{config.remark}',
            ThisObject.attribute(config),
            JavaCode.Attribute(f'@Param("index") Integer', f'index', "获取的下标值"),
            FuzzySearch.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def select(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute(f'List<{config.className}>', "list", f'{config.remark}列表'),
            f'select{config.className}',
            f'查询多个{config.remark}',
            ThisObject.attribute(config),
            Page.attribute(),
            FuzzySearch.attribute(config),
            SplicingSQL.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def count(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.Attribute("Integer", "i", "查询到的记录数"),
            f'count{config.className}',
            f'统计{config.remark}记录数',
            ThisObject.attribute(config),
            FuzzySearch.attribute(config),
        )
        function.is_interface = True
        return function


# 一对一接口
class SelectOneToOne:
    """
    单表查接口
    """

    @staticmethod
    def create(code: JavaCode.JavaCode, config: CodeConfig):
        """
        构建方法对象
        :param code:源码
        :param config: 配置
        """
        if len(config.oneToOne) == 0:
            return
        for one_to_one in config.oneToOne:
            code.add_import(one_to_one.package)
            code.add_function(SelectOneToOne.find_one_to_one(config, one_to_one))
            code.add_function(SelectOneToOne.count_find_one_to_one(config, one_to_one))
            code.add_function(SelectOneToOne.link_one_to_one(config, one_to_one))
            code.add_function(SelectOneToOne.query_one_to_one(config, one_to_one))
            code.add_function(SelectOneToOne.count_query_one_to_one(config, one_to_one))

    @staticmethod
    def find_one_to_one(config: CodeConfig, another: CodeConfig):
        # 一对一内联
        function = JavaCode.Function(
            "",
            JavaCode.Attribute(f'List<{config.className}>', "list", f'{config.remark}列表'),
            f'find{config.className}OneToOne{another.className}',
            f'内联一对一查询{another.remark}',
            ThisObject.attribute(config),
            ThisObject.attribute(another),
            Page.attribute(),
            FuzzySearch.attribute(config),
            FuzzySearch.attribute(another, "1"),
            SplicingSQL.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def count_find_one_to_one(config: CodeConfig, another: CodeConfig):
        # 一对一内联计数
        function = JavaCode.Function(
            "",
            JavaCode.Attribute(f'Integer', "i", f'查询到的记录数'),
            f'countFind{config.className}OneToOne{another.className}',
            f'内联一对一统计{config.remark}',
            ThisObject.attribute(config),
            ThisObject.attribute(another),
            FuzzySearch.attribute(config),
            FuzzySearch.attribute(another, "1"),
        )
        function.is_interface = True
        return function

    @staticmethod
    def link_one_to_one(config: CodeConfig, another: CodeConfig):
        # 一对一获取对方
        function = JavaCode.Function(
            "",
            JavaCode.Attribute(f'List<{another.className}>', "list", f'{another.remark}列表'),
            f'linkOneToOne{another.className}',
            f'内联一对一查询{config.remark}，只返回{another.remark}',
            ThisObject.attribute(config),
            ThisObject.attribute(another),
            Page.attribute(),
            FuzzySearch.attribute(config),
            FuzzySearch.attribute(another, "1"),
            SplicingSQL.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def query_one_to_one(config: CodeConfig, another: CodeConfig):
        # 一对一外联
        function = JavaCode.Function(
            "",
            JavaCode.Attribute(f'List<{config.className}>', "list", f'{config.remark}列表'),
            f'query{config.className}OneToOne{another.className}',
            f'外联一对一查询{another.remark}',
            ThisObject.attribute(config),
            ThisObject.attribute(another),
            Page.attribute(),
            Page.attribute("1"),
            FuzzySearch.attribute(config),
            FuzzySearch.attribute(another, "1"),
            SplicingSQL.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def count_query_one_to_one(config: CodeConfig, another: CodeConfig):
        # 一对一外联计数
        function = JavaCode.Function(
            "",
            JavaCode.Attribute(f'Integer', "i", f'查询到的记录数'),
            f'countQuery{config.className}OneToOne{another.className}',
            f'外联一对一统计{another.remark}',
            ThisObject.attribute(config),
            ThisObject.attribute(another),
            Page.attribute(),
            Page.attribute("1"),
            FuzzySearch.attribute(config),
            FuzzySearch.attribute(another, "1"),
        )
        function.is_interface = True
        return function


# 一对多接口
class SelectOneToMany:
    """
    一对多接口
    """

    @staticmethod
    def create(code: JavaCode.JavaCode, config: CodeConfig):
        """
        构建方法对象
        :param code:源码
        :param config: 配置
        """
        if len(config.oneToMany) == 0:
            return
        for one_to_many in config.oneToMany:
            code.add_import(one_to_many.package)
            code.add_function(SelectOneToMany.find_one_to_many(config, one_to_many))
            code.add_function(SelectOneToMany.count_find_one_to_many(config, one_to_many))
            code.add_function(SelectOneToMany.link_one_to_many(config, one_to_many))
            code.add_function(SelectOneToMany.query_one_to_many(config, one_to_many))
            code.add_function(SelectOneToMany.count_query_one_to_many(config, one_to_many))

    @staticmethod
    def find_one_to_many(config: CodeConfig, another: CodeConfig):
        # 一对一内联
        function = JavaCode.Function(
            "",
            JavaCode.Attribute(f'List<{config.className}>', "list", f'{config.remark}列表'),
            f'find{config.className}OneToMany{another.className}',
            f'内联一对多查询{another.remark}，双方均可分页',
            ThisObject.attribute(config),
            ThisObject.attribute(another),
            Page.param("onePage", config.remark),
            Page.param("manyPage", another.remark),
            FuzzySearch.attribute(config),
            FuzzySearch.attribute(another, "1"),
            SplicingSQL.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def count_find_one_to_many(config: CodeConfig, another: CodeConfig):
        # 一对一内联计数
        function = JavaCode.Function(
            "",
            JavaCode.Attribute(f'Integer', "i", f'查询到的记录数'),
            f'countFind{config.className}OneToMany{another.className}',
            f'内联一对多统计{config.remark}，双方均可分页',
            ThisObject.attribute(config),
            ThisObject.attribute(another),
            Page.param("onePage", config.remark),
            Page.param("manyPage", another.remark),
            FuzzySearch.attribute(config),
            FuzzySearch.attribute(another, "1"),
        )
        function.is_interface = True
        return function

    @staticmethod
    def link_one_to_many(config: CodeConfig, another: CodeConfig):
        # 一对一获取对方
        function = JavaCode.Function(
            "",
            JavaCode.Attribute(f'List<{another.className}>', "list", f'{another.remark}列表'),
            f'linkOneToMany{another.className}',
            f'内联一对多查询{config.remark}，只返回{another.remark}',
            ThisObject.attribute(config),
            ThisObject.attribute(another),
            Page.param("onePage", config.remark),
            Page.param("manyPage", another.remark),
            FuzzySearch.attribute(config),
            FuzzySearch.attribute(another, "1"),
            SplicingSQL.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def query_one_to_many(config: CodeConfig, another: CodeConfig):
        # 一对一外联
        function = JavaCode.Function(
            "",
            JavaCode.Attribute(f'List<{config.className}>', "list", f'{config.remark}列表'),
            f'query{config.className}OneToMany{another.className}',
            f'外联一对多查询{another.remark}',
            ThisObject.attribute(config),
            ThisObject.attribute(another),
            Page.param("onePage", config.remark),
            Page.param("manyPage", another.remark),
            FuzzySearch.attribute(config),
            FuzzySearch.attribute(another, "1"),
            SplicingSQL.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def count_query_one_to_many(config: CodeConfig, another: CodeConfig):
        # 一对一外联计数
        function = JavaCode.Function(
            "",
            JavaCode.Attribute(f'Integer', "i", f'查询到的记录数'),
            f'countQuery{config.className}OneToMany{another.className}',
            f'外联一对多统计{another.remark}，双方均可分页',
            ThisObject.attribute(config),
            ThisObject.attribute(another),
            Page.param("onePage", config.remark),
            Page.param("manyPage", another.remark),
            FuzzySearch.attribute(config),
            FuzzySearch.attribute(another, "1"),
            SplicingSQL.attribute(config)
        )
        function.is_interface = True
        return function


# 多对多接口
class SelectManyToMany:
    """
    多对多接口
    """

    @staticmethod
    def create(code: JavaCode.JavaCode, config: CodeConfig):
        """
        构建方法对象
        :param code:源码
        :param config: 配置
        """
        if len(config.manyToMany) == 0:
            return
        for many_to_many in config.manyToMany:
            code.add_function(SelectManyToMany.find_many_to_many(config, many_to_many.to, many_to_many.many))
            code.add_function(SelectManyToMany.query_many_to_many(config, many_to_many.to, many_to_many.many))

    @staticmethod
    def find_many_to_many(config: CodeConfig, to: CodeConfig, many: CodeConfig):
        # 内联多对多查询
        function = JavaCode.Function(
            "",
            JavaCode.Attribute(f'List<{config.className}>', "list", f'{config.remark}列表'),
            f'find{config.className}ManyToManyLink{to.className}On{many.className}',
            f'内联多对多查询{config.remark},根据{to.remark}联查{many.remark}',
            ThisObject.attribute(config),
            Page.attribute(),
            FuzzySearch.attribute(config),
            SplicingSQL.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def query_many_to_many(config: CodeConfig, to: CodeConfig, many: CodeConfig):
        # 外联多对多查询
        function = JavaCode.Function(
            "",
            JavaCode.Attribute(f'List<{config.className}>', "list", f'{config.remark}列表'),
            f'query{config.className}ManyToManyLink{to.className}On{many.className}',
            f'外联多对多查询{config.remark},根据{to.remark}联查{many.remark}',
            ThisObject.attribute(config),
            Page.attribute(),
            FuzzySearch.attribute(config),
            SplicingSQL.attribute(config)
        )
        function.is_interface = True
        return function


# 外键查接口
class SelectForeignKey:
    """
    外键查接口
    """

    @staticmethod
    def create(code: JavaCode.JavaCode, config: CodeConfig):
        """
        构建方法对象
        :param code:源码
        :param config: 配置
        """
        if len(config.oneToOne) == 0:
            return
        for one_to_one in config.oneToOne:
            code.add_function(SelectForeignKey.select_in_and_where(config, one_to_one))

    @staticmethod
    def select_in_and_where(config: CodeConfig, another: CodeConfig):
        # 查找外键是属于这个表中的那个属性
        attr = None
        for i in config.attr:
            if i.filed == another.foreignKey:
                attr = i
        if attr is None:
            return

            # 内联多对多查询
        function = JavaCode.Function(
            "",
            JavaCode.Attribute(f'List<{config.className}>', "list", f'{config.remark}列表'),
            f'select{config.className}In{attr.upper_name()}AndWhere',
            f'根据{attr.remark}列表和其他条件查询{config.remark}',
            JavaCode.Attribute(f'@Param("list") List<{attr.type}>', "list", f'{config.remark}的{attr.remark}列表'),
            ThisObject.attribute(config),
            FuzzySearch.attribute(config),
        )
        function.is_interface = True
        return function
