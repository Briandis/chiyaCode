from typing import List

from src.java.CodeConfig import CodeConfig
from src.java import JavaCode
from src.module.repository.mapper.JavaBaseMapper import BaseMapperJavaCode
from src.util.chiyaUtil import StringUtil


class TestCaseJavaCode:

    @staticmethod
    def create(config: CodeConfig):
        code = JavaCode.JavaCode(
            "auto.test",
            config.module.entity.className + "MapperCase",
            f'{config.module.entity.remark}针对Mapper的自动化测试用例'
        )

        code.add_import(config.module.entity.get_package())
        code.add_import(f'chiya.core.base.page.Page')
        code.add_import(f'chiya.core.base.pack.SelectPack')
        code.add_import(f'chiya.core.base.collection.ContainerUtil')
        code.add_import(f'chiya.core.base.random.RandomString')
        code.add_import(f'chiya.core.base.random.RandomUtil')
        code.add_import(f'java.util.Date')

        code.add_function(TestCaseJavaCode._create_test_function(config))
        return code.create()

    @staticmethod
    def _create_test_function(config: CodeConfig):
        function = JavaCode.Function(
            "public",
            None,
            "testCase",
            "测试用例方法",
            JavaCode.Attribute(
                config.module.mapperInterface.className,
                config.module.mapperInterface.low_name(),
                f'{config.module.entity.remark}缓存',
                config.module.mapperInterface.get_package(),
            ),
            is_static=True
        )

        class Body(JavaCode.FunctionBody):
            def function_body(self, parameter: list[JavaCode.Attribute]):
                code_obj = BaseMapperJavaCode.create_code_object(config)
                function.import_set.update(code_obj.import_set)
                data = ""
                for func in code_obj.function:
                    # 对每个方法进行用例生成
                    self.line_annotation(func.annotation)

                    if func.parameter is not None:
                        lists = []
                        count_len = 0
                        for param in func.parameter:
                            if param.type in ["Page"]:
                                param_str = f'new {param.type}()'
                            elif param.type == "Integer":
                                param_str = f'RandomUtil.randInt(10)'
                            elif param.type == "String":
                                param_str = f'null'
                            elif param.type == config.module.entity.className:
                                param_str = f'new {param.type}()'
                                chain_data = TestCaseJavaCode.create_entity_random_class(config)
                                for chain in chain_data:
                                    param_str += f'\n{"\t" * (self.indentation + 2)}{chain}'
                            elif "SelectPack" in param.type:
                                param_str = f'new {param.type}()'
                            elif "List" in param.type:
                                if "Integer" in param.type:
                                    param_str = f'ContainerUtil.createList(RandomUtil.randInt(10), RandomUtil.randInt(10), RandomUtil.randInt(10))'
                                elif config.module.entity.className in param.type:
                                    param_str = f'ContainerUtil.createList(\n'
                                    param_str += f'{"\t" * (self.indentation + 2)}new {config.module.entity.className}()'
                                    chain_data = TestCaseJavaCode.create_entity_random_class(config)
                                    for chain in chain_data:
                                        param_str += f'\n{"\t" * (self.indentation + 3)}{chain}'
                                    param_str += ',\n'
                                    param_str += f'{"\t" * (self.indentation + 2)}new {config.module.entity.className}()'
                                    chain_data = TestCaseJavaCode.create_entity_random_class(config)
                                    for chain in chain_data:
                                        param_str += f'\n{"\t" * (self.indentation + 3)}{chain}'

                                    param_str += f'\n{"\t" * (self.indentation + 1)})'
                                else:
                                    param_str = "null"
                            else:
                                param_str = "null"
                            lists.append(param_str)
                            count_len += len(param_str)
                        # 如果字符串大于85，则需要换行展示
                        if count_len > 85:
                            count = 0
                            data += f'\n'

                            self.line(f'{config.module.mapperInterface.low_name()}.{func.name}(')
                            self.indentation += 1
                            for i in lists:
                                if count + 1 == len(lists):
                                    self.line(f'{i}')
                                else:
                                    self.line(f'{i},')
                                count += 1
                            self.indent_sub(f');')
                        else:
                            self.line(f'{config.module.mapperInterface.low_name()}.{func.name}({StringUtil.string_join(", ", *lists)});')

                    self.line_blank()

        function.add_body(Body())
        return function

    @staticmethod
    def create_entity_random_class(config: CodeConfig) -> List[str]:
        res_data = []
        attr_list = []
        attr_list.extend(config.baseInfo.attr)
        for attr in attr_list:
            if attr.type in ["String", "Text"]:
                res_data.append(f'.chain{attr.upper_name()}(RandomString.randomString())')
            if attr.type in ["Integer", "Long"]:
                res_data.append(f'.chain{attr.upper_name()}(RandomUtil.randInt(10))')
            if attr.type in ["Date"]:
                res_data.append(f'.chain{attr.upper_name()}(new Date())')
        return res_data
