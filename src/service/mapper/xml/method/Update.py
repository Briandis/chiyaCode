from src.service.mapper.xml.method.Block import CreateXmlBlock
from src.util import StringUtil


class CreateMethodUpdate:
    """
    创建更新方法
    """

    # 创建修改块
    @staticmethod
    def __create_update(config):
        """
        创建修改块
        :param config: 配置文件
        """
        if "key" not in config:
            return ""
        className = config["className"]
        key = config["key"]["attr"]
        upperKey = StringUtil.first_char_upper_case(key)
        keyFiled = config["key"]["filed"]
        tableName = config["tableName"]

        tag = "\t"
        data = f'{tag}<update id="update{className}By{upperKey}">\n'
        data += f'{tag * 2}UPDATE {tableName}\n'
        data += f'{tag * 2}<set>\n'
        data += CreateXmlBlock.if_mod_3(config, 3)
        data += f'{tag * 2}</set>\n'
        data += f'{tag * 2}WHERE {keyFiled} = #{{{key}}}\n'
        data += f'{tag}</update>\n\n'
        return data

    # 不重复则修改
    @staticmethod
    def __create_update_not_repeat(config):
        """
        不重复则修改
        :param config: 配置文件
        """
        className = config["className"]
        key = None
        if "key" in config:
            key = config["key"]["attr"]
            keyFiled = config["key"]["filed"]
        tableName = config["tableName"]

        tag = "\t"
        data = f'{tag}<update id="update{className}ByNotRepeatWhere">\n'
        data += f'{tag * 2}UPDATE {tableName}\n'
        data += f'{tag * 2}<set>\n'
        data += CreateXmlBlock.if_mod_3(config, 3, f'save{className}')
        data += f'{tag * 2}</set>\n'
        if key:
            data += f'{tag * 2}WHERE {keyFiled} = #{{save{className}.{key}}}\n'
        else:
            data += f'{tag * 2}WHERE\n'

        temp_str = f'condition{className}.{key}!=null'
        for attr in config["attr"]:
            temp_str += f' or condition{className}.{attr["attr"]}!=null'

        data += f'{tag * 2}<if test="condition{className}!=null and ({temp_str})">\n'
        data += f'{tag * 3}AND NOT EXISTS (\n'
        if key:
            data += f'{tag * 4}SELECT {keyFiled} FROM (SELECT * FROM {tableName} ) AS t \n'
        else:
            data += f'{tag * 4}SELECT * FROM (SELECT * FROM {tableName} ) AS t \n'
        data += f'{tag * 4}<where>\n'
        data += CreateXmlBlock.where_mod_2(config, 5, f'condition{className}', False, "t")
        data += f'{tag * 4}</where>\n'
        data += f'{tag * 3})\n'
        data += f'{tag * 2}</if>\n'
        data += f'{tag}</update>\n\n'
        return data

    # 根据id和其他条件更新
    @staticmethod
    def __create_update_by_key_and_where(config):
        """
        根据主键条件删除
        :param config: 配置文件
        """
        if "key" not in config:
            return ""
        className = config["className"]
        key = config["key"]["attr"]
        upperKey = StringUtil.first_char_upper_case(key)
        keyFiled = config["key"]["filed"]
        tableName = config["tableName"]

        tag = "\t"
        data = f'{tag}<update id="update{className}By{upperKey}AndWhere">\n'
        data += f'{tag * 2}UPDATE {tableName}\n'
        data += f'{tag * 2}<set>\n'
        data += CreateXmlBlock.if_mod_3(config, 3, f'save{className}')
        data += f'{tag * 2}</set>\n'
        data += f'{tag * 2}<where>\n'
        data += f'{tag * 3}{keyFiled} = #{{save{className}.{key}}}\n'
        data += CreateXmlBlock.where_mod_2(config, 3, f'condition{className}', False)
        data += f'{tag * 2}</where>\n'
        data += f'{tag}</update>\n\n'
        return data

    # 根据条件修改
    @staticmethod
    def __create_update_by_where(config):
        """
        根据条件修改
        :param config: 配置文件
        """
        if "key" not in config:
            return ""
        className = config["className"]
        key = config["key"]["attr"]
        keyFiled = config["key"]["filed"]
        tableName = config["tableName"]

        tag = "\t"
        data = f'{tag}<update id="update{className}">\n'
        data += f'{tag * 2}UPDATE {tableName}\n'
        data += f'{tag * 2}<set>\n'
        data += CreateXmlBlock.if_mod_3(config, 3, f'save{className}')
        data += f'{tag * 2}</set>\n'
        data += f'{tag * 2}<where>\n'
        data += f'{tag * 3}<if test="save{className}.{key}!=null">\n'
        data += f'{tag * 4}AND {keyFiled} = #{{save{className}.{key}}}\n'
        data += f'{tag * 3}</if>\n'
        data += CreateXmlBlock.where_mod_2(config, 3, f'condition{className}', False)
        data += f'{tag * 2}</where>\n'
        data += f'{tag}</update>\n\n'
        return data

    # 根据传入参数设置Null
    @staticmethod
    def __create_update_null(config):
        """
        根据传入参数设置Null
        :param config: 配置文件
        """
        if "key" not in config:
            return ""
        className = config["className"]
        key = config["key"]["attr"]
        upperKey = StringUtil.first_char_upper_case(key)
        keyFiled = config["key"]["filed"]
        tableName = config["tableName"]

        tag = "\t"
        data = f'{tag}<update id="update{className}SetNullBy{upperKey}">\n'
        data += f'{tag * 2}UPDATE {tableName}\n'
        data += f'{tag * 2}<set>\n'
        data += CreateXmlBlock.if_is_null(config, 3)
        data += f'{tag * 2}</set>\n'
        data += f'{tag * 2}WHERE {keyFiled} = #{{{key}}}\n'
        data += f'{tag}</update>\n\n'
        return data

    @staticmethod
    def create(config):
        data = ""
        data += CreateMethodUpdate.__create_update(config)
        data += CreateMethodUpdate.__create_update_not_repeat(config)
        data += CreateMethodUpdate.__create_update_by_key_and_where(config)
        data += CreateMethodUpdate.__create_update_by_where(config)
        data += CreateMethodUpdate.__create_update_null(config)
        return data
