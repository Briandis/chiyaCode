from src.java import JavaCode
from src.java.CodeConfig import CodeConfig, Field


class ApiName:
    """
    接口名称
    """

    @staticmethod
    def _default_name(config: CodeConfig, index: int, extra=None):
        """
        获取默认名字
        :param config: 配置
        :param index:默认索引
        :return: 名字
        """
        if extra:
            return f'{extra}{config.createConfig.methodName.get_upper(index)}{config.module.entity.className}'
        return f'{config.createConfig.methodName.get(index)}{config.module.entity.className}'

    @staticmethod
    def insert(config: CodeConfig, extra=None):
        return ApiName._default_name(config, 0, extra)

    @staticmethod
    def delete(config: CodeConfig, extra=None):
        return ApiName._default_name(config, 1, extra)

    @staticmethod
    def update(config: CodeConfig, extra=None):
        return ApiName._default_name(config, 2, extra)

    @staticmethod
    def get(config: CodeConfig, extra=None):
        return ApiName._default_name(config, 3, extra)

    @staticmethod
    def list(config: CodeConfig, extra=None):
        return ApiName._default_name(config, 4, extra)


class AnnotationInfo:
    """
    方法注释信息
    """

    @staticmethod
    def _base(config: CodeConfig, todo, extra=None):
        if extra:
            return f'{extra}{todo}{config.module.entity.remark}'
        return f'{todo}{config.module.entity.remark}'

    @staticmethod
    def insert(config: CodeConfig, extra=None):
        return AnnotationInfo._base(config, "添加", extra)

    @staticmethod
    def delete(config: CodeConfig, extra=None):
        return AnnotationInfo._base(config, f'根据{config.baseInfo.key.attr}删除', extra)

    @staticmethod
    def delete_not_key(config: CodeConfig, extra=None):
        return AnnotationInfo._base(config, f'删除', extra)

    @staticmethod
    def update(config: CodeConfig, extra=None):
        return AnnotationInfo._base(config, "修改", extra)

    @staticmethod
    def get(config: CodeConfig, extra=None):
        return AnnotationInfo._base(config, f'根据{config.baseInfo.key.attr}查询一个', extra)

    @staticmethod
    def list(config: CodeConfig, extra=None):
        return AnnotationInfo._base(config, "获取多个", extra)


class Template:

    @staticmethod
    def impl(config: CodeConfig, code: JavaCode.JavaCode, service_name, extra=None):
        pass

    @staticmethod
    def extra_impl(config: CodeConfig, code: JavaCode.JavaCode, service_name):
        pass


class BaseApi:
    """
    创建默认方法
    """

    @staticmethod
    def insert(config: CodeConfig, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.ReturnBoolean,
            ApiName.insert(config, extra),
            AnnotationInfo.insert(config, extra),
            JavaCode.DefaultAttribute.self_class(config),
        )
        function.set_is_interface()
        return function

    @staticmethod
    def delete(config: CodeConfig, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.ReturnBoolean,
            ApiName.delete(config, extra),
            AnnotationInfo.delete(config, extra),
            JavaCode.DefaultAttribute.self_key(config),
        )
        function.set_is_interface()
        return function

    @staticmethod
    def delete_not_key(config: CodeConfig, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.ReturnBoolean,
            ApiName.delete(config, extra),
            AnnotationInfo.delete_not_key(config, extra),
            JavaCode.DefaultAttribute.self_class(config)
        )
        function.set_is_interface()
        return function

    @staticmethod
    def update(config: CodeConfig, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.ReturnBoolean,
            ApiName.update(config, extra),
            AnnotationInfo.update(config, extra),
            JavaCode.DefaultAttribute.self_class(config),
        )
        function.set_is_interface()
        return function

    @staticmethod
    def get(config: CodeConfig, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.self_class(config),
            ApiName.get(config, extra),
            AnnotationInfo.get(config, extra),
            JavaCode.DefaultAttribute.self_key(config),
        )
        function.set_is_interface()
        return function

    @staticmethod
    def lists(config: CodeConfig, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.self_list_class(config),
            ApiName.list(config, extra),
            AnnotationInfo.list(config, extra),
            JavaCode.DefaultAttribute.self_class(config),
            JavaCode.DefaultAttribute.Page,
        )
        function.set_is_interface()
        return function

    @staticmethod
    def api(config: CodeConfig, code: JavaCode.JavaCode, extra=None):
        code.add_import(config.module.entity.get_package())
        code.add_function(BaseApi.insert(config, extra))
        if config.baseInfo.key:
            code.add_function(BaseApi.delete(config, extra))
            code.add_function(BaseApi.update(config, extra))
            code.add_function(BaseApi.get(config, extra))
        else:
            code.add_function(BaseApi.delete_not_key(config, extra))
        code.add_function(BaseApi.lists(config, extra))

    @staticmethod
    def extra_api(config: CodeConfig, code: JavaCode.JavaCode):
        if config.createConfig.extraAPI.enable:
            value = config.createConfig.extraAPI.value
            if value is None:
                value = config.createConfig.extraAPI.default
            lists = value.split(",")
            for extra in lists:
                BaseApi.api(config, code, extra)


