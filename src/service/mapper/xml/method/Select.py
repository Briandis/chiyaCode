from src.service.mapper.xml.method.Block import CreateXmlBlock
from src.util import StringUtil


class CreateMethodSelect:
    """
    创建查询方法
    """

    @staticmethod
    def getResult(config):
        """
        获取返回类型
        :param config: 配置文件
        :return: map 或 type
        """
        if config["config"]["resultMap"]["enable"]:
            return f'resultMap="{config["config"]["xmlConfig"]["resultMapName"]}{config["className"]}"'
        else:
            return f'resultType="{config["path"]}"'

    # 创建查询块
    @staticmethod
    def __create_select_by_key(config):
        """
        创建查询块
        :param config: 配置文件
        """
        className = config["className"]
        key = config["key"]["attr"]
        upperKey = StringUtil.first_char_upper_case(key)
        keyFiled = config["key"]["filed"]
        tableName = config["tableName"]

        tag = "\t"
        res_type = CreateMethodSelect.getResult(config)

        data = f'{tag}<select id="select{className}By{upperKey}" {res_type}>\n'
        data += f'{tag * 2}SELECT * FROM {tableName} WHERE {keyFiled} = #{{{key}}}\n'
        data += f'{tag}</select>\n\n'
        return data

    # 根据id获取多个对象
    @staticmethod
    def __create_select_in_key(config):
        """
        根据id获取多个对象
        :param config: 配置文件
        """
        className = config["className"]
        key = config["key"]["attr"]
        upperKey = StringUtil.first_char_upper_case(key)
        keyFiled = config["key"]["filed"]
        tableName = config["tableName"]

        tag = "\t"
        res_type = CreateMethodSelect.getResult(config)
        data = f'{tag}<select id="select{className}In{upperKey}" {res_type}>\n'
        data += f'{tag * 2}SELECT * FROM {tableName} WHERE {keyFiled} IN \n'
        data += f'{tag * 3}<foreach item="item" index="index" collection="list" open="(" separator="," close=")">#{{item}}</foreach>\n'
        data += f'{tag}</select>\n\n'
        return data

    # 查询一个
    @staticmethod
    def __create_select_one(config):
        """
        根据主键条件删除
        :param config: 配置文件
        """
        className = config["className"]
        lowClassName = StringUtil.first_char_lower_case(className)
        key = config["key"]["attr"]
        tableName = config["tableName"]

        tag = "\t"
        res_type = CreateMethodSelect.getResult(config)
        data = f'{tag}<select id="selectOne{className}" {res_type}>\n'
        data += f'{tag * 2}SELECT * FROM {tableName}\n'
        data += f'{tag * 2}<where>\n'
        data += CreateXmlBlock.where_mod_1(config, 3, lowClassName)
        data += f'{tag * 2}</where>\n'
        data += f'{tag * 2}limit #{{index}},1'
        data += f'{tag}</select>\n\n'
        return data

    # 查询记录
    @staticmethod
    def __create_select(config):
        """
        查询记录
        :param config: 配置文件
        """
        className = config["className"]
        lowClassName = StringUtil.first_char_lower_case(className)
        tableName = config["tableName"]

        tag = "\t"
        res_type = CreateMethodSelect.getResult(config)

        data = f'{tag}<select id="select{className}" {res_type}>\n'
        data += f'{tag * 2}SELECT * FROM {tableName}\n'
        data += f'{tag * 2}<where>\n'
        data += CreateXmlBlock.where_mod_1(config, 3, lowClassName)
        data += f'{tag * 2}</where>\n'
        data += CreateXmlBlock.splicing_sql(config)
        data += CreateXmlBlock.page()
        data += f'{tag}</select>\n\n'
        return data

    # 统计查询
    @staticmethod
    def __create_count_select(config):
        """
        统计查询
        :param config: 配置文件
        """
        className = config["className"]
        lowClassName = StringUtil.first_char_lower_case(className)
        key = config["key"]["attr"]
        tableName = config["tableName"]

        tag = "\t"

        data = f'{tag}<select id="count{className}" resultType="int">\n'
        data += f'{tag * 2}SELECT COUNT(*) FROM {tableName}\n'
        data += f'{tag * 2}<where>\n'
        data += CreateXmlBlock.where_mod_1(config, 3, lowClassName)
        data += f'{tag * 2}</where>\n'
        data += f'{tag}</select>\n\n'
        return data

    @staticmethod
    def create(config):
        data = ""
        data += CreateMethodSelect.__create_select_by_key(config)
        data += CreateMethodSelect.__create_select_in_key(config)
        data += CreateMethodSelect.__create_select_one(config)
        data += CreateMethodSelect.__create_select(config)
        data += CreateMethodSelect.__create_count_select(config)
        return data
