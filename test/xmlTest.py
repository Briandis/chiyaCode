import json

from src.java.CodeConfig import CodeConfig, Field, MultiTableParsing, ManyToMany
from src.module.repository.mapper.XmlBaseMapper import XmlBaseMapperCode
from src.module.repository.mapper.XmlMapper import XmlMapperCode
from src.util.chiyaUtil import JsonUtil, StringUtil


def set_module(module, a, b, c, ):
    module.path = a
    module.className = b
    module.remark = c


def add_field(config, name, sql_field, java_type="String", remark="", is_key=False):
    field = Field()
    field.attr = name
    field.type = java_type
    field.remark = remark
    field.field = sql_field
    if is_key:
        config.baseInfo.key = field
    else:
        config.baseInfo.attr.append(field)


def skip_config(class_name, remark="", need_id=True):
    class_name = StringUtil.first_char_upper_case(class_name)
    config = CodeConfig()

    package = StringUtil.hump_to_underscore(class_name).replace("_", ".")

    set_module(config.module.entity, f"chiya.test.{package}.entity", class_name, f"{remark}类")
    set_module(config.module.baseEntity, f"chiya.test.{package}.entity", f"Base{class_name}", f"{remark}抽象类")
    set_module(config.module.mapperInterface, f"chiya.test.{package}.mapper", f"{class_name}Mapper", f"{remark}Mapper用户接口")
    set_module(config.module.baseMapperInterface, f"chiya.test.{package}.mapper", f"Base{class_name}Mapper", f"{remark}Mapper抽象接口")
    set_module(config.module.mapperXml, f"chiya.test.{package}.mapper", f"{class_name}Mapper", f"{remark}Mapper用户XML")
    set_module(config.module.baseMapperXml, f"chiya.test.{package}.mapper", f"Base{class_name}Mapper", f"{remark}Mapper抽象XML")

    if need_id:
        add_field(config, "id", f"{StringUtil.hump_to_underscore(class_name)}_id", "Integer", f"{remark}id", True)
    config.baseInfo.tableName = StringUtil.hump_to_underscore(class_name)
    return config


user_config = skip_config("User", "用户")
add_field(user_config, "name", "user_name", "String", "用户名")
add_field(user_config, "password", "user_password", "String", "用户名")
add_field(user_config, "phone", "user_phone", "String", "手机号")
add_field(user_config, "create_time", "user_create_time", "Date", "创建时间")

user_config.createConfig.fuzzySearch.data = ["user_name", "user_password"]
user_config.createConfig.fuzzySearch.value = "keyword"

user_sign = skip_config("UserSign", "用户签到", False)
add_field(user_sign, "userId", "user_id", "Integer", "用户id")
add_field(user_sign, "signCount", "sign_count", "Integer", "用户签到次数")
user_sign.baseInfo.foreignKey = "user_id"

game = skip_config("Game", "游戏")
add_field(game, "name", "name", "String", "游戏名称")
add_field(game, "createTime", "create_time", "Date", "创建时间")
game.baseInfo.foreignKey = "game_id"

game.createConfig.fuzzySearch.data = ["name"]

game_role = skip_config("GameRole", "用户游戏角色")
add_field(game_role, "userId", "user_id", "Integer", "用户id")
add_field(game_role, "gameId", "game_id", "Integer", "游戏id")
game_role.baseInfo.foreignKey = "user_id"

user_info = skip_config("UserInfo", "用户信息", False)
add_field(user_info, "userId", "user_id", "Integer", "用户id")
add_field(user_info, "info", "info", "String", "用户信息")
user_info.baseInfo.foreignKey = "user_phone"
user_info.createConfig.fuzzySearch.data = ["info"]

user_config.baseInfo.oneToOne.append(user_info)
user_config.baseInfo.oneToMany.append(user_sign)

many_to_many = ManyToMany()
many_to_many.to = game_role
many_to_many.many = game
user_config.baseInfo.manyToMany.append(many_to_many)

MultiTableParsing.parsing(user_config)
print()

code = XmlBaseMapperCode.create(user_config)
# code = XmlMapperCode.create(user_config)
print(code)
