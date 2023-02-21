from src.java.CodeConfig import CodeConfig
from src.util.chiyaUtil import StringUtil


class MapperUtil:

    @staticmethod
    def get_database(code_config: CodeConfig):
        """
        获取拼接的数据库名称字符串
        :param code_config: 配置
        :return: 数据库名称的字符串
        """
        value = code_config.createConfig.databaseName.value
        if code_config.createConfig.databaseName.enable and StringUtil.is_not_null(value):
            return value
        return None

    @staticmethod
    def get_table_name(code_config: CodeConfig):
        """
        获取表明
        :param code_config:配置
        :return: 数据库命.表名
        """
        database_name = MapperUtil.get_database(code_config)
        if database_name is None:
            return code_config.baseInfo.tableName
        return f'{MapperUtil.get_database(code_config)}.{code_config.baseInfo.tableName}'

    @staticmethod
    def result_map_name(code_config: CodeConfig, other_config: CodeConfig = None, one_to_one=False, one_to_many=False, many_to_many=False):
        """
        获取 result_map的名称
        :param code_config:当前配置
        :param other_config: 多表的配置
        :param one_to_one: 是否一对一
        :param one_to_many: 是否一对多
        :param many_to_many: 是否多对多
        :return: 名字
        """
        if one_to_one:
            return f'result{code_config.module.entity.className}OneToOne{other_config.module.entity.className}'
        if one_to_many:
            return f'result{code_config.module.entity.className}OneToMany{other_config.module.entity.className}'
        if many_to_many:
            return f'result{code_config.module.entity.className}ManyToMany{other_config.module.entity.className}'
        return f'result{code_config.module.entity.className}'

    @staticmethod
    def join_all_field(code_config: CodeConfig, join=","):
        """
        获取全部字符拼成的字段
        :param code_config: 配置
        :param join: 拼接符
        :return: 拼接的字段
        """
        data = ""
        if code_config.baseInfo.key is not None:
            data += f'{code_config.baseInfo.key.field}{join}'
        for field in code_config.baseInfo.attr:
            data += f'{field.field}{join}'
        return data.strip(join)

    @staticmethod
    def sql_tag_name(code_config: CodeConfig):
        """
        获取sqlTag的名称
        :param code_config:配置
        :return: 名称
        """
        return f'sql_filed_{code_config.baseInfo.tableName}'
