from src.ddd.util import JavaCode
from src.ddd.util.JavaCode import Attribute
from src.structure.CodeConfig import CodeConfig


class CreateFile:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig):
        code = JavaCode.JavaCode(
            config.module.domainImpl.path,
            config.module.domainImpl.className,
            f'{config.remark}领域层实现'
        )
        code.add_implement(JavaCode.Attribute(config.module.domain.className, "", "实现的业务层", config.module.domain.package))
        code.add_mate(f'@Service')

        code.add_attr(
            JavaCode.Attribute(
                config.module.repository.className,
                config.module.repository.low_name(),
                f'{config.remark}仓库层接口',
                config.module.repository.package,
            ).add_mate("@Autowired").add_mate(f'@Qualifier("{config.module.repositoryImpl.low_name()}")')
        )
        code.add_import(config.package)
        code.add_function(CreateMethodDefaultAPI.insert(config))
        code.add_function(CreateMethodDefaultAPI.delete(config))
        code.add_function(CreateMethodDefaultAPI.update(config))
        code.add_function(CreateMethodDefaultAPI.get(config))
        code.add_function(CreateMethodDefaultAPI.lists(config))
        # 额外的接口
        CreateMethodExtraAPI.create(config, code)

        return code.create()


class CreateMethodDefaultAPI:
    """
    创建默认方法
    """

    @staticmethod
    def insert(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            JavaCode.Attribute("boolean", "b", "true:添加成功/false:添加失败"),
            f'{config.createConfig.methodName.get(0)}{config.className}',
            f'前台添加{config.remark}',
            JavaCode.Attribute(config.className, config.low_name(), f'{config.remark}对象'),
        )
        function.add_mate(f'@Override')

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'boolean b = false;')
                self.line(f'b = {config.module.repository.low_name()}.{config.createConfig.methodName.get(0)}{config.className}({config.low_name()});')
                self.line(f'return b;')

        function.add_body(Body())
        return function

    @staticmethod
    def delete(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            JavaCode.Attribute("boolean", "b", "true:删除成功/false:删除失败"),
            f'{config.createConfig.methodName.get(1)}{config.className}',
            f'前台删除{config.remark},{config.key.attr}必传',
            JavaCode.Attribute(config.key.type, config.key.attr, f'{config.remark}的{config.key.attr}'),
        )
        function.add_mate(f'@Override')

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'boolean b = false;')
                self.line_if(f'{config.key.attr} != null')
                self.line(f'b = {config.module.repository.low_name()}.{config.createConfig.methodName.get(1)}{config.className}({config.key.attr});')
                self.block_end()
                self.line(f'return b;')

        function.add_body(Body())
        return function

    @staticmethod
    def update(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            JavaCode.Attribute("boolean", "b", "true:修改成功/false:修改失败"),
            f'{config.createConfig.methodName.get(2)}{config.className}',
            f'前台修改{config.remark}',
            JavaCode.Attribute(config.className, config.low_name(), f'{config.remark}对象'),
        )
        function.add_mate(f'@Override')

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'boolean b = false;')
                self.line_if(f'{config.low_name()}.get{config.key.upper_name()}() != null')
                self.line(f'b = {config.module.repository.low_name()}.{config.createConfig.methodName.get(2)}{config.className}({config.low_name()});')
                self.block_end()
                self.line(f'return b;')

        function.add_body(Body())
        return function

    @staticmethod
    def get(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            JavaCode.Attribute(config.className, config.className, f'获取到的{config.remark}对象'),
            f'{config.createConfig.methodName.get(3)}{config.className}',
            f'前台根据{config.key.attr}查询一个{config.remark}',
            JavaCode.Attribute(config.key.type, config.key.attr, f'{config.remark}的{config.key.attr}'),
        )
        function.add_mate(f'@Override')

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'boolean b = false;')
                self.line_if(f'{config.key.attr} != null')
                self.line(f'return {config.module.repository.low_name()}.{config.createConfig.methodName.get(3)}{config.className}({config.key.attr});')
                self.block_end()
                self.line(f'return null;')

        function.add_body(Body())
        return function

    @staticmethod
    def lists(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            JavaCode.Attribute(f'List<{config.className}>', "list", f'{config.remark}列表'),
            f'{config.createConfig.methodName.get(4)}{config.className}',
            f'前台获取多个{config.remark}',
            JavaCode.Attribute(config.className, config.low_name(), f'{config.remark}对象'),
            JavaCode.Attribute("Page", "page", f'分页对象'),
        )
        function.add_mate(f'@Override')

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'List<{config.className}> list = {config.module.repository.low_name()}.{config.createConfig.methodName.get(4)}{config.className}({config.low_name()}, page);')
                self.line(f'return list;')

        function.add_body(Body())
        return function


