class Constant:
    STRING = "String"
    INTEGER = "Integer"
    LONG = "Long"
    DATE = "Date"
    FLOAT = "Float"
    DOUBLE = "Double"
    BOOLEAN = "Boolean"
    CHARACTER = "Character"
    DECIMAL = "BigDecimal"


class PackObjectDict:
    DATA = {
        "int": Constant.INTEGER,
        "long": Constant.LONG,
        "char": Constant.CHARACTER,
        "time": Constant.DATE,
        "float": Constant.FLOAT,
        "double": Constant.DOUBLE,
        "boolean": Constant.BOOLEAN,
    }


class MySQLObjectDict:
    DATA = {
        # 整数类
        "tinyint": Constant.INTEGER,
        "smallint": Constant.INTEGER,
        "mediumint": Constant.INTEGER,
        "int": Constant.INTEGER,
        "integer": Constant.INTEGER,
        "long": Constant.LONG,
        "bigint": Constant.LONG,
        # 小数类
        "float": Constant.FLOAT,
        "double": Constant.DOUBLE,
        "decimal": Constant.DECIMAL,
        # 时间类
        "time": Constant.DATE,
        "date": Constant.DATE,
        "datetime": Constant.DATE,
        "year": Constant.DATE,
        "timestamp": Constant.DATE,
        # 字符串类
        "char": Constant.STRING,
        "varchar": Constant.STRING,
        "tinyblob": Constant.STRING,
        "tinytext": Constant.STRING,
        "blob": Constant.STRING,
        "text": Constant.STRING,
        "mediumblob": Constant.STRING,
        "mediumtext": Constant.STRING,
        "longblob": Constant.STRING,
        "longtext": Constant.STRING,

    }


def get_java_pack_object(type_str: str) -> str:
    """
    获取Java基础数据类型的包装类
    :param type_str:基础类型包装类
    :return: 类型的字符串
    """
    temp_str = type_str.lower()
    if temp_str in PackObjectDict.DATA:
        return PackObjectDict.DATA.get(temp_str)
    return Constant.STRING


def mysql_to_java_object(type_str: str) -> str:
    """
    mysql数据类型转成java包装类
    :param type_str:基础类型的字符串
    :return: 类型的字符串
    """
    temp_str = type_str.lower()
    if temp_str in MySQLObjectDict.DATA:
        return MySQLObjectDict.DATA.get(temp_str)
    return Constant.STRING