class BaseAPIImpl(Template):
    """
    默认方法的实现
    """

    @staticmethod
    def insert(config: CodeConfig, service_name, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.ReturnBoolean,
            ApiName.insert(config, extra),
            AnnotationInfo.insert(config, extra),
            JavaCode.DefaultAttribute.self_class(config)
        )
        function.add_mate(JavaCode.DefaultMate.Override())

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line(f'boolean b = false;')
                self.line(f'b = {service_name}.{ApiName.insert(config)}({parameter[0].name});')
                self.line(f'return b;')

        function.add_body(Body())
        return function

    @staticmethod
    def delete(config: CodeConfig, service_name, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.ReturnBoolean,
            ApiName.delete(config, extra),
            AnnotationInfo.delete(config, extra),
            JavaCode.DefaultAttribute.self_key(config),
        )
        function.add_mate(JavaCode.DefaultMate.Override())

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line(f'boolean b = false;')
                self.line_if(f'{config.baseInfo.key.attr} != null')
                self.line(f'b = {service_name}.{ApiName.delete(config)}({config.baseInfo.key.attr});')
                self.block_end()
                self.line(f'return b;')

        function.add_body(Body())
        return function

    @staticmethod
    def delete_not_key(config: CodeConfig, service_name, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.ReturnBoolean,
            ApiName.delete(config, extra),
            AnnotationInfo.delete_not_key(config, extra),
            JavaCode.DefaultAttribute.self_class(config)
        )
        function.add_mate(JavaCode.DefaultMate.Override())

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line(f'boolean b = false;')
                self.line(f'b = {service_name}.{ApiName.delete(config)}({parameter[0].name});')
                self.line(f'return b;')

        function.add_body(Body())
        return function

    @staticmethod
    def update(config: CodeConfig, service_name, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.ReturnBoolean,
            ApiName.update(config, extra),
            AnnotationInfo.update(config, extra),
            JavaCode.DefaultAttribute.self_class(config)
        )
        function.add_mate(JavaCode.DefaultMate.Override())

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line(f'boolean b = false;')
                self.line_if(f'{parameter[0].name}.get{config.baseInfo.key.upper_name()}() != null')
                self.line(f'b = {service_name}.{ApiName.update(config)}({parameter[0].name});')
                self.block_end()
                self.line(f'return b;')

        function.add_body(Body())
        return function

    @staticmethod
    def get(config: CodeConfig, service_name, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.self_class(config),
            ApiName.get(config, extra),
            AnnotationInfo.get(config, extra),
            JavaCode.DefaultAttribute.self_key(config),
        )
        function.add_mate(JavaCode.DefaultMate.Override())

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line_if(f'{parameter[0].name} != null')
                self.line(f'return {service_name}.{ApiName.get(config)}({parameter[0].name});')
                self.block_end()
                self.line(f'return null;')

        function.add_body(Body())
        return function

    @staticmethod
    def lists(config: CodeConfig, service_name, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.self_list_class(config),
            ApiName.list(config, extra),
            AnnotationInfo.list(config, extra),
            JavaCode.DefaultAttribute.self_class(config),
            JavaCode.DefaultAttribute.Page
        )
        function.add_mate(JavaCode.DefaultMate.Override())

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line(f'List<{config.module.entity.className}> list = {service_name}.{ApiName.list(config)}({parameter[0].name}, {parameter[1].name});')
                self.line(f'return list;')

        function.add_body(Body())
        return function

    @staticmethod
    def impl(config: CodeConfig, code: JavaCode.JavaCode, service_name, extra=None):
        code.add_import(config.module.entity.get_package())
        code.add_function(BaseAPIImpl.insert(config, service_name, extra))
        if config.baseInfo.key:
            code.add_function(BaseAPIImpl.delete(config, service_name, extra))
            code.add_function(BaseAPIImpl.update(config, service_name, extra))
            code.add_function(BaseAPIImpl.get(config, service_name, extra))
        else:
            code.add_function(BaseAPIImpl.delete_not_key(config, service_name, extra))
        code.add_function(BaseAPIImpl.lists(config, service_name, extra))

    @staticmethod
    def extra_impl(config: CodeConfig, code: JavaCode.JavaCode, service_name):
        if config.createConfig.extraAPI.enable:
            value = config.createConfig.extraAPI.value
            if value is None:
                value = config.createConfig.extraAPI.default
            lists = value.split(",")
            for extra in lists:
                BaseAPIImpl.impl(config, code, service_name, extra)


