from src.ddd.util import JavaCode
from src.ddd.util.JavaCode import Attribute
from src.structure.CodeConfig import CodeConfig
from src.util import StringUtil


class CreateFile:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig):

        code = JavaCode.JavaCode(
            config.module.controller.path,
            config.module.controller.className,
            f'{config.remark}web接入层'
        )

        if config.createConfig.restful.enable:
            code.add_mate("@RestController")
        else:
            code.add_mate("@Controller")
        code.add_mate(f'@RequestMapping("/{config.low_name()}")')

        code.add_attr(
            JavaCode.Attribute(
                config.module.serviceInterface.className,
                config.module.serviceInterface.low_name(),
                f'{config.remark}业务接口',
                config.module.serviceInterface.package,
            ).add_mate("@Autowired").add_mate(f'@Qualifier("{config.module.serviceImplements.low_name()}")')
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
            JavaCode.Attribute("Result", "Result", "Result 业务对象"),
            f'{config.createConfig.methodName.get(0)}{config.className}',
            f'前台添加{config.remark}',
            JavaCode.Attribute(config.className, config.low_name(), f'{config.remark}对象'),
        )
        if config.createConfig.restful.enable:
            function.add_mate(f'@PostMapping("/{config.low_name()}")')
        else:
            function.add_mate(f'@RequestMapping("/{config.createConfig.methodName.get(0)}{config.className}")')
            function.add_mate(f'@ResponseBody')

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'boolean b = false;')
                self.line(f'b = {config.module.serviceInterface.low_name()}.{config.createConfig.methodName.get(0)}{config.className}({config.low_name()});')
                self.line(f'return Result.judge(b);')

        function.add_body(Body())
        return function

    @staticmethod
    def delete(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            JavaCode.Attribute("Result", "Result", "Result 业务对象"),
            f'{config.createConfig.methodName.get(1)}{config.className}',
            f'前台删除{config.remark},{config.key.attr}必传',
            JavaCode.Attribute(config.key.type, config.key.attr, f'{config.remark}的{config.key.attr}'),
        )
        if config.createConfig.restful.enable:
            function.add_mate(f'@DeleteMapping("/{config.low_name()}")')
        else:
            function.add_mate(f'@RequestMapping("/{config.createConfig.methodName.get(1)}{config.className}")')
            function.add_mate(f'@ResponseBody')

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'boolean b = false;')
                self.line_if(f'{config.key.attr} != null')
                self.line(f'b = {config.module.serviceInterface.low_name()}.{config.createConfig.methodName.get(1)}{config.className}({config.key.attr});')
                self.block_end()
                self.line(f'return Result.judge(b);')

        function.add_body(Body())
        return function

    @staticmethod
    def update(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            JavaCode.Attribute("Result", "Result", "Result 业务对象"),
            f'{config.createConfig.methodName.get(2)}{config.className}',
            f'前台修改{config.remark}',
            JavaCode.Attribute(config.className, config.low_name(), f'{config.remark}对象'),
        )
        if config.createConfig.restful.enable:
            function.add_mate(f'@PutMapping("/{config.low_name()}")')
        else:
            function.add_mate(f'@RequestMapping("/{config.createConfig.methodName.get(2)}{config.className}")')
            function.add_mate(f'@ResponseBody')

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'boolean b = false;')
                self.line_if(f'{config.low_name()}.get{config.key.upper_name()}() != null')
                self.line(f'b = {config.module.serviceInterface.low_name()}.{config.createConfig.methodName.get(2)}{config.className}({config.low_name()});')
                self.block_end()
                self.line(f'return Result.judge(b);')

        function.add_body(Body())
        return function

    @staticmethod
    def get(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            JavaCode.Attribute("Result", "Result", "Result 业务对象"),
            f'{config.createConfig.methodName.get(3)}{config.className}',
            f'前台根据{config.key.attr}查询一个{config.remark}',
            JavaCode.Attribute(config.key.type, config.key.attr, f'{config.remark}的{config.key.attr}'),
        )
        if config.createConfig.restful.enable:
            function.add_mate(f'@GetMapping("/{config.low_name()}")')
        else:
            function.add_mate(f'@RequestMapping("/{config.createConfig.methodName.get(3)}{config.className}")')
            function.add_mate(f'@ResponseBody')

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'boolean b = false;')
                self.line_if(f'{config.key.attr} != null')
                self.line(f'return Result.success({config.module.serviceInterface.low_name()}.{config.createConfig.methodName.get(3)}{config.className}({config.key.attr}));')
                self.block_end()
                self.line(f'return Result.judge(b);')

        function.add_body(Body())
        return function

    @staticmethod
    def lists(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            JavaCode.Attribute("Result", "Result", "Result 业务对象"),
            f'{config.createConfig.methodName.get(4)}{config.className}',
            f'前台获取多个{config.remark}',
            JavaCode.Attribute(config.className, config.low_name(), f'{config.remark}对象'),
            JavaCode.Attribute("Page", "page", f'分页对象'),
        )
        if config.createConfig.restful.enable:
            function.add_mate(f'@GetMapping("/{config.createConfig.methodName.get(4)}{config.className}")')
        else:
            function.add_mate(f'@RequestMapping("/{config.createConfig.methodName.get(4)}{config.className}")')
            function.add_mate(f'@ResponseBody')

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'List<{config.className}> list = {config.module.serviceInterface.low_name()}.{config.createConfig.methodName.get(4)}{config.className}({config.low_name()}, page);')
                self.line(f'return Result.success(list, page);')

        function.add_body(Body())
        return function
