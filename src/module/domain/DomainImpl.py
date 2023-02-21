from src.java import JavaCode
from src.java.CodeConfig import CodeConfig
from src.module.base.BaseApi import Template


class DomainImplJavaCode:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig, service_attribute: JavaCode.Attribute, service_impl: Template):
        code = JavaCode.JavaCode(
            config.module.domainImpl.path,
            config.module.domainImpl.className,
            f'{config.module.entity.remark}领域层实现'
        )
        code.add_implement(JavaCode.Attribute(config.module.domain.className, "", "实现的业务层", config.module.domain.get_package()))
        code.add_mate(JavaCode.DefaultMate.Service())

        code.add_attr(service_attribute)

        service_impl.impl(config, code, code.get_attr_name(0))

        return code.create()
