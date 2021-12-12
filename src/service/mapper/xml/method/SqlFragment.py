class CreateSqlFragment:
    """
    创建resultMap块
    """

    # 创建sql片段
    @staticmethod
    def create(config: dict, tables, tableDuplication: bool):
        """
        创建sql片段
        :param config:配置文件
        :param tables: 新结构配置文件
        :param tableDuplication: 自己的表重复
        :return: 组装后的sql片段
        """
        string_block = ""
        tag = "\t"
        # 装配 sql片段，针对普通的情况
        for table in tables:
            data = ""
            for attr in tables[table]["attr"]:
                if "fieldAlias" in attr:
                    data += f'{table}.{attr["filed"]} AS {attr["fieldAlias"]},'
                    # 这TM啥？
                    if tables[table].get("foreignKey") == attr["filed"]:
                        tables[table]["foreignKeyAlias"] = attr["fieldAlias"]
                else:
                    data += f'{table}.{attr["filed"]},'

            data = data.strip(",")
            data = f'<sql id="sql_filed_{table}">{data}</sql>'
            string_block += f'{tag}{data}\n'

        # 针对自我重复的表，将其起名均为结尾加1的形式
        if tableDuplication:
            data = f'{config["tableName"]}1.{config["key"]["filed"]} AS {config["key"]["filed"]}1,'
            for attr in config["attr"]:
                data += f'{config["tableName"]}1.{attr["filed"]} AS {attr["filed"]}1,'
            data = data.strip(",")
            data = f'<sql id="sql_filed_{config["tableName"]}1">{data}</sql>'
            string_block += f'{tag}{data}\n'
        string_block += "\n"
        return string_block
