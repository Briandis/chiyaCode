from src.ddd.util import JavaCode
from src.structure.CodeConfig import CodeConfig


class CreateFile:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig):
        code = JavaCode.JavaCode(
            config.path,
            config.className,
            f'{config.remark}实体'
        )
        code.add_extend(JavaCode.Attribute(config.module.baseEntity.className + f'<{config.className}>', "", "", config.module.baseEntity.package))
        return code.create()
