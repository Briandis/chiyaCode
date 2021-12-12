from src.service.mapper.xml.method.Block import CreateXmlBlock
from src.util import StringUtil


class CreateMethodDelete:
    """
    创建删除方法
    """

    # 创建删除块
    @staticmethod
    def __create_delete(config):
        """
        创建删除块
        :param config: 配置文件
        """
        className = config["className"]
        key = config["key"]["attr"]
        upperKey = StringUtil.first_char_upper_case(key)
        keyFiled = config["key"]["filed"]
        tableName = config["tableName"]

        tag = "\t"
        data = f'{tag}<delete id="delete{className}By{upperKey}">\n'
        data += f'{tag * 2}DELETE FROM {tableName} WHERE {keyFiled} = #{{{key}}}\n'
        data += f'{tag}</delete>\n\n'
        return data

    # 创建批量删除id块
    @staticmethod
    def __create_delete_list(config):
        """
        创建批量删除id块
        :param config: 配置文件
        """
        className = config["className"]
        key = config["key"]["attr"]
        upperKey = StringUtil.first_char_upper_case(key)
        keyFiled = config["key"]["filed"]
        tableName = config["tableName"]

        tag = "\t"
        data = f'{tag}<delete id="delete{className}In{upperKey}">\n'
        data += f'{tag * 2}DELETE FROM {tableName} WHERE {keyFiled} IN\n'
        data += f'{tag * 3}<foreach item="item" index="index" collection="list" open="(" separator="," close=")">#{{item}}</foreach>\n'
        data += f'{tag}</delete>\n\n'
        return data

    # 根据主键条件删除
    @staticmethod
    def __create_delete_by_key_and_where(config):
        """
        根据主键条件删除
        :param config: 配置文件
        """
        className = config["className"]
        lowClassName = StringUtil.first_char_lower_case(className)
        key = config["key"]["attr"]
        upperKey = StringUtil.first_char_upper_case(key)
        keyFiled = config["key"]["filed"]
        tableName = config["tableName"]

        tag = "\t"
        data = f'{tag}<delete id="delete{className}By{upperKey}AndWhere">\n'
        data += f'{tag * 2}DELETE FROM {tableName}\n'
        data += f'{tag * 2}<where>\n'
        data += f'{tag * 3}{keyFiled} = #{{{key}}}\n'
        data += CreateXmlBlock.where_mod_1(config, 3, lowClassName)
        data += f'{tag * 2}</where>\n'
        data += f'{tag}</delete>\n\n'
        return data

    # 根据条件删除
    @staticmethod
    def __create_delete_by_where(config):
        """
        根据条件删除
        :param config: 配置文件
        """
        className = config["className"]
        lowClassName = StringUtil.first_char_lower_case(className)
        tableName = config["tableName"]

        tag = "\t"
        data = f'{tag}<delete id="delete{className}">\n'
        data += f'{tag * 2}DELETE FROM {tableName}\n'
        data += f'{tag * 2}<where>\n'
        data += f'{CreateXmlBlock.where_mod_1(config, 3, lowClassName)}'
        data += f'{tag * 2}</where>\n'
        data += f'{tag}</delete>\n\n'
        return data

    # 假删
    @staticmethod
    def __create_false_delete(config):
        """
        假删
        :param config: 配置文件
        """
        className = config["className"]
        key = config["key"]["attr"]
        upperKey = StringUtil.first_char_upper_case(key)
        keyFiled = config["key"]["filed"]
        tableName = config["tableName"]
        deleteKey = config["config"]["falseDelete"]["deleteKey"]
        deleteValue = config["config"]["falseDelete"]["deleteValue"]

        updateTime = ""
        if config["config"]["falseDelete"]["isUpdate"]:
            updateTime = config["config"]["falseDelete"]["updateKey"]
            updateTime = f', {updateTime} = NOW() '
        tag = "\t"
        data = f'{tag}<update id="falseDelete{className}By{upperKey}">\n'
        data += f'{tag * 2}UPDATE {tableName} SET {deleteKey} = {deleteValue} {updateTime}WHERE {keyFiled} = #{{{key}}}\n'
        data += f'{tag}</update>\n\n'
        return data

    @staticmethod
    def create(config):
        data = ""
        data += CreateMethodDelete.__create_delete(config)
        data += CreateMethodDelete.__create_delete_list(config)
        data += CreateMethodDelete.__create_delete_by_key_and_where(config)
        data += CreateMethodDelete.__create_delete_by_where(config)
        if config["config"]["falseDelete"]["enable"]:
            data += CreateMethodDelete.__create_false_delete(config)
        return data
