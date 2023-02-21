from src.java import JavaCode
from src.java.CodeConfig import CodeConfig
from src.module.base.BaseApi import MapperApi


class CacheJavaCode:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig):
        code = JavaCode.JavaCode(
            config.module.cache.path,
            config.module.cache.className,
            f'{config.module.entity.remark}缓存层'
        )
        code.add_mate(JavaCode.DefaultMate.Service())

        code.add_attr(JavaCode.DefaultAttribute.get_mapper(config))
        code.add_import(config.module.entity.get_package())
        code.add_attr(
            JavaCode.Attribute(
                "BaseRedisService",
                "baseRedisService",
                f'Redis操作库',
                "chiya.web.redis.BaseRedisService",
            ).add_mate(JavaCode.DefaultMate.Autowired())
        )
        if config.baseInfo.key:
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
            JavaCode.Attribute("String", "string", f"{config.module.entity.remark}的唯一缓存key"),
            f'getKey',
            f'根据{config.module.entity.remark}的{config.baseInfo.key.attr}创建唯一key',
            JavaCode.DefaultAttribute.self_key(config)
        )

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line(f'return "{config.baseInfo.tableName.replace("_", ":")}:" + {parameter[0].name};')

        function.add_body(Body())
        return function

    @staticmethod
    def set_value(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            None,
            f'setValue',
            f'缓存{config.module.entity.remark}数据，默认1天时间',
            JavaCode.DefaultAttribute.self_class(config),
        )

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line_if(f'{parameter[0].name} != null')
                self.line_annotation("默认缓存1天")
                self.line(f'baseRedisService.set(getKey({parameter[0].name}.get{config.baseInfo.key.upper_name()}()), {parameter[0].name}, 1000 * 60 * 60 * 24);')
                self.block_end()

        function.add_body(Body())
        return function

    @staticmethod
    def get_value(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.self_class(config),
            f'getValue',
            f'获取缓存中的{config.module.entity.remark}数据',
            JavaCode.DefaultAttribute.self_key(config)
        )

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line_if_one_block(f'{parameter[0].name} == null', f'return null;')
                self.line(f'Object object = baseRedisService.get(getKey({parameter[0].name}));')
                self.line_if(f'object != null && object instanceof {config.module.entity.className}')
                self.line(f'return ({config.module.entity.className}) object;')
                self.block_end()
                self.line(f'return null;')

        function.add_body(Body())
        return function

    @staticmethod
    def load_and_get(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            JavaCode.DefaultAttribute.self_class(config),
            f'loadAndGet',
            f'加载并获取缓存中的{config.module.entity.remark}数据',
            JavaCode.DefaultAttribute.self_key(config),
        )

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line_if_one_block(f'{parameter[0].name} == null', f'return null;')
                self.line_annotation(f'先从缓存中查询{config.module.entity.remark}')
                self.line(f'{config.module.entity.className} {config.module.entity.low_name()} = getValue({parameter[0].name});')
                self.line_if(f'{config.module.entity.low_name()} == null')
                self.line_annotation(f'从数据库中查询{config.module.entity.remark}')
                self.line(f'{config.module.entity.low_name()} = {config.module.mapperInterface.low_name()}.{MapperApi.Select.select_by_id(config)}({parameter[0].name});')
                self.line_annotation(f'缓存{config.module.entity.remark}')
                self.line(f'setValue({config.module.entity.low_name()});')
                self.block_end()
                self.line(f'return {config.module.entity.low_name()};')

        function.add_body(Body())
        return function

    @staticmethod
    def remove(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            None,
            f'removeValue',
            f'加载并获取缓存中的{config.module.entity.remark}数据',
            JavaCode.DefaultAttribute.self_key(config)
        )

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                self.line_if_one_block(f'{parameter[0].name} != null', f'baseRedisService.delete(getKey({parameter[0].name}));')

        function.add_body(Body())
        return function
