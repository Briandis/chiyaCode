from src.java import JavaCode
from src.java.CodeConfig import CodeConfig
from src.module.base.BaseApi import BaseApi


class RepositoryJavaCode:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig):
        code = JavaCode.JavaCode(
            config.module.repository.path,
            config.module.repository.className,
            f'{config.module.entity.remark}仓库层接口'
        )
        code.is_class = False
        BaseApi.api(config, code)

        return code.create()
