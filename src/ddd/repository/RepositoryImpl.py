from src.ddd.util import JavaCode
from src.ddd.util.JavaCode import Attribute
from src.structure.CodeConfig import CodeConfig


class FuzzySearch:
    """
    模糊搜索处理类
    """

    @staticmethod
    def param(config: CodeConfig):
        """
        获取模糊搜索的方法参数
        :param config: 配置
        :return: None|方法参数字符串
        """
        if config.createConfig.fuzzySearch.enable:
            if len(config.createConfig.fuzzySearch.value) != 0:
                return ", null"
        return ""


class SplicingSQL:
    """
    sql语句注入项
    """

    @staticmethod
    def param(config: CodeConfig):
        """
        SQL语句拼接项参数
        :param config:配置
        :return: None|方法参数
        """
        if config.createConfig.splicingSQL.enable:
            return f', null'
        return ""


class CreateFile:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig):
        code = JavaCode.JavaCode(
            config.module.repositoryImpl.path,
            config.module.repositoryImpl.className,
            f'{config.remark}仓库层实现'
        )
        code.add_implement(JavaCode.Attribute(config.module.repository.className, "", "实现的仓库层", config.module.repository.package))
        code.add_mate(f'@Repository')

        code.add_attr(
            JavaCode.Attribute(
                config.module.mapperInterface.className,
                config.module.mapperInterface.low_name(),
                f'{config.remark}mapper层',
                config.module.mapperInterface.package,
            ).add_mate("@Autowired")
        )
        code.add_attr(
            JavaCode.Attribute(
                config.module.cache.className,
                config.module.cache.low_name(),
                f'{config.remark}缓存',
                config.module.cache.package,
            ).add_mate("@Autowired")
        )

        code.add_import(config.package)
        code.add_function(CreateMethodDefaultAPI.insert(config))
        code.add_function(CreateMethodDefaultAPI.delete(config))
        code.add_function(CreateMethodDefaultAPI.update(config))
        code.add_function(CreateMethodDefaultAPI.get(config))
        code.add_function(CreateMethodDefaultAPI.lists(config))

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
            f'添加{config.remark}',
            JavaCode.Attribute(config.className, config.low_name(), f'{config.remark}对象'),
        )
        function.add_mate(f'@Override')

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'boolean b = false;')
                self.line(f'b = {config.module.mapperInterface.low_name()}.insert{config.className}({parameter[0].name}) > 0;')
                self.line(f'return b;')

        function.add_body(Body())
        return function

    @staticmethod
    def delete(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            JavaCode.Attribute("boolean", "b", "true:删除成功/false:删除失败"),
            f'{config.createConfig.methodName.get(1)}{config.className}',
            f'删除{config.remark},{config.key.attr}必传',
            JavaCode.Attribute(config.key.type, config.key.attr, f'{config.remark}的{config.key.attr}'),
        )
        function.add_mate(f'@Override')

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'boolean b = false;')
                self.line(f'b = {config.module.mapperInterface.low_name()}.delete{config.className}By{config.key.upper_name()}({parameter[0].name}) > 0;')
                self.line_if_one_block(f'b', f'{config.module.cache.low_name()}.removeValue({parameter[0].name});')
                self.line(f'return b;')

        function.add_body(Body())
        return function

    @staticmethod
    def update(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            JavaCode.Attribute("boolean", "b", "true:修改成功/false:修改失败"),
            f'{config.createConfig.methodName.get(2)}{config.className}',
            f'修改{config.remark}',
            JavaCode.Attribute(config.className, config.low_name(), f'{config.remark}对象'),
        )
        function.add_mate(f'@Override')

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'boolean b = false;')
                self.line(f'b = {config.module.mapperInterface.low_name()}.update{config.className}By{config.key.upper_name()}({config.low_name()}) > 0;')
                self.line_if_one_block(f'b', f'{config.module.cache.low_name()}.removeValue({parameter[0].name}.get{config.key.upper_name()}());')
                self.line(f'return b;')

        function.add_body(Body())
        return function

    @staticmethod
    def get(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            JavaCode.Attribute(config.className, config.className, f'获取到的{config.remark}对象'),
            f'{config.createConfig.methodName.get(3)}{config.className}',
            f'根据{config.key.attr}查询一个{config.remark}',
            JavaCode.Attribute(config.key.type, config.key.attr, f'{config.remark}的{config.key.attr}'),
        )
        function.add_mate(f'@Override')

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'{config.className} {config.low_name()} = {config.module.cache.low_name()}.loadAndGet({parameter[0].name});')
                self.line(f'return {config.low_name()};')

        function.add_body(Body())
        return function

    @staticmethod
    def lists(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            JavaCode.Attribute(f'List<{config.className}>', "list", f'{config.remark}列表'),
            f'{config.createConfig.methodName.get(4)}{config.className}',
            f'获取多个{config.remark}',
            JavaCode.Attribute(config.className, config.low_name(), f'{config.remark}对象'),
            JavaCode.Attribute("Page", "page", f'分页对象'),
        )
        function.add_mate(f'@Override')

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line_if(f'page != null')
                self.line(f'page.setMax({config.module.mapperInterface.low_name()}.count{config.className}({config.low_name()}{FuzzySearch.param(config)}));')
                self.block_end()
                self.line(f'return {config.module.mapperInterface.low_name()}.select{config.className}({config.low_name()}, page{FuzzySearch.param(config)}{SplicingSQL.param(config)});')

        function.add_body(Body())
        return function
