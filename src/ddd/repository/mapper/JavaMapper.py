from src.ddd.util import JavaCode
from src.structure.CodeConfig import CodeConfig


class CreateFile:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig):
        code = JavaCode.JavaCode(
            config.module.mapperInterface.path,
            config.module.mapperInterface.className,
            f'{config.remark}mapper层'
        )
        code.is_class = False
        code.add_mate("@Mapper")

        code.add_extend(JavaCode.Attribute(config.module.baseMapperInterface.className, "", "抽象的mapper接口"))
        return code.create()