class CreateMethodExtraAPI:
    """
    创建默认方法
    """

    @staticmethod
    def create(config: CodeConfig, code: JavaCode.JavaCode):

        if config.createConfig.extraAPI.enable:
            value = config.createConfig.extraAPI.value
            if value is None:
                value = config.createConfig.extraAPI.default
            lists = value.split(",")
            for i in lists:
                code.add_function(CreateMethodExtraAPI.insert(config, i))
                code.add_function(CreateMethodExtraAPI.delete(config, i))
                code.add_function(CreateMethodExtraAPI.update(config, i))
                code.add_function(CreateMethodExtraAPI.get(config, i))
                code.add_function(CreateMethodExtraAPI.lists(config, i))

    @staticmethod
    def insert(config: CodeConfig, extra: str):
        function = JavaCode.Function(
            "public",
            JavaCode.Attribute("boolean", "b", "true:修改成功/false:修改失败"),
            f'{extra}{config.createConfig.methodName.get_upper(0)}{config.className}',
            f'{extra}添加{config.remark}',
            JavaCode.Attribute(config.className, config.low_name(), f'{config.remark}对象'),
        )
        function.add_mate(f'@Override')

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'boolean b = false;')
                self.line(f'b = {config.module.repository.low_name()}.{config.createConfig.methodName.get_upper(0)}{config.className}({config.low_name()});')
                self.line(f'return b;')

        function.add_body(Body())
        return function

    @staticmethod
    def delete(config: CodeConfig, extra: str):
        function = JavaCode.Function(
            "public",
            JavaCode.Attribute("boolean", "b", "true:删除成功/false:删除失败"),
            f'{extra}{config.createConfig.methodName.get_upper(1)}{config.className}',
            f'{extra}删除{config.remark},{config.key.attr}必传',
            JavaCode.Attribute(config.key.type, config.key.attr, f'{config.remark}的{config.key.attr}'),
        )
        function.add_mate(f'@Override')

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'boolean b = false;')
                self.line_if(f'{config.key.attr} != null')
                self.line(f'b = {config.module.repository.low_name()}.{config.createConfig.methodName.get_upper(1)}{config.className}({config.key.attr});')
                self.block_end()
                self.line(f'return b;')

        function.add_body(Body())
        return function

    @staticmethod
    def update(config: CodeConfig, extra: str):
        function = JavaCode.Function(
            "public",
            JavaCode.Attribute("boolean", "b", "true:修改成功/false:修改失败"),
            f'{extra}{config.createConfig.methodName.get_upper(2)}{config.className}',
            f'{extra}修改{config.remark}',
            JavaCode.Attribute(config.className, config.low_name(), f'{config.remark}对象'),
        )
        function.add_mate(f'@Override')

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'boolean b = false;')
                self.line_if(f'{config.low_name()}.get{config.key.upper_name()}() != null')
                self.line(f'b = {config.module.repository.low_name()}.{config.createConfig.methodName.get_upper(2)}{config.className}({config.low_name()});')
                self.block_end()
                self.line(f'return b;')

        function.add_body(Body())
        return function

    @staticmethod
    def get(config: CodeConfig, extra: str):
        function = JavaCode.Function(
            "public",
            JavaCode.Attribute(config.className, config.className, f'获取到的{config.remark}对象'),
            f'{extra}{config.createConfig.methodName.get_upper(3)}{config.className}',
            f'{extra}根据{config.key.attr}查询一个{config.remark}',
            JavaCode.Attribute(config.key.type, config.key.attr, f'{config.remark}的{config.key.attr}'),
        )
        function.add_mate(f'@Override')

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'boolean b = false;')
                self.line_if(f'{config.key.attr} != null')
                self.line(f'return {config.module.repository.low_name()}.{config.createConfig.methodName.get_upper(3)}{config.className}({config.key.attr});')
                self.block_end()
                self.line(f'return null;')

        function.add_body(Body())
        return function

    @staticmethod
    def lists(config: CodeConfig, extra: str):
        function = JavaCode.Function(
            "public",
            JavaCode.Attribute(f'List<{config.className}>', "list", f'{config.remark}列表'),
            f'{extra}{config.createConfig.methodName.get_upper(4)}{config.className}',
            f'{extra}获取多个{config.remark}',
            JavaCode.Attribute(config.className, config.low_name(), f'{config.remark}对象'),
            JavaCode.Attribute("Page", "page", f'分页对象'),
        )
        function.add_mate(f'@Override')

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'List<{config.className}> list = {config.module.repository.low_name()}.{config.createConfig.methodName.get_upper(4)}{config.className}({config.low_name()}, page);')
                self.line(f'return list;')

        function.add_body(Body())
        return function
