from src.java import JavaCode
from src.java.CodeConfig import CodeConfig


class MapperJavaCode:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig):
        code = JavaCode.JavaCode(
            config.module.mapperInterface.path,
            config.module.mapperInterface.className,
            f'{config.module.entity.remark}mapper层'
        )
        code.is_class = False
        code.add_mate(JavaCode.DefaultMate.Mapper())

        code.add_extend(JavaCode.Attribute(config.module.baseMapperInterface.className, "", "抽象的mapper接口"))
        return code.create()