class ModuleConfig:
    """
    根据配置进行处理
    """

    class ChiyaSecurity:
        @staticmethod
        def add_import(config: CodeConfig, code: JavaCode.JavaCode):
            """
            添加导入配置
            :param config: 配置信息
            :param code: 源码实例
            """
            if config.createConfig.chiyaSecurity.enable:
                code.add_import("chiya.web.security.entity.ChiyaRole")

        @staticmethod
        def add_default_mate(config: CodeConfig, function: JavaCode.Function):
            """
            添加默认接口的权限
            :param config: 配置信息
            :param function: 方法实例
            """
            if config.createConfig.chiyaSecurity.enable:
                function.add_mate(JavaCode.DefaultMate.ChiyaSecurity("ChiyaRole.USER"))

        @staticmethod
        def add_extra_mate(config: CodeConfig, function: JavaCode.Function):
            """
            添加扩展接口的权限
            :param config: 配置信息
            :param function: 方法实例
            """
            if config.createConfig.chiyaSecurity.enable:
                function.add_mate(JavaCode.DefaultMate.ChiyaSecurity("ChiyaRole.ADMIN"))


class WebApi:
    """
    HTTP入口的方法
    """

    @staticmethod
    def insert(config: CodeConfig, service_name, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.Result,
            ApiName.insert(config, extra),
            AnnotationInfo.insert(config, extra),
            JavaCode.DefaultAttribute.self_class(config)
        )
        if config.createConfig.restful.enable:
            function.add_mate(JavaCode.DefaultMate.PostMapping(extra, config.module.entity.low_name()))
        else:
            function.add_mate(JavaCode.DefaultMate.RequestMapping(extra, ApiName.insert(config)))
            function.add_mate(JavaCode.DefaultMate.ResponseBody())
        # 用户权限
        ModuleConfig.ChiyaSecurity.add_default_mate(config, function)

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line(f'boolean b = false;')
                self.line(f'b = {service_name}.{ApiName.insert(config, extra)}({parameter[0].name});')
                self.line(f'return Result.judge(b);')

        function.add_body(Body())

        return function

    @staticmethod
    def delete(config: CodeConfig, service_name, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.Result,
            ApiName.delete(config, extra),
            AnnotationInfo.delete(config, extra),
            JavaCode.DefaultAttribute.self_key(config),
        )
        if config.createConfig.restful.enable:
            function.add_mate(JavaCode.DefaultMate.DeleteMapping(extra, config.module.entity.low_name()))
        else:
            function.add_mate(JavaCode.DefaultMate.RequestMapping(extra, ApiName.delete(config)))
            function.add_mate(JavaCode.DefaultMate.ResponseBody())
        # 用户权限
        ModuleConfig.ChiyaSecurity.add_default_mate(config, function)

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line(f'boolean b = false;')
                self.line_if(f'{parameter[0].name} != null')
                self.line(f'b = {service_name}.{ApiName.delete(config, extra)}({parameter[0].name});')
                self.block_end()
                self.line(f'return Result.judge(b);')

        function.add_body(Body())
        return function

    @staticmethod
    def update(config: CodeConfig, service_name, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.Result,
            ApiName.update(config, extra),
            AnnotationInfo.update(config, extra),
            JavaCode.DefaultAttribute.self_class(config),
        )
        if config.createConfig.restful.enable:
            function.add_mate(JavaCode.DefaultMate.PutMapping(extra, config.module.entity.low_name()))
        else:
            function.add_mate(JavaCode.DefaultMate.RequestMapping(extra, ApiName.update(config)))
            function.add_mate(JavaCode.DefaultMate.ResponseBody())
        # 用户权限
        ModuleConfig.ChiyaSecurity.add_default_mate(config, function)

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line(f'boolean b = false;')
                self.line_if(f'{parameter[0].name}.get{config.baseInfo.key.upper_name()}() != null')
                self.line(f'b = {service_name}.{ApiName.update(config, extra)}({parameter[0].name});')
                self.block_end()
                self.line(f'return Result.judge(b);')

        function.add_body(Body())
        return function

    @staticmethod
    def get(config: CodeConfig, service_name, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.Result,
            ApiName.get(config, extra),
            AnnotationInfo.get(config, extra),
            JavaCode.DefaultAttribute.self_key(config),
        )
        if config.createConfig.restful.enable:
            function.add_mate(JavaCode.DefaultMate.GetMapping(extra, config.module.entity.low_name()))
        else:
            function.add_mate(JavaCode.DefaultMate.RequestMapping(extra, ApiName.get(config)))
            function.add_mate(JavaCode.DefaultMate.ResponseBody())
        # 用户权限
        ModuleConfig.ChiyaSecurity.add_default_mate(config, function)

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line(f'boolean b = false;')
                self.line_if(f'{parameter[0].name} != null')
                self.line(f'return Result.success({service_name}.{ApiName.get(config, extra)}({parameter[0].name}));')
                self.block_end()
                self.line(f'return Result.judge(b);')

        function.add_body(Body())
        return function

    @staticmethod
    def lists(config: CodeConfig, service_name, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.Result,
            ApiName.list(config, extra),
            AnnotationInfo.list(config, extra),
            JavaCode.DefaultAttribute.self_class(config),
            JavaCode.DefaultAttribute.Page,
        )
        if config.createConfig.restful.enable:
            function.add_mate(JavaCode.DefaultMate.GetMapping(extra, ApiName.list(config)))
        else:
            function.add_mate(JavaCode.DefaultMate.RequestMapping(extra, ApiName.get(config)))
            function.add_mate(JavaCode.DefaultMate.ResponseBody())
        # 用户权限
        ModuleConfig.ChiyaSecurity.add_default_mate(config, function)

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line(f'List<{config.module.entity.className}> list = {service_name}.{ApiName.list(config, extra)}({parameter[0].name}, {parameter[1].name});')
                self.line(f'return Result.success(list, {parameter[1].name});')

        function.add_body(Body())
        return function

    @staticmethod
    def api(config: CodeConfig, code: JavaCode.JavaCode, service_name, extra=None):
        code.add_import("java.util.List")
        code.add_import(config.module.entity.get_package())
        code.add_function(WebApi.insert(config, service_name, extra))
        ModuleConfig.ChiyaSecurity.add_import(config, code)
        if config.baseInfo.key:
            code.add_function(WebApi.delete(config, service_name, extra))
            code.add_function(WebApi.update(config, service_name, extra))
            code.add_function(WebApi.get(config, service_name, extra))
        code.add_function(WebApi.lists(config, service_name, extra))

    @staticmethod
    def extra_api(config: CodeConfig, code: JavaCode.JavaCode, service_name):
        if config.createConfig.extraAPI.enable:
            value = config.createConfig.extraAPI.value
            if value is None:
                value = config.createConfig.extraAPI.default
            lists = value.split(",")
            for extra in lists:
                WebApi.api(config, code, service_name, extra)


