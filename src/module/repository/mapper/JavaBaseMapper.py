from src.java import JavaCode
from src.java.CodeConfig import CodeConfig
from src.module.base.BaseApi import MapperApi, MapperApiNote


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
    def attribute(config: CodeConfig, not_param=False, other_config: CodeConfig = None):
        """
        方法参数 @Param("User") User user,
        :param config: 配置
        :param not_param :不需要@Param
        :param other_config:另一方配置，用于校验是否要生成另一个名字
        :return: None|方法参数字符串
        """
        suffix = ""
        if other_config and other_config.module.entity.low_name() == config.module.entity.low_name():
            # 同名模块，需要添加下标区分
            suffix = "1"

        attr_type = f'@Param("{config.module.entity.low_name()}{suffix}") {config.module.entity.className}'
        if not_param:
            attr_type = config.module.entity.className
        return JavaCode.Attribute(
            attr_type,
            f'{config.module.entity.low_name()}{suffix}',
            f'{config.module.entity.remark}对象'
        )


class ThisKey:
    """
    指代本类的信息
    """

    @staticmethod
    def attribute(config: CodeConfig, not_param=False):
        """
        方法参数 @Param("id") Integer id,
        :param config: 配置
        :param not_param :不需要@Param
        :return: None|方法参数字符串
        """
        attr_type = f'@Param("{config.baseInfo.key.attr}") {config.baseInfo.key.type}'
        if not_param:
            attr_type = config.baseInfo.key.type

        return JavaCode.Attribute(
            attr_type,
            config.baseInfo.key.attr,
            f'{config.module.entity.remark}的{config.baseInfo.key.remark}'
        )


class InKey:
    """
    指代本类的信息
    """

    @staticmethod
    def attribute(config: CodeConfig):
        """
        方法参数 @Param("list") List<Integer> list,
        :param config: 配置
        :return: None|方法参数字符串
        """
        return JavaCode.Attribute(
            f'@Param("list") List<{config.baseInfo.key.type}>',
            'list',
            f'{config.module.entity.remark}的{config.baseInfo.key.remark}列表'
        )


class SaveObject:
    """
    指代本类的信息
    """

    @staticmethod
    def attribute(config: CodeConfig):
        """
        方法参数 @Param("saveUser") User saveUser,
        :param config: 配置
        :return: None|方法参数字符串
        """
        return JavaCode.Attribute(
            f'@Param("save{config.module.entity.className}") {config.module.entity.className}',
            f'save{config.module.entity.className}',
            f'要保存的{config.module.entity.remark}对象'
        )


class ConditionObject:
    """
    指代本类的信息
    """

    @staticmethod
    def attribute(config: CodeConfig):
        """
        方法参数 @Param("conditionUser") User conditionUser,
        :param config: 配置
        :return: None|方法参数字符串
        """
        return JavaCode.Attribute(
            f'@Param("{config.get_class_name(condition=True)}") {config.module.entity.className}',
            f'{config.get_class_name(condition=True)}',
            f'查询的{config.module.entity.remark}条件对象'
        )


class FuzzySearch:
    """
    模糊搜索处理类
    """

    @staticmethod
    def attribute(config: CodeConfig, index=""):
        """
        获取模糊搜索的方法参数 @Param("keyword") String keyword,
        :param config: 配置
        :param index : 参数索引
        :return: None|方法参数字符串
        """
        if config.createConfig.fuzzySearch.enable:
            if config.createConfig.fuzzySearch.data is not None and len(config.createConfig.fuzzySearch.data) != 0:
                return JavaCode.Attribute(
                    f'@Param("{config.createConfig.fuzzySearch.get_value()}{index}") String',
                    f'{config.createConfig.fuzzySearch.get_value()}{index}',
                    f'模糊搜索内容'
                )
        return None


class SplicingSQL:
    """
    sql语句注入项
    """

    @staticmethod
    def attribute(config: CodeConfig):
        """
        SQL语句拼接项参数 @Param("splicingSQL") String splicingSQL,
        :param config:配置
        :return: None|方法参数
        """
        if config.createConfig.splicingSQL.enable:
            return JavaCode.Attribute(
                f'@Param("{config.createConfig.splicingSQL.get_value()}") String',
                f'{config.createConfig.splicingSQL.get_value()}',
                f'拼接的SQL语句'
            )
        return None


