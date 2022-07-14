from src.project.common import bootstrap, cache, converter, exception, threadSession, security, securityTask
from src.project.config import globalCorsConfig, redisConfig, webConfig, beanConfig
from src.util import OSUtil


def create_project_init(root: str):
    """
    创建工程初始化目录
    :param root: 包名路径
    :return:
    """
    project = []
    """
    生成的结构
    |-root
        |-common
            |-bootstrap
            |-converter
            |-entity
                |-constant
                |-enums
                |-factory
            |-exception
            |-stream
            |-util
        |-config
        |-module 
    """
    project.append(f'{root}.common.bootstrap')
    project.append(f'{root}.common.converter')
    project.append(f'{root}.common.entity.constant')
    project.append(f'{root}.common.entity.enums')
    project.append(f'{root}.common.entity.factory')
    project.append(f'{root}.common.exception')
    project.append(f'{root}.common.module.cache')
    project.append(f'{root}.common.module.security')
    project.append(f'{root}.common.stream')
    project.append(f'{root}.common.util')

    project.append(f'{root}.config')

    project.append(f'{root}.module')

    for path in project:
        OSUtil.create_dir(path)


def create_java_file(root: str):
    """
    构建java文件
    :param root:模块路径
    """
    bootstrap.create_file(root)
    cache.create_file(root)
    converter.create_file(root)
    exception.create_file(root)
    globalCorsConfig.create_file(root)
    redisConfig.create_file(root)
    webConfig.create_file(root)
    threadSession.create_file(root)
    beanConfig.create_file(root)
    security.create_file(root)
    securityTask.create_file(root)


def init(root: str):
    """
    构建项目，进行初始化
    :param root:包所在路径
    """
    create_project_init(root)
    create_java_file(root)
