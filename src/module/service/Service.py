from src.java import JavaCode
from src.java.CodeConfig import CodeConfig
from src.module.base.BaseApi import BaseApi


class ServiceJavaCode:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig):
        code = JavaCode.JavaCode(
            config.module.serviceInterface.path,
            config.module.serviceInterface.className,
            f'{config.module.entity.remark}业务层'
        )
        code.is_class = False
        # 基础接口
        BaseApi.api(config, code)
        # 额外的接口
        BaseApi.extra_api(config, code)

        return code.create()
