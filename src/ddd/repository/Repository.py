from src.ddd.util import JavaCode
from src.structure.CodeConfig import CodeConfig


class CreateFile:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig):
        code = JavaCode.JavaCode(
            config.module.repository.path,
            config.module.repository.className,
            f'{config.remark}仓库层接口'
        )
        code.is_class = False
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
        function.set_is_interface()
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
        function.set_is_interface()
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
        function.set_is_interface()
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
        function.set_is_interface()
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
        function.set_is_interface()
        return function
