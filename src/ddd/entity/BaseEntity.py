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

        field_list = FieldMap.get_map_filed(config, code)

        for field in field_list:
            CreateField.create_field(field, config, code)

        ToString.create_field(field_list, config, code)
        return code.create()


# 生成全部的字段信息
class FieldMap:
    @staticmethod
    def get_map_filed(config: CodeConfig, code: JavaCode.JavaCode):
        """
        获取字段列表
        :param config:配置信息
        :return: 字段列表
        """
        field_map = {
            config.key.attr: config.key
        }
        for attr in config.attr:
            field_map[attr.attr] = attr

        for obj in config.oneToOne:
            field = Field()
            field.attr = obj.low_name()
            field.type = obj.className
            field.remark = obj.remark
            field_map[field.attr] = field
            code.add_import(obj.package)

        for obj in config.oneToMany:
            field = Field()
            field.attr = f'list{obj.className}'
            field.type = f'List<{obj.className}>'
            field.remark = obj.remark
            field_map[field.attr] = field
            code.add_import(obj.package)

        for obj in config.manyToMany:
            field = Field()
            field.attr = f'list{obj.many.className}'
            field.type = f'List<{obj.many.className}>'
            field.remark = obj.many.remark
            field_map[field.attr] = field
            code.add_import(obj.many.package)

        return field_map.values()


# 字符串方法
class ToString:
    @staticmethod
    def create_field(field_list, config: CodeConfig, code: JavaCode.JavaCode):
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
                        i = 0
                        for attr in field_list:
                            self.line(f'builder.append("\\"{attr.attr}\\" : \\"" + {attr.attr} + "\\"");')
                            if i < len(field_list) - 1:
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