class MapperApi:
    """
    Mapper层的方法名称
    """

    class Insert:
        @staticmethod
        def insert(config: CodeConfig) -> str:
            return f'insert{config.module.entity.className}'

        @staticmethod
        def insert_list(config: CodeConfig) -> str:
            return f'insert{config.module.entity.className}List'

        @staticmethod
        def insert_or_update_by_unique(config: CodeConfig) -> str:
            return f'insertOrUpdate{config.module.entity.className}ByUnique'

        @staticmethod
        def insert_or_update_by_where(config: CodeConfig) -> str:
            return f'insertOrUpdate{config.module.entity.className}ByWhere'

        @staticmethod
        def insert_by_exist_where(config: CodeConfig) -> str:
            return f'insert{config.module.entity.className}ByExistWhere'

        @staticmethod
        def insert_by_not_exist_where(config: CodeConfig) -> str:
            return f'insert{config.module.entity.className}ByNotExistWhere'

    class Delete:
        @staticmethod
        def delete_by_id(config: CodeConfig) -> str:
            return f'delete{config.module.entity.className}By{config.baseInfo.key.upper_name()}'

        @staticmethod
        def delete_in_id(config: CodeConfig) -> str:
            return f'delete{config.module.entity.className}In{config.baseInfo.key.upper_name()}'

        @staticmethod
        def delete_by_id_and_where(config: CodeConfig) -> str:
            return f'delete{config.module.entity.className}By{config.baseInfo.key.upper_name()}AndWhere'

        @staticmethod
        def delete(config: CodeConfig) -> str:
            return f'delete{config.module.entity.className}'

        @staticmethod
        def false_delete(config: CodeConfig) -> str:
            return f'falseDelete{config.module.entity.className}By{config.baseInfo.key.upper_name()}'

    class Update:
        @staticmethod
        def update_by_id(config: CodeConfig) -> str:
            return f'update{config.module.entity.className}By{config.baseInfo.key.upper_name()}'

        @staticmethod
        def update_by_id_and_where(config: CodeConfig) -> str:
            return f'update{config.module.entity.className}By{config.baseInfo.key.upper_name()}AndWhere'

        @staticmethod
        def update_by_not_repeat_where(config: CodeConfig) -> str:
            return f'update{config.module.entity.className}ByNotRepeatWhere'

        @staticmethod
        def update(config: CodeConfig) -> str:
            return f'update{config.module.entity.className}'

        @staticmethod
        def update_set_null_by_id(config: CodeConfig) -> str:
            return f'update{config.module.entity.className}SetNullBy{config.baseInfo.key.upper_name()}'

    class Select:
        @staticmethod
        def select_by_id(config: CodeConfig) -> str:
            return f'select{config.module.entity.className}By{config.baseInfo.key.upper_name()}'

        @staticmethod
        def select_in_id(config: CodeConfig) -> str:
            return f'select{config.module.entity.className}In{config.baseInfo.key.upper_name()}'

        @staticmethod
        def select_in_id_and_where(config: CodeConfig) -> str:
            return f'select{config.module.entity.className}In{config.baseInfo.key.upper_name()}AndWhere'

        @staticmethod
        def select_one(config: CodeConfig) -> str:
            return f'selectOne{config.module.entity.className}'

        @staticmethod
        def select(config: CodeConfig) -> str:
            return f'select{config.module.entity.className}'

        @staticmethod
        def count(config: CodeConfig) -> str:
            return f'count{config.module.entity.className}'

    class SelectOneToOne:
        @staticmethod
        def find_one_to_one(config: CodeConfig, another: CodeConfig) -> str:
            return f'find{config.module.entity.className}OneToOne{another.module.entity.className}'

        @staticmethod
        def count_find_one_to_one(config: CodeConfig, another: CodeConfig) -> str:
            return f'countFind{config.module.entity.className}OneToOne{another.module.entity.className}'

        @staticmethod
        def link_one_to_one(another: CodeConfig) -> str:
            return f'linkOneToOne{another.module.entity.className}'

        @staticmethod
        def query_one_to_one(config: CodeConfig, another: CodeConfig) -> str:
            return f'query{config.module.entity.className}OneToOne{another.module.entity.className}'

        @staticmethod
        def count_query_one_to_one(config: CodeConfig, another: CodeConfig) -> str:
            return f'countQuery{config.module.entity.className}OneToOne{another.module.entity.className}'

    class SelectOneToMany:
        @staticmethod
        def find_one_to_many(config: CodeConfig, another: CodeConfig) -> str:
            return f'find{config.module.entity.className}OneToMany{another.module.entity.className}'

        @staticmethod
        def count_find_one_to_many(config: CodeConfig, another: CodeConfig) -> str:
            return f'countFind{config.module.entity.className}OneToMany{another.module.entity.className}'

        @staticmethod
        def link_one_to_many(another: CodeConfig) -> str:
            return f'linkOneToMany{another.module.entity.className}'

        @staticmethod
        def query_one_to_many(config: CodeConfig, another: CodeConfig) -> str:
            return f'query{config.module.entity.className}OneToMany{another.module.entity.className}'

        @staticmethod
        def count_query_one_to_many(config: CodeConfig, another: CodeConfig) -> str:
            return f'countQuery{config.module.entity.className}OneToMany{another.module.entity.className}'

    class SelectManyToMany:
        @staticmethod
        def find_many_to_many(config: CodeConfig, to: CodeConfig, many: CodeConfig) -> str:
            return f'find{config.module.entity.className}ManyToManyLink{to.module.entity.className}On{many.module.entity.className}'

        @staticmethod
        def query_many_to_many(config: CodeConfig, to: CodeConfig, many: CodeConfig) -> str:
            return f'query{config.module.entity.className}ManyToManyLink{to.module.entity.className}On{many.module.entity.className}'

    class SelectForeignKey:
        @staticmethod
        def select_in_and_where(config: CodeConfig, attr: Field) -> str:
            return f'select{config.module.entity.className}In{attr.upper_name()}AndWhere'


