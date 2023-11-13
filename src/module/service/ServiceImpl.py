from src.java import JavaCode
from src.java.CodeConfig import CodeConfig
from src.module.base.BaseApi import BaseAPIImpl, Template


class ServiceImplJavaCode:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig, service_attribute: JavaCode.Attribute, service_impl: Template, next_type):
        code = JavaCode.JavaCode(
            config.module.serviceImplements.path,
            config.module.serviceImplements.className,
            f'{config.module.entity.remark}业务层实现'
        )
        code.add_implement(JavaCode.Attribute(config.module.serviceInterface.className, "", "实现的业务层", config.module.serviceInterface.get_package()))
        code.add_mate(JavaCode.DefaultMate.Service())
        # 注入任意层
        code.add_attr(service_attribute)
        # 是否使用缓存，如果使用则添加该缓的熟悉
        if next_type == "mapper" and config.createConfig.repositoryUseCache.enable:
            code.add_attr(
                JavaCode.Attribute(
                    config.module.cache.className,
                    config.module.cache.low_name(),
                    f'{config.module.entity.remark}缓存',
                    config.module.cache.get_package(),
                ).add_mate(JavaCode.DefaultMate.Autowired())
            )

        service_impl.impl(config, code, code.get_attr_name(0))
        # 额外的接口
        service_impl.extra_impl(config, code, code.get_attr_name(0))

        return code.create()
