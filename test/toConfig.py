import json

from src.code.generateCode import Generate
from src.java import JavaCode
from src.java.CodeConfig import CodeConfig, Field, MultiTableParsing
from src.module.api.Controller import ControllerJavaCode
from src.module.base import BaseApi
from src.module.domain.Domain import DomainJavaCode
from src.module.domain.DomainImpl import DomainImplJavaCode
from src.module.repository.RepositoryImpl import RepositoryImplJavaCode
from src.module.repository.cache.Cache import CacheJavaCode
from src.module.repository.mapper.XmlBaseMapper import XmlBaseMapperCode
from src.module.repository.mapper.XmlMapper import XmlMapperCode
from src.module.service.Service import ServiceJavaCode
from src.module.service.ServiceImpl import ServiceImplJavaCode
from src.util.chiyaUtil import JsonUtil
import copy


def set_module(module, a, b, c, ):
    module.path = a
    module.className = b
    module.remark = c


package_name = "chiya.test"

codeConfig = CodeConfig()

set_module(codeConfig.module.entity, package_name + "user.entity", "TestUser", "测试类")
set_module(codeConfig.module.baseEntity, package_name + "user.entity", "BaseTestUser", "测试类")
set_module(codeConfig.module.controller, package_name + "user.controller", "TestUserController", "测试类")
set_module(codeConfig.module.serviceInterface, package_name + "user.service", "TestUserService", "测试类")
set_module(codeConfig.module.serviceImplements, package_name + "user.service", "TestUserServiceImpl", "测试类")
set_module(codeConfig.module.mapperInterface, package_name + "user.mapper", "TestUserMapper", "测试类")
set_module(codeConfig.module.baseMapperInterface, package_name + "user.mapper", "BaseTestUserMapper", "测试类")
set_module(codeConfig.module.domain, package_name + "user.domain", "TestUserDomain", "测试类")
set_module(codeConfig.module.domainImpl, package_name + "user.domain", "TestUserDomainImpl", "测试类")
set_module(codeConfig.module.repository, package_name + "user.repository", "TestUserRepository", "测试类")
set_module(codeConfig.module.repositoryImpl, package_name + "user.repository", "TestUserRepositoryImpl", "测试类")
set_module(codeConfig.module.cache, package_name + "user.cache", "TestUserCache", "测试类")
set_module(codeConfig.module.api, package_name + "user.controller", "TestUserApi", "测试类RPC")
set_module(codeConfig.module.mapperXml, package_name + "user.mapper", "TestUserMapper", "测试类")
set_module(codeConfig.module.baseMapperXml, package_name + "user.mapper", "BaseTestUserMapper", "测试类")
field = Field()
field.attr = "id"
field.type = "Integer"
field.remark = "用户id"
field.field = "user_id"

codeConfig.baseInfo.key = field
codeConfig.baseInfo.tableName = "test_user"

field = Field()
field.attr = "name"
field.type = "String"
field.remark = "用户名"
field.field = "user_name"
codeConfig.baseInfo.attr.append(field)

codeConfig.createConfig.repositoryUseCache.enable = True

config_json = JsonUtil.to_json(codeConfig)
new_config = CodeConfig.get_code_config(json.loads(config_json))

codeConfig.baseInfo.oneToOne.append(new_config)
codeConfig.baseInfo.oneToMany.append(new_config)

MultiTableParsing.parsing(codeConfig)
print()

Generate().parsing(codeConfig)