class RepositoryConfig:

    @staticmethod
    def FuzzySearch(config: CodeConfig):
        """
        获取模糊搜索的方法参数
        :param config: 配置
        :return: None|方法参数字符串
        """
        if config.createConfig.fuzzySearch.enable:
            if config.createConfig.fuzzySearch.value and len(config.createConfig.fuzzySearch.value) != 0:
                return ", null"
        return ""

    @staticmethod
    def SplicingSQL(config: CodeConfig):
        """
        SQL语句拼接项参数
        :param config:配置
        :return: None|方法参数
        """
        if config.createConfig.splicingSQL.enable:
            return f', null'
        return ""


class BaseRepository(Template):
    """
    创建默认方法
    """

    @staticmethod
    def insert(config: CodeConfig, service_name, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.ReturnBoolean,
            ApiName.insert(config, extra),
            AnnotationInfo.insert(config, extra),
            JavaCode.DefaultAttribute.self_class(config),
        )
        function.add_mate(JavaCode.DefaultMate.Override())

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line(f'boolean b = false;')
                self.line(f'b = {service_name}.{MapperApi.Insert.insert(config)}({parameter[0].name}) > 0;')
                self.line(f'return b;')

        function.add_body(Body())
        return function

    @staticmethod
    def delete(config: CodeConfig, service_name, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.ReturnBoolean,
            ApiName.delete(config, extra),
            AnnotationInfo.delete(config, extra),
            JavaCode.DefaultAttribute.self_key(config),
        )
        function.add_mate(JavaCode.DefaultMate.Override())

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line(f'boolean b = false;')
                self.line(f'b = {service_name}.{MapperApi.Delete.delete_by_id(config)}({parameter[0].name}) > 0;')
                if config.createConfig.repositoryUseCache.enable:
                    self.line_if_one_block(f'b', f'{config.module.cache.low_name()}.removeValue({parameter[0].name});')
                self.line(f'return b;')

        function.add_body(Body())
        return function

    @staticmethod
    def delete_not_key(config: CodeConfig, service_name, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.ReturnBoolean,
            ApiName.delete(config, extra),
            AnnotationInfo.delete_not_key(config, extra),
            JavaCode.DefaultAttribute.self_class(config)
        )
        function.add_mate(JavaCode.DefaultMate.Override())

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line(f'boolean b = false;')
                self.line(f'b = {service_name}.{MapperApi.Delete.delete(config)}({parameter[0].name}{RepositoryConfig.FuzzySearch(config)}) > 0;')
                self.line(f'return b;')

        function.add_body(Body())
        return function

    @staticmethod
    def update(config: CodeConfig, service_name, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.ReturnBoolean,
            ApiName.update(config, extra),
            AnnotationInfo.update(config, extra),
            JavaCode.DefaultAttribute.self_class(config),
        )
        function.add_mate(JavaCode.DefaultMate.Override())

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line(f'boolean b = false;')
                self.line(f'b = {service_name}.{MapperApi.Update.update_by_id(config)}({parameter[0].name}) > 0;')
                if config.createConfig.repositoryUseCache.enable:
                    self.line_if_one_block(f'b', f'{config.module.cache.low_name()}.removeValue({parameter[0].name}.get{config.baseInfo.key.upper_name()}());')
                self.line(f'return b;')

        function.add_body(Body())
        return function

    @staticmethod
    def get(config: CodeConfig, service_name, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.self_class(config),
            ApiName.get(config, extra),
            AnnotationInfo.get(config, extra),
            JavaCode.DefaultAttribute.self_key(config)
        )
        function.add_mate(JavaCode.DefaultMate.Override())

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                if config.createConfig.repositoryUseCache.enable:
                    self.line(f'{config.module.entity.className} {config.module.entity.low_name()} = {config.module.cache.low_name()}.loadAndGet({parameter[0].name});')
                else:
                    self.line(f'{config.module.entity.className} {config.module.entity.low_name()} = {service_name}.{MapperApi.Select.select_by_id(config)}({parameter[0].name});')
                self.line(f'return {config.module.entity.low_name()};')

        function.add_body(Body())
        return function

    @staticmethod
    def get_one(config: CodeConfig, service_name, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.self_class(config),
            f'{config.createConfig.methodName.get(3)}One{config.module.entity.className}',
            f'查询一个{config.module.entity.remark}',
            JavaCode.DefaultAttribute.self_class(config)
        )
        function.add_mate(JavaCode.DefaultMate.Override())

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line(f'return  {service_name}.{MapperApi.Select.select_one(config)}({parameter[0].name}, 0{RepositoryConfig.FuzzySearch(config)});')

        function.add_body(Body())
        return function

    @staticmethod
    def lists(config: CodeConfig, service_name, extra=None):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.self_list_class(config),
            ApiName.list(config, extra),
            AnnotationInfo.list(config, extra),
            JavaCode.DefaultAttribute.self_class(config),
            JavaCode.DefaultAttribute.Page,
        )
        function.add_mate(JavaCode.DefaultMate.Override())

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line_if(f'page != null')
                self.line(f'page.setMax({service_name}.{MapperApi.Select.count(config)}({parameter[0].name}{RepositoryConfig.FuzzySearch(config)}));')
                self.block_end()
                self.line(
                    f'return {service_name}.{MapperApi.Select.select(config)}({parameter[0].name}, {parameter[1].name}{RepositoryConfig.FuzzySearch(config)}{RepositoryConfig.SplicingSQL(config)});'
                )

        function.add_body(Body())
        return function

    @staticmethod
    def impl(config: CodeConfig, code: JavaCode.JavaCode, service_name, extra=None):
        code.add_import(config.module.entity.get_package())
        code.add_function(BaseRepository.insert(config, service_name, extra))
        if config.baseInfo.key:
            code.add_function(BaseRepository.delete(config, service_name, extra))
            code.add_function(BaseRepository.update(config, service_name, extra))
            code.add_function(BaseRepository.get(config, service_name, extra))
        else:
            code.add_function(BaseRepository.delete_not_key(config, service_name, extra))
        code.add_function(BaseRepository.lists(config, service_name, extra))

    @staticmethod
    def extra_impl(config: CodeConfig, code: JavaCode.JavaCode, service_name):
        if config.createConfig.extraAPI.enable:
            value = config.createConfig.extraAPI.value
            if value is None:
                value = config.createConfig.extraAPI.default
            lists = value.split(",")
            for extra in lists:
                BaseRepository.impl(config, code, service_name, extra)


