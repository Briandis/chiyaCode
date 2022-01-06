from src.constant.ProtocolConstant import JsonKey
from src.util import util


class CreateXmlBlock:
    """
    创建XML块
    """

    @staticmethod
    def if_mod_1(config: dict, indent: int, prefix=None):
        """
        <if test="prefix.attr!=null">filed,</if>
        :param config: 配置文件
        :param indent: 缩进
        :param prefix: 前缀
        """
        tap = "\t" * indent
        i, max_len, data = 0, len(config["attr"]), ""
        prefix = util.if_return(prefix, f"{prefix}.", "")

        for attr in config["attr"]:
            i += 1
            dian = util.if_return(i == max_len, "", ",")
            data += f'{tap}<if test="{prefix}{attr["attr"]}!=null">{attr["filed"]}{dian}</if>\n'
        return data

    @staticmethod
    def if_mod_2(config: dict, indent: int, prefix=None):
        """
        <if test="prefix.attr!=null">#{prefix.attr},</if>
        :param config: 配置文件
        :param indent: 缩进
        :param prefix: 前缀
        """
        tap = "\t" * indent
        i, max_len, data = 0, len(config["attr"]), ""
        prefix = util.if_return(prefix, f"{prefix}.", "")

        for attr in config["attr"]:
            i += 1
            dian = util.if_return(i == max_len, "", ",")
            data += f'{tap}<if test="{prefix}{attr["attr"]}!=null">#{{{prefix}{attr["attr"]}}}{dian}</if>\n'
        return data

    @staticmethod
    def if_mod_3(config: dict, indent: int, prefix=None):
        """
        <if test="prefix.attr!=null">filed = #{prefix.attr},</if>
        :param config: 配置文件
        :param indent: 缩进
        :param prefix: 前缀
        """
        tap = "\t" * indent
        i, max_len, data = 0, len(config["attr"]), ""
        prefix = util.if_return(prefix, f"{prefix}.", "")

        for attr in config["attr"]:
            i += 1
            dian = util.if_return(i == max_len, "", ",")
            data += f'{tap}<if test="{prefix}{attr["attr"]}!=null">{attr["filed"]} = #{{{prefix}{attr["attr"]}}}{dian}</if>\n'
        return data

    @staticmethod
    def if_mod_4(config: dict, indent: int, prefix=None):
        """
        <if test="prefix.attr!=null">AND filed = #{prefix.attr}</if>
        :param config: 配置文件
        :param indent: 缩进
        :param prefix: 前缀
        """
        tap = "\t" * indent
        i, max_len, data = 0, len(config["attr"]), ""
        prefix = util.if_return(prefix, f"{prefix}.", "")

        for attr in config["attr"]:
            data += f'{tap}<if test="{prefix}{attr["attr"]}!=null">AND {attr["filed"]} = #{{{prefix}{attr["attr"]}}}</if>\n'
        return data

    @staticmethod
    def if_is_null(config: dict, indent: int, prefix=None):
        """
        <if test="prefix.attr!=null">AND filed = #{prefix.attr}</if>
        :param config: 配置文件
        :param indent: 缩进
        :param prefix: 前缀
        """
        tap = "\t" * indent
        i, max_len, data = 0, len(config["attr"]), ""
        prefix = util.if_return(prefix, f"{prefix}.", "")
        for attr in config["attr"]:
            i += 1
            dian = util.if_return(i == max_len, "", ",")
            data += f'{tap}<if test="{prefix}{attr["attr"]}!=null">{attr["filed"]} = NULL{dian}</if>\n'
        return data

    # 创建模糊搜索块
    @staticmethod
    def fuzzy_search(config: dict, indent: int, table="", suffix=""):
        """
        创建模糊搜索块
        :param config: 配置文件
        :param indent: 缩进
        :param table:所属表
        :param suffix:后缀
        :return: if .... and (a like #{keyWord} or b like #{keyword})
        """
        tag = "\t"
        block_str = ""
        if config["config"]["fuzzySearch"]["enable"] and len(config["config"]["fuzzySearch"]["data"]) > 0:
            key_word_name = config["config"]["fuzzySearch"]["value"]
            if key_word_name is not None:
                key_word_name = key_word_name.strip()
            else:
                key_word_name = config["config"]["fuzzySearch"]["default"]
            if key_word_name == "":
                key_word_name = config["config"]["fuzzySearch"]["default"]

            code = ""
            i = 0
            block_str = f'{tag * indent}<if test="{key_word_name}{suffix}!=null">\n'
            for filed in config["config"]["fuzzySearch"]["data"]:
                if i == 0:
                    code = f'{table}{filed} LIKE #{{{key_word_name}{suffix}}}'
                    i = 1
                else:
                    code += f' OR {table}{filed} LIKE #{{{key_word_name}{suffix}}}'
            block_str += f'{tag * (indent + 1)}AND ({code})\n'
            block_str += f'{tag * indent}</if>\n'
        return block_str

    # 获取SQL注入块
    @staticmethod
    def splicing_sql(config: dict, indent=2):
        """
        获取SQL注入块
        :param config: 配置文件
        :param indent: 缩进
        """
        tag = "\t" * indent
        data = ""
        if config["config"]["splicingSQL"]["enable"]:
            splicingSQL = config[JsonKey.config.self][JsonKey.config.splicingSQL.self][JsonKey.config.splicingSQL.value]
            data += f'{tag}<if test="{splicingSQL}!=null">\n'
            data += f'{tag}\t${{{splicingSQL}}}\n'
            data += f'{tag}</if>\n'
        return data

    # 分页块
    @staticmethod
    def page(indent=2, page="page"):
        """
        获取SQL注入块
        :param indent: 缩进
        :param page:分页名称
        """
        tag = "\t" * indent
        data = ""
        data += f'{tag}<if test="{page}!=null">\n'
        data += f'{tag}\tlimit #{{{page}.start}} , #{{{page}.count}}\n'
        data += f'{tag}</if>\n'
        return data

    @staticmethod
    def where_mod_1(config: dict, indent: int, prefix=None, fuzzy_search=True, table_as_name=None):
        """
        <if test="prefix.attr!=null">AND filed = #{prefix.attr}</if>
        :param config: 配置文件
        :param indent: 缩进
        :param prefix: 前缀
        :param fuzzy_search: 模糊搜索
        :param table_as_name: 表别名
        """
        className = config["className"]
        key = config["key"]["attr"]
        keyFiled = config["key"]["filed"]
        tableName = config["tableName"]

        tap = "\t" * indent
        i, max_len, data = 0, len(config["attr"]), ""
        if prefix:
            start = f'{tap}<if test="{prefix}!=null">\n'
            prefix = f'{prefix}.'
            end = f"{tap}</if>\n"
            tap += '\t'
        else:
            prefix = start = end = ""

        table_as_name = util.if_return(table_as_name, f'{table_as_name}.', "")
        data += start

        data += f'{tap}<if test="{prefix}{key}!=null">AND {table_as_name}{keyFiled} = #{{{prefix}{key}}}</if>\n'
        for attr in config["attr"]:
            if "Date" == attr.get("type"):
                data += f'{tap}<if test="{prefix}{attr["attr"]}!=null">AND DATE({table_as_name}{attr["filed"]}) = DATE(#{{{prefix}{attr["attr"]}}})</if>\n'
            else:
                data += f'{tap}<if test="{prefix}{attr["attr"]}!=null">AND {table_as_name}{attr["filed"]} = #{{{prefix}{attr["attr"]}}}</if>\n'
        data += f'{end}'
        if fuzzy_search:
            data += CreateXmlBlock.fuzzy_search(config, indent, table_as_name)
        return data

    @staticmethod
    def where_mod_2(config: dict, indent: int, prefix=None, fuzzy_search=True, table_as_name=None):
        """
        忽略DATE的类型，适用于insert,update,delete
        <if test="prefix.attr!=null">AND filed = #{prefix.attr}</if>
        :param config: 配置文件
        :param indent: 缩进
        :param prefix: 前缀
        :param fuzzy_search: 模糊搜索
        :param table_as_name: 表别名
        """
        className = config["className"]
        key = config["key"]["attr"]
        keyFiled = config["key"]["filed"]
        tableName = config["tableName"]

        tap = "\t" * indent
        i, max_len, data = 0, len(config["attr"]), ""
        if prefix:
            start = f'{tap}<if test="{prefix}!=null">\n'
            prefix = f'{prefix}.'
            end = f"{tap}</if>\n"
            tap += '\t'
        else:
            prefix = start = end = ""

        table_as_name = util.if_return(table_as_name, f'{table_as_name}.', "")
        data += start

        data += f'{tap}<if test="{prefix}{key}!=null">AND {table_as_name}{keyFiled} = #{{{prefix}{key}}}</if>\n'
        for attr in config["attr"]:
                data += f'{tap}<if test="{prefix}{attr["attr"]}!=null">AND {table_as_name}{attr["filed"]} = #{{{prefix}{attr["attr"]}}}</if>\n'
        data += f'{end}'
        if fuzzy_search:
            data += CreateXmlBlock.fuzzy_search(config, indent, table_as_name)
        return data



    @staticmethod
    def compulsory_fuzzy_search(lists: list, keyword, indent: int, table_name="", ):
        """
        强制生成模糊搜索块
        :param lists: 搜索字段
        :param keyword:关键字名称
        :param table_name:表名称
        :param indent: 缩进
        """
        if lists is None or len(lists) == 0:
            return ""
        tag = "\t"
        code = ""
        i = 0
        if table_name != "":
            table_name += "."
        block_str = f'{tag * indent}<if test="{keyword}!=null">\n'
        for filed in lists:
            if i == 0:
                code = f'{table_name}{filed} LIKE #{{{keyword}}}'
                i = 1
            else:
                code += f' OR {table_name}{filed} LIKE #{{{keyword}}}'
        block_str += f'{tag * (indent + 1)}AND ({code})\n'
        block_str += f'{tag * indent}</if>\n'
        return block_str
