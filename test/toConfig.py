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


codeConfig = CodeConfig()

set_module(codeConfig.module.entity, "chiya.test.user.entity", "TestUser", "测试类")
set_module(codeConfig.module.baseEntity, "chiya.test.user.entity", "BaseTestUser", "测试类")
set_module(codeConfig.module.controller, "chiya.test.user.controller", "TestUserController", "测试类")
set_module(codeConfig.module.serviceInterface, "chiya.test.user.service", "TestUserService", "测试类")
set_module(codeConfig.module.serviceImplements, "chiya.test.user.service.impl", "TestUserServiceImpl", "测试类")
set_module(codeConfig.module.mapperInterface, "chiya.test.user.mapper", "TestUserMapper", "测试类")
set_module(codeConfig.module.baseMapperInterface, "chiya.test.user.mapper", "BaseTestUserMapper", "测试类")
set_module(codeConfig.module.domain, "chiya.test.user.domain", "TestUserDomain", "测试类")
set_module(codeConfig.module.domainImpl, "chiya.test.user.domain.impl", "TestUserDomainImpl", "测试类")
set_module(codeConfig.module.repository, "chiya.test.user.repository", "TestUserRepository", "测试类")
set_module(codeConfig.module.repositoryImpl, "chiya.test.user.repository.impl", "TestUserRepositoryImpl", "测试类")
set_module(codeConfig.module.cache, "chiya.test.user.cache", "TestUserCache", "测试类")
set_module(codeConfig.module.api, "chiya.test.user.controller", "TestUserApi", "测试类RPC")
set_module(codeConfig.module.mapperXml, "chiya.test.user.mapper", "TestUserMapper", "测试类")
set_module(codeConfig.module.baseMapperXml, "chiya.test.user.mapper", "BaseTestUserMapper", "测试类")
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