class BaseMapperJavaCode:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig):
        code = JavaCode.JavaCode(
            config.module.baseMapperInterface.path,
            config.module.baseMapperInterface.className,
            f'{config.module.entity.remark}自动生成的mapper层，请勿在该接口进行新增修改'
        )
        code.is_class = False
        code.add_mate(JavaCode.DefaultMate.Mapper())

        code.add_import(config.module.entity.get_package())
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
        """
        生成的样式：Integer insertUser(User user);
        :param config: 配置
        :return: 生成函数
        """
        function = JavaCode.Function(
            "",
            JavaCode.DefaultAttribute.MapperInteger,
            MapperApi.Insert.insert(config),
            MapperApiNote.Insert.insert(config),
            ThisObject.attribute(config, True)
        )
        function.is_interface = True
        return function

    @staticmethod
    def insert_list(config: CodeConfig):
        """
        生成的样式：Integer insertUserList(@Param("list") List<User> list);
        :param config: 配置
        :return: 生成函数
        """
        function = JavaCode.Function(
            "",
            JavaCode.DefaultAttribute.MapperInteger,
            MapperApi.Insert.insert_list(config),
            MapperApiNote.Insert.insert_list(config),
            JavaCode.Attribute(f'@Param("list") List<{config.module.entity.className}>', 'list', f'{config.module.entity.remark}列表'),
        )
        function.is_interface = True
        return function

    @staticmethod
    def insert_or_update_by_unique(config: CodeConfig):
        """
        生成的样式：Integer insertOrUpdateUserByUnique(User user);
        :param config: 配置
        :return: 生成函数
        """
        function = JavaCode.Function(
            "",
            JavaCode.DefaultAttribute.MapperInteger,
            MapperApi.Insert.insert_or_update_by_unique(config),
            MapperApiNote.Insert.insert_or_update_by_unique(config),
            ThisObject.attribute(config, True)
        )
        function.is_interface = True
        return function

    @staticmethod
    def insert_or_update_by_where(config: CodeConfig):
        """
        生成的样式：Integer insertOrUpdateUserByWhere(@Param("con") User user, @Param("save") User user);
        :param config: 配置
        :return: 生成函数
        """
        function = JavaCode.Function(
            "",
            JavaCode.DefaultAttribute.MapperInteger,
            MapperApi.Insert.insert_or_update_by_where(config),
            MapperApiNote.Insert.insert_or_update_by_where(config),
            SaveObject.attribute(config),
            ConditionObject.attribute(config),
        )
        function.is_interface = True
        return function

    @staticmethod
    def insert_by_exist_where(config: CodeConfig):
        """
        生成的样式：Integer insertUserByExistWhere(@Param("con") User user, @Param("save") User user);
        :param config: 配置
        :return: 生成函数
        """
        function = JavaCode.Function(
            "",
            JavaCode.DefaultAttribute.MapperInteger,
            MapperApi.Insert.insert_by_exist_where(config),
            MapperApiNote.Insert.insert_by_exist_where(config),
            SaveObject.attribute(config),
            ConditionObject.attribute(config),
        )
        function.is_interface = True
        return function

    @staticmethod
    def insert_by_not_exist_where(config: CodeConfig):
        """
        生成的样式：Integer insertByNotExistWhere(@Param("con") User user, @Param("save") User user);
        :param config: 配置
        :return: 生成函数
        """
        function = JavaCode.Function(
            "",
            JavaCode.DefaultAttribute.MapperInteger,
            MapperApi.Insert.insert_by_not_exist_where(config),
            MapperApiNote.Insert.insert_by_not_exist_where(config),
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
        if config.baseInfo.key:
            code.add_function(Delete.delete_by_id(config))
            code.add_function(Delete.delete_in_id(config))
            code.add_function(Delete.delete_by_id_and_where(config))
        code.add_function(Delete.delete(config))

    @staticmethod
    def delete_by_id(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.DefaultAttribute.MapperInteger,
            MapperApi.Delete.delete_by_id(config),
            MapperApiNote.Delete.delete_by_id(config),
            ThisKey.attribute(config, True)
        )
        function.is_interface = True
        return function

    @staticmethod
    def delete_in_id(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.DefaultAttribute.MapperInteger,
            MapperApi.Delete.delete_in_id(config),
            MapperApiNote.Delete.delete_in_id(config),
            InKey.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def delete_by_id_and_where(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.DefaultAttribute.MapperInteger,
            MapperApi.Delete.delete_by_id_and_where(config),
            MapperApiNote.Delete.delete_by_id_and_where(config),
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
            JavaCode.DefaultAttribute.MapperInteger,
            MapperApi.Delete.delete(config),
            MapperApiNote.Delete.delete(config),
            ThisObject.attribute(config),
            FuzzySearch.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def false_delete(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.DefaultAttribute.MapperInteger,
            MapperApi.Delete.false_delete(config),
            MapperApiNote.Delete.false_delete(config),
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
        if config.baseInfo.key:
            code.add_function(Update.update_by_id(config))
            code.add_function(Update.update_by_not_repeat_where(config))
        code.add_function(Update.update(config))
        if config.baseInfo.key:
            code.add_function(Update.update_set_null_by_id(config))

    @staticmethod
    def update_by_id(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.DefaultAttribute.MapperInteger,
            MapperApi.Update.update_by_id(config),
            MapperApiNote.Update.update_by_id(config),
            ThisObject.attribute(config, True)
        )
        function.is_interface = True
        return function

    @staticmethod
    def update_by_id_and_where(config: CodeConfig):
        # 废弃
        function = JavaCode.Function(
            "",
            JavaCode.DefaultAttribute.MapperInteger,
            MapperApi.Update.update_by_id_and_where(config),
            MapperApiNote.Update.update_by_id_and_where(config),
            SaveObject.attribute(config),
            ConditionObject.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def update_by_not_repeat_where(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.DefaultAttribute.MapperInteger,
            MapperApi.Update.update_by_not_repeat_where(config),
            MapperApiNote.Update.update_by_not_repeat_where(config),
            SaveObject.attribute(config),
            ConditionObject.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def update(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.DefaultAttribute.MapperInteger,
            MapperApi.Update.update(config),
            MapperApiNote.Update.update(config),
            SaveObject.attribute(config),
            ConditionObject.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def update_set_null_by_id(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.DefaultAttribute.MapperInteger,
            MapperApi.Update.update_set_null_by_id(config),
            MapperApiNote.Update.update_set_null_by_id(config),
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
        if config.baseInfo.key:
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
            JavaCode.DefaultAttribute.self_class(config),
            MapperApi.Select.select_by_id(config),
            MapperApiNote.Select.select_by_id(config),
            ThisKey.attribute(config, True)
        )
        function.is_interface = True
        return function

    @staticmethod
    def select_in_id(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.DefaultAttribute.self_list_class(config),
            MapperApi.Select.select_in_id(config),
            MapperApiNote.Select.select_in_id(config),
            InKey.attribute(config)
        )
        function.is_interface = True
        return function

    @staticmethod
    def select_in_id_and_where(config: CodeConfig):
        function = JavaCode.Function(
            "",
            JavaCode.DefaultAttribute.self_list_class(config),
            MapperApi.Select.select_in_id_and_where(config),
            MapperApiNote.Select.select_in_id_and_where(config),
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
            JavaCode.DefaultAttribute.self_class(config),
            MapperApi.Select.select_one(config),
            MapperApiNote.Select.select_one(config),
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
            JavaCode.DefaultAttribute.self_list_class(config),
            MapperApi.Select.select(config),
            MapperApiNote.Select.select(config),
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
            MapperApi.Select.count(config),
            MapperApiNote.Select.count(config),
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
        if len(config.baseInfo.oneToOne) == 0:
            return
        for one_to_one in config.baseInfo.oneToOne:
            code.add_import(one_to_one.module.entity.get_package())
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
            JavaCode.DefaultAttribute.self_list_class(config),
            MapperApi.SelectOneToOne.find_one_to_one(config, another),
            MapperApiNote.SelectOneToOne.find_one_to_one(config),
            ThisObject.attribute(config),
            ThisObject.attribute(another, other_config=config),
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
            MapperApi.SelectOneToOne.count_find_one_to_one(config, another),
            MapperApiNote.SelectOneToOne.count_find_one_to_one(config),
            ThisObject.attribute(config),
            ThisObject.attribute(another, other_config=config),
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
            JavaCode.DefaultAttribute.self_class(another),
            MapperApi.SelectOneToOne.link_one_to_one(another),
            MapperApiNote.SelectOneToOne.link_one_to_one(config, another),
            ThisObject.attribute(config),
            ThisObject.attribute(another, other_config=config),
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
            JavaCode.DefaultAttribute.self_list_class(config),
            MapperApi.SelectOneToOne.query_one_to_one(config, another),
            MapperApiNote.SelectOneToOne.query_one_to_one(config),
            ThisObject.attribute(config),
            ThisObject.attribute(another, other_config=config),
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
            MapperApi.SelectOneToOne.count_query_one_to_one(config, another),
            MapperApiNote.SelectOneToOne.count_query_one_to_one(config),
            ThisObject.attribute(config),
            ThisObject.attribute(another, other_config=config),
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
        if len(config.baseInfo.oneToMany) == 0:
            return
        for one_to_many in config.baseInfo.oneToMany:
            code.add_import(one_to_many.module.entity.get_package())
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
            JavaCode.DefaultAttribute.self_list_class(config),
            MapperApi.SelectOneToMany.find_one_to_many(config, another),
            MapperApiNote.SelectOneToMany.find_one_to_many(another),
            ThisObject.attribute(config),
            ThisObject.attribute(another, other_config=config),
            Page.param("onePage", config.module.entity.remark),
            Page.param("manyPage", another.module.entity.remark),
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
            MapperApi.SelectOneToMany.count_find_one_to_many(config, another),
            MapperApiNote.SelectOneToMany.count_find_one_to_many(config),
            ThisObject.attribute(config),
            ThisObject.attribute(another, other_config=config),
            Page.param("onePage", config.module.entity.remark),
            Page.param("manyPage", another.module.entity.remark),
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
            JavaCode.DefaultAttribute.self_list_class(another),
            MapperApi.SelectOneToMany.link_one_to_many(another),
            MapperApiNote.SelectOneToMany.link_one_to_many(config, another),
            ThisObject.attribute(config),
            ThisObject.attribute(another, other_config=config),
            Page.param("onePage", config.module.entity.remark),
            Page.param("manyPage", another.module.entity.remark),
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
            JavaCode.DefaultAttribute.self_list_class(config),
            MapperApi.SelectOneToMany.query_one_to_many(config, another),
            MapperApiNote.SelectOneToMany.query_one_to_many(another),
            ThisObject.attribute(config),
            ThisObject.attribute(another, other_config=config),
            Page.param("onePage", config.module.entity.remark),
            Page.param("manyPage", another.module.entity.remark),
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
            MapperApi.SelectOneToMany.count_query_one_to_many(config, another),
            MapperApiNote.SelectOneToMany.count_query_one_to_many(another),
            ThisObject.attribute(config),
            ThisObject.attribute(another, other_config=config),
            Page.param("onePage", config.module.entity.remark),
            Page.param("manyPage", another.module.entity.remark),
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
        if len(config.baseInfo.manyToMany) == 0:
            return
        for many_to_many in config.baseInfo.manyToMany:
            code.add_function(SelectManyToMany.find_many_to_many(config, many_to_many.to, many_to_many.many))
            code.add_function(SelectManyToMany.query_many_to_many(config, many_to_many.to, many_to_many.many))

    @staticmethod
    def find_many_to_many(config: CodeConfig, to: CodeConfig, many: CodeConfig):
        # 内联多对多查询
        function = JavaCode.Function(
            "",
            JavaCode.DefaultAttribute.self_list_class(config),
            MapperApi.SelectManyToMany.find_many_to_many(config, to, many),
            MapperApiNote.SelectManyToMany.find_many_to_many(config, to, many),
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
            JavaCode.DefaultAttribute.self_list_class(config),
            MapperApi.SelectManyToMany.query_many_to_many(config, to, many),
            MapperApiNote.SelectManyToMany.query_many_to_many(config, to, many),
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
        if len(config.baseInfo.oneToOne) == 0:
            return
        for one_to_one in config.baseInfo.oneToOne:
            code.add_function(SelectForeignKey.select_in_and_where(config, one_to_one))

    @staticmethod
    def select_in_and_where(config: CodeConfig, another: CodeConfig):
        # 查找外键是属于这个表中的那个属性
        attr = None
        for i in config.baseInfo.attr:
            if i.field == another.baseInfo.foreignKey:
                attr = i
        if attr is None:
            return
        # 如果与自身重复，则不查询
        if config.module.entity.low_name() == another.module.entity.low_name():
            return

            # 内联多对多查询
        function = JavaCode.Function(
            "",
            JavaCode.DefaultAttribute.self_list_class(config),
            MapperApi.SelectForeignKey.select_in_and_where(config, attr),
            MapperApiNote.SelectForeignKey.select_in_and_where(config, attr),
            JavaCode.Attribute(f'@Param("list") List<{attr.type}>', "list", f'{config.module.entity.remark}的{attr.remark}列表'),
            ThisObject.attribute(config),
            FuzzySearch.attribute(config),
        )
        function.is_interface = True
        return function
