from src.java import JavaCode
from src.java.CodeConfig import CodeConfig
from src.module.base.BaseApi import BaseApi


class DomainJavaCode:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig):
        code = JavaCode.JavaCode(
            config.module.domain.path,
            config.module.domain.className,
            f'{config.module.entity.remark}领域层接口'
        )
        code.is_class = False
        # 基础接口
        BaseApi.api(config, code)

        return code.create()