class MapperApiNote:
    """
    Mapper层的方法注释
    """

    class Insert:
        @staticmethod
        def insert(config: CodeConfig) -> str:
            return f'添加{config.module.entity.remark}'

        @staticmethod
        def insert_list(config: CodeConfig) -> str:
            return f'添加多个{config.module.entity.remark}'

        @staticmethod
        def insert_or_update_by_unique(config: CodeConfig) -> str:
            return f'添加或更新{config.module.entity.remark}，根据唯一性索引'

        @staticmethod
        def insert_or_update_by_where(config: CodeConfig) -> str:
            return f'添加或更新{config.module.entity.remark}，根据查询条件'

        @staticmethod
        def insert_by_exist_where(config: CodeConfig) -> str:
            return f'条件添加{config.module.entity.remark}，查询条件存在的情况下'

        @staticmethod
        def insert_by_not_exist_where(config: CodeConfig) -> str:
            return f'条件添加{config.module.entity.remark}，查询条件不存在的情况下'

    class Delete:
        @staticmethod
        def delete_by_id(config: CodeConfig) -> str:
            return f'根据{config.baseInfo.key.attr}真删{config.module.entity.remark}'

        @staticmethod
        def delete_in_id(config: CodeConfig) -> str:
            return f'根据{config.baseInfo.key.attr}列表真删{config.module.entity.remark}'

        @staticmethod
        def delete_by_id_and_where(config: CodeConfig) -> str:
            return f'根据{config.baseInfo.key.attr}和其他条件真删{config.module.entity.remark}'

        @staticmethod
        def delete(config: CodeConfig) -> str:
            return f'根据条件真删{config.module.entity.remark}'

        @staticmethod
        def false_delete(config: CodeConfig) -> str:
            return f'根据{config.baseInfo.key.attr}假删{config.module.entity.remark}'

    class Update:
        @staticmethod
        def update_by_id(config: CodeConfig) -> str:
            return f'根据{config.baseInfo.key.attr}修改{config.module.entity.remark}'

        @staticmethod
        def update_by_id_and_where(config: CodeConfig) -> str:
            return f'根据{config.baseInfo.key.attr}和其他的条件更新{config.module.entity.remark}'

        @staticmethod
        def update_by_not_repeat_where(config: CodeConfig) -> str:
            return f'根据查询条件不满足的情况下更新{config.module.entity.remark}。说明：查询的记录不存在则更新'

        @staticmethod
        def update(config: CodeConfig) -> str:
            return f'根据条件更新{config.module.entity.remark}'

        @staticmethod
        def update_set_null_by_id(config: CodeConfig) -> str:
            return f'记录{config.baseInfo.key.attr}设置其他字段为null，对象中字段不为Null则是要设置成null的字段'

    class Select:
        @staticmethod
        def select_by_id(config: CodeConfig) -> str:
            return f'根据{config.baseInfo.key.attr}查询{config.module.entity.remark}'

        @staticmethod
        def select_in_id(config: CodeConfig) -> str:
            return f'根据{config.baseInfo.key.attr}列表查询{config.module.entity.remark}'

        @staticmethod
        def select_in_id_and_where(config: CodeConfig) -> str:
            return f'根据{config.baseInfo.key.attr}列表和其他条件查询{config.module.entity.remark}'

        @staticmethod
        def select_one(config: CodeConfig) -> str:
            return f'只查询一个{config.module.entity.remark}'

        @staticmethod
        def select(config: CodeConfig) -> str:
            return f'查询多个{config.module.entity.remark}'

        @staticmethod
        def count(config: CodeConfig) -> str:
            return f'统计{config.module.entity.remark}记录数'

    class SelectOneToOne:
        @staticmethod
        def find_one_to_one(another: CodeConfig) -> str:
            return f'内联一对一查询{another.module.entity.remark}'

        @staticmethod
        def count_find_one_to_one(config: CodeConfig) -> str:
            return f'内联一对一统计{config.module.entity.remark}'

        @staticmethod
        def link_one_to_one(config: CodeConfig, another: CodeConfig) -> str:
            return f'内联一对一查询{config.module.entity.remark}，只返回{another.module.entity.remark}'

        @staticmethod
        def query_one_to_one(another: CodeConfig) -> str:
            return f'外联一对一查询{another.module.entity.remark}'

        @staticmethod
        def count_query_one_to_one(another: CodeConfig) -> str:
            return f'外联一对一统计{another.module.entity.remark}'

    class SelectOneToMany:
        @staticmethod
        def find_one_to_many(another: CodeConfig) -> str:
            return f'内联一对多查询{another.module.entity.remark}，双方均可分页'

        @staticmethod
        def count_find_one_to_many(config: CodeConfig) -> str:
            return f'内联一对多统计{config.module.entity.remark}，双方均可分页'

        @staticmethod
        def link_one_to_many(config: CodeConfig, another: CodeConfig) -> str:
            return f'内联一对多查询{config.module.entity.remark}，只返回{another.module.entity.remark}'

        @staticmethod
        def query_one_to_many(another: CodeConfig) -> str:
            return f'外联一对多查询{another.module.entity.remark}'

        @staticmethod
        def count_query_one_to_many(another: CodeConfig) -> str:
            return f'外联一对多统计{another.module.entity.remark}，双方均可分页'

    class SelectManyToMany:
        @staticmethod
        def find_many_to_many(config: CodeConfig, to: CodeConfig, many: CodeConfig) -> str:
            return f'内联多对多查询{config.module.entity.remark},根据{to.module.entity.remark}联查{many.module.entity.remark}'

        @staticmethod
        def query_many_to_many(config: CodeConfig, to: CodeConfig, many: CodeConfig) -> str:
            return f'外联多对多查询{config.module.entity.remark},根据{to.module.entity.remark}联查{many.module.entity.remark}'

    class SelectForeignKey:
        @staticmethod
        def select_in_and_where(config: CodeConfig, attr: Field) -> str:
            return f'根据{attr.remark}列表和其他条件查询{config.module.entity.remark}'
