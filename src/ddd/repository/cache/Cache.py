from src.ddd.util import JavaCode
from src.structure.CodeConfig import CodeConfig


class CreateFile:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig):
        code = JavaCode.JavaCode(
            config.module.cache.path,
            config.module.cache.className,
            f'{config.remark}缓存层'
        )
        code.add_mate("@Service")

        code.add_attr(
            JavaCode.Attribute(
                config.module.mapperInterface.className,
                config.module.mapperInterface.low_name(),
                f'{config.remark}Mapper接口',
                config.module.mapperInterface.package,
            ).add_mate("@Autowired")
        )
        code.add_import(config.package)
        code.add_attr(
            JavaCode.Attribute(
                "BaseRedisService",
                "baseRedisService",
                f'Redis操作库',
                "chiya.web.redis.BaseRedisService",
            ).add_mate("@Autowired")
        )
        if config.key:
            code.add_function(FunctionCreate.get_key(config))
            code.add_function(FunctionCreate.set_value(config))
            code.add_function(FunctionCreate.get_value(config))
            code.add_function(FunctionCreate.load_and_get(config))
            code.add_function(FunctionCreate.remove(config))

        return code.create()


class FunctionCreate:
    """
    获取唯一性key
    """

    @staticmethod
    def get_key(config: CodeConfig):
        function = JavaCode.Function(
            "private",
            JavaCode.Attribute("String", "String", f"{config.remark}的唯一缓存key"),
            f'getKey',
            f'根据{config.remark}的{config.key.attr}创建唯一key',
            JavaCode.Attribute(config.key.type, config.key.attr, f'{config.remark}的{config.key.attr}'),
        )

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line(f'return "{config.tableName.replace("_", ":")}:" + {parameter[0].name};')

        function.add_body(Body())
        return function

    @staticmethod
    def set_value(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            None,
            f'setValue',
            f'缓存{config.remark}数据，默认1天时间',
            JavaCode.Attribute(config.className, config.low_name(), f"{config.remark}对象"),
        )

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line_if(f'{parameter[0].name} != null')
                self.line_annotation("默认缓存1天")
                self.line(f'baseRedisService.set(getKey({config.low_name()}.get{config.key.upper_name()}()), {parameter[0].name}, 1000 * 60 * 60 * 24);')
                self.block_end()

        function.add_body(Body())
        return function

    @staticmethod
    def get_value(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            JavaCode.Attribute(config.className, config.low_name(), f"{config.remark}对象"),
            f'getValue',
            f'获取缓存中的{config.remark}数据',
            JavaCode.Attribute(config.key.type, config.key.attr, f"{config.remark}对象的{config.key.attr}"),
        )

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line_if_one_block(f'{parameter[0].name} == null', f'return null;')
                self.line(f'Object object = baseRedisService.get(getKey({parameter[0].name}));')
                self.line_if(f'object != null && object instanceof {config.className}')
                self.line(f'return ({config.className}) object;')
                self.block_end()
                self.line(f'return null;')

        function.add_body(Body())
        return function

    @staticmethod
    def load_and_get(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            JavaCode.Attribute(config.className, config.low_name(), f"{config.remark}对象"),
            f'loadAndGet',
            f'加载并获取缓存中的{config.remark}数据',
            JavaCode.Attribute(config.key.type, config.key.attr, f"{config.remark}对象的{config.key.attr}"),
        )

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line_if_one_block(f'{parameter[0].name} == null', f'return null;')
                self.line_annotation(f'先从缓存中查询{config.remark}')
                self.line(f'{config.className} {config.low_name()} = getValue({parameter[0].name});')
                self.line_if(f'{config.low_name()} == null')
                self.line_annotation(f'从数据库中查询{config.remark}')
                self.line(f'{config.low_name()} = {config.module.mapperInterface.low_name()}.select{config.className}By{config.key.upper_name()}({parameter[0].name});')
                self.line_annotation(f'缓存{config.remark}')
                self.line(f'setValue({config.low_name()});')
                self.block_end()
                self.line(f'return {config.low_name()};')

        function.add_body(Body())
        return function

    @staticmethod
    def remove(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            None,
            f'removeValue',
            f'加载并获取缓存中的{config.remark}数据',
            JavaCode.Attribute(config.key.type, config.key.attr, f"{config.remark}对象的{config.key.attr}"),
        )

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line_if_one_block(f'{parameter[0].name} != null', f'baseRedisService.delete(getKey({parameter[0].name}));')

        function.add_body(Body())
        return function
