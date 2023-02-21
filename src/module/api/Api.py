from src.java.CodeConfig import CodeConfig
from src.java import JavaCode


class APIJavaCode:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig):
        code = JavaCode.JavaCode(
            config.module.api.path,
            config.module.api.className,
            f'{config.module.entity.remark}RPC接入层'
        )
        return code.create()
