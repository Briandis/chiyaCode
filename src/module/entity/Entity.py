from src.java import JavaCode
from src.java.CodeConfig import CodeConfig


class EntityJavaCode:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig):
        code = JavaCode.JavaCode(
            config.module.entity.path,
            config.module.entity.className,
            f'{config.module.entity.remark}实体'
        )
        code.add_extend(JavaCode.Attribute(config.module.baseEntity.className + f'<{config.module.entity.className}>', "", "", config.module.baseEntity.get_package()))
        return code.create()
