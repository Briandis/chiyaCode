from src.ddd.util import JavaCode
from src.ddd.util.JavaCode import Attribute
from src.structure.CodeConfig import CodeConfig, Field


class CreateFile:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig):
        code = JavaCode.JavaCode(
            config.module.baseEntity.path,
            config.module.baseEntity.className + "<T>",
            f'{config.remark}实体'
        )
        code.is_abstract = True

        code.add_mate(f'@SuppressWarnings("unchecked")')
        CreateField.create_field(config.key, config, code)
        for field in config.attr:
            CreateField.create_field(field, config, code)
        ToString.create_field(config, code)
        return code.create()


class ToString:
    @staticmethod
    def create_field(config: CodeConfig, code: JavaCode.JavaCode):
        if config.createConfig.toJsonString.enable:
            if config.createConfig.toJsonString.isFastJson:
                code.add_import("com.alibaba.fastjson.JSON")

            class Body(JavaCode.FunctionBody):
                def function_body(self, parameter: list[Attribute]):
                    if config.createConfig.toJsonString.isFastJson:
                        self.line("return JSON.toJSONString(this);")
                    else:
                        self.line("StringBuilder builder = new StringBuilder();")
                        self.line(f'builder.append("{{");')
                        self.line(f'builder.append("\\"{config.key.attr}\\" : \\"" + {config.key.attr} + "\\"");')
                        self.line(f'builder.append(",");')
                        i = 0
                        for attr in config.attr:
                            self.line(f'builder.append("\\"{attr.attr}\\" : \\"" + {attr.attr} + "\\"");')
                            if i < len(config.attr) - 1:
                                self.line(f'builder.append(",");')
                            i += 1
                        self.line(f'builder.append("}}");')
                        self.line(f'return builder.toString();')

            code.add_function(
                JavaCode.Function(
                    "public",
                    JavaCode.Attribute("String", "", "对象字符化后的字符串"),
                    "toString",
                    "对象字符串化",
                ).add_mate("@Override").add_body(Body())
            )


class CreateField:

    @staticmethod
    def create_field(attr: Field, config: CodeConfig, code: JavaCode.JavaCode):
        # 属性
        code.add_attr(JavaCode.Attribute(attr.type, attr.attr, attr.remark))

        # get
        class Get(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'return {attr.attr};')

        code.add_function(
            JavaCode.Function(
                "public",
                JavaCode.Attribute(attr.type, "", attr.remark),
                f'get{attr.upper_name()}',
                f'获取{attr.remark}').add_body(Get())
        )

        # set
        class Set(JavaCode.FunctionBody):
            def function_body(self, parameter: list[Attribute]):
                self.line(f'this.{attr.attr} = {attr.attr};')

        code.add_function(
            JavaCode.Function(
                "public",
                None,
                f'set{attr.upper_name()}',
                f'设置{attr.remark}',
                JavaCode.Attribute(attr.type, attr.attr, attr.remark)
            ).add_body(Set())
        )
        # 如果链式操作启用的话
        if config.createConfig.chain.enable:
            # chain
            class Chain(JavaCode.FunctionBody):
                def function_body(self, parameter: list[Attribute]):
                    self.line(f'set{attr.upper_name()}({attr.attr});')
                    self.line(f'return (T) this;')

            code.add_function(
                JavaCode.Function(
                    "public",
                    JavaCode.Attribute("T", "", "对象本身"),
                    f'chain{attr.upper_name()}',
                    f'链式设置{attr.remark}',
                    JavaCode.Attribute(attr.type, attr.attr, attr.remark)
                ).add_body(Chain())
            )
