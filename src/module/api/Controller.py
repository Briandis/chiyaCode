from src.java.CodeConfig import CodeConfig
from src.java import JavaCode
from src.module.base.BaseApi import WebApi


class ControllerJavaCode:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig, service_attribute: JavaCode.Attribute):

        code = JavaCode.JavaCode(
            config.module.controller.path,
            config.module.controller.className,
            f'{config.module.entity.remark}web接入层'
        )

        if config.createConfig.restful.enable:
            code.add_mate(JavaCode.DefaultMate.RestController())
        else:
            code.add_mate(JavaCode.DefaultMate.Controller())
        code.add_mate(JavaCode.DefaultMate.RequestMapping(config.module.entity.low_name()))
        # 注入任符合的service层对象
        code.add_attr(service_attribute)
        code.add_import(config.module.entity.get_package())

        WebApi.api(config, code, code.get_attr_name(0))
        WebApi.extra_api(config, code, code.get_attr_name(0))

        return code.create()
