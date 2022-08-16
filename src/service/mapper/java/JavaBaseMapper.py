from src.constant.ProtocolConstant import JsonKey
from src.util import StringUtil
from src.util.StringUtil import create_annotation, create_java_function, create_java_interface


class CreateFile:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config):
        importSet = set()
        methodData = CreateMethod.create(config, importSet)

        data = f'package {config["module"]["baseMapperInterface"]["path"]};\n'
        data += "\n"
        # 生成导包文件
        data += CreateImportData.create(config, importSet)
        data += "\n"
        # 文件本体内容
        data += f'@Mapper\n'
        data += f'public interface {config["module"]["baseMapperInterface"]["className"]} {{\n\n'
        # 文件接口内容
        data += methodData
        data += "}"
        return data


class Page:
    """
    分页信息
    """

    @staticmethod
    def param(index=""):
        """
        方法参数
        :param index:下标
        :return: None|方法参数字符串
        """
        return f'@Param("page{index}") Page page{index}'

    @staticmethod
    def annotation(index="", msg=""):
        """
        注解
        :param index:下标
        :param msg:消息
        :return: None|方法参数字符串
        """
        return f'page{index} {msg}分页对象'


class ThisObject:
    """
    指代本类的信息
    """

    @staticmethod
    def param(config, param=True):
        """
        方法参数
        :param config: 配置
        :param param: 需要@param
        :return: None|方法参数字符串
        """
        lowClassName = StringUtil.first_char_lower_case(config["className"])
        className = config["className"]
        if param:
            return f'@Param("{lowClassName}") {className} {lowClassName}'
        return f'{className} {lowClassName}'

    @staticmethod
    def annotation(config):
        """
        注解
        :param config:
        :return: None|方法参数字符串
        """
        lowClassName = StringUtil.first_char_lower_case(config["className"])
        return f'{lowClassName} {config["remark"]}对象'


class SaveObject:
    """
    指代本类的信息
    """

    @staticmethod
    def param(config, param=True):
        """
        方法参数
        :param config: 配置
        :param param: 需要@param
        :return: None|方法参数字符串
        """
        className = config["className"]
        if param:
            return f'@Param("save{className}") {className} save{className}'
        return f'{className} save{className}'

    @staticmethod
    def annotation(config):
        """
        注解
        :param config:
        :return: None|方法参数字符串
        """
        return f'save{config["className"]} 添加的{config["remark"]}对象'


class ConditionObject:
    """
    指代本类的信息
    """

    @staticmethod
    def param(config, param=True):
        """
        方法参数
        :param config: 配置
        :param param: 需要@param
        :return: None|方法参数字符串
        """
        className = config["className"]
        if param:
            return f'@Param("condition{className}") {className} condition{className}'
        return f'{className} condition{className}'

    @staticmethod
    def annotation(config):
        """
        注解
        :param config:
        :return: None|方法参数字符串
        """
        return f'condition{config["className"]} {config["remark"]}条件对象'


class FuzzySearch:
    """
    模糊搜索处理类
    """

    @staticmethod
    def param(config, index=""):
        """
        获取模糊搜索的方法参数
        :param config: 配置
        :param index: 下标索引
        :return: None|方法参数字符串
        """
        if config["config"]["fuzzySearch"]["enable"]:
            keyWord = config["config"]["fuzzySearch"]["value"]
            if len(config["config"]["fuzzySearch"]["data"]) != 0:
                return f'@Param("{keyWord}{index}") String {keyWord}{index}'
        return None

    @staticmethod
    def annotation(config, index="", msg=""):
        """
        获取模糊搜索的注解
        :param config:配置
        :param index: 下标索引
        :param msg: 描述
        :return: None|方法参数字符串
        """
        if config["config"]["fuzzySearch"]["enable"]:
            keyWord = config["config"]["fuzzySearch"]["value"]
            if len(config["config"]["fuzzySearch"]["data"]) != 0:
                return f'{keyWord}{index} {msg}模糊搜索内容'
        return None


class SplicingSQL:
    """
    sql语句注入项
    """

    @staticmethod
    def param(config):
        """
        SQL语句拼接项参数
        :param config:配置
        :return: None|方法参数
        """
        if config["config"]["splicingSQL"]["enable"]:
            value = config["config"]["splicingSQL"]["value"]
            return f'@Param("{value}") String {value}'
        return None

    @staticmethod
    def annotation(config):
        """
        SQL语句拼接项注解
        :param config:配置
        :return: None|注解参数
        """
        if config["config"]["splicingSQL"]["enable"]:
            value = config["config"]["splicingSQL"]["value"]
            return f'{value} 拼接的sql语句'
        return None


# 创建导包
class CreateImportData:
    """
    创建导包文件
    """

    @staticmethod
    def create(config, importSet: set):
        data = "import java.util.List;\n"
        data += f'import {config["module"]["Page"]["package"]};\n'
        data += f'import org.apache.ibatis.annotations.Mapper;\n'
        data += f'import org.apache.ibatis.annotations.Param;\n'
        if config["path"] != config["module"]["serviceInterface"]["path"]:
            importSet.add(config["package"])
        for i in importSet:
            data += f'import {i};\n'
        return data


# 创建插入
class CreateMethodInsert:
    """
    创建插入的方法
    """

    @staticmethod
    def create(config):
        lowClassName = StringUtil.first_char_lower_case(config["className"])
        className = config["className"]
        remark = config["remark"]
        method_str = ""
        # 添加
        method_str += create_annotation(f'添加{remark}', "受影响行数", ThisObject.annotation(config))
        method_str += create_java_interface("Integer", f'insert{className}', ThisObject.param(config, False))
        # 添加多个
        method_str += create_annotation(f'添加多个{remark}', "受影响行数", f'list {remark}列表')
        method_str += create_java_interface("Integer", f'insert{className}List', f'@Param("list") List<{className}> list')
        # 保存或更新，唯一索引方式
        method_str += create_annotation(f'添加或更新{remark}，根据唯一性索引', "受影响行数", ThisObject.param(config, False))
        method_str += create_java_interface("Integer", f'insertOrUpdate{className}ByUnique', ThisObject.param(config, False))
        # 保存或更新条件式
        method_str += create_annotation(f'添加或更新{remark}，根据查询条件', "受影响行数", SaveObject.annotation(config), ConditionObject.annotation(config))
        method_str += create_java_interface("Integer", f'insertOrUpdate{className}ByWhere', SaveObject.param(config), ConditionObject.param(config))
        # 仅条件插入
        method_str += create_annotation(f'条件添加{remark}，查询条件存在的情况下', "受影响行数", SaveObject.annotation(config), ConditionObject.annotation(config))
        method_str += create_java_interface("Integer", f'insert{className}ByExistWhere', SaveObject.param(config), ConditionObject.param(config))
        # 仅条件插入
        method_str += create_annotation(f'条件添加{remark}，查询条件不存在的情况下', "受影响行数", SaveObject.annotation(config), ConditionObject.annotation(config))
        method_str += create_java_interface("Integer", f'insert{className}ByNotExistWhere', SaveObject.param(config), ConditionObject.param(config))
        return method_str


# 创建删除
class CreateMethodDelete:
    """
    创建删除的方法
    """

    @staticmethod
    def create(config):
        lowClassName = StringUtil.first_char_lower_case(config["className"])
        className = config["className"]
        remark = config["remark"]
        upperKey = StringUtil.first_char_upper_case(config["key"]["attr"])
        key = config["key"]["attr"]
        keyType = config["key"]["type"]

        method_str = ""
        # 主键删除
        method_str += create_annotation(f'根据{key}真删{remark}', "受影响行数", f'{key} {remark}的{key}')
        method_str += create_java_interface("Integer", f'delete{className}By{upperKey}', f'{keyType} {key}')

        # 多个主键删除
        method_str += create_annotation(f'根据{key}列表真删{remark}', "受影响行数", f'list {remark}的{key}列表')
        method_str += create_java_interface("Integer", f'delete{className}In{upperKey}', f'List<{keyType}> list')

        # 主键条件删
        method_str += create_annotation(f'根据{key}和其他条件真删{remark}', "受影响行数", f'{key} {remark}的{key}', f'{lowClassName} {remark}条件对象', FuzzySearch.annotation(config))
        method_str += create_java_interface("Integer", f'delete{className}By{upperKey}AndWhere', f'@Param("{key}") {keyType} {key}', ThisObject.param(config), FuzzySearch.param(config))
        # 条件删除
        method_str += create_annotation(f'根据条件真删{remark}', "受影响行数", f'{lowClassName} {remark}条件对象', FuzzySearch.annotation(config))
        method_str += create_java_interface("Integer", f'delete{className}', ThisObject.param(config), FuzzySearch.param(config))

        # 主键假删
        if config["config"]["falseDelete"]["enable"]:
            method_str += create_annotation(f'根据{key}假删{remark}', "受影响行数", f'{key} {remark}的{key}')
            method_str += create_java_interface("Integer", f'falseDelete{className}By{upperKey}', f'{keyType} {key}')

        return method_str


# 创建更新
class CreateMethodUpdate:
    """
    创建更新方法
    """

    @staticmethod
    def create(config):
        lowClassName = StringUtil.first_char_lower_case(config["className"])
        className = config["className"]
        remark = config["remark"]
        upperKey = StringUtil.first_char_upper_case(config["key"]["attr"])
        key = config["key"]["attr"]
        keyType = config["key"]["type"]
        method_str = ""
        # 根据主键更新
        method_str += create_annotation(f'根据{key}修改{remark}', "受影响行数", f'{lowClassName} 要更新的{remark}对象')
        method_str += create_java_interface("Integer", f'update{className}By{upperKey}', ThisObject.param(config, False))
        # 不重复条件改
        method_str += create_annotation(f'根据{key}和不满足的条件更新{remark}，查询条件不满足时更新对象', "受影响行数",
                                        f'save{className} 更新的{remark}对象', f'condition{className} 不存在的{remark}对象')
        method_str += create_java_interface("Integer", f'update{className}ByNotRepeatWhere', SaveObject.param(config), ConditionObject.param(config))

        # 条件更新ID
        method_str += create_annotation(f'根据{key}和其他的条件更新{remark}', "受影响行数", f'save{className} 更新的{remark}对象', f'condition{className} {remark}条件对象')
        method_str += create_java_interface("Integer", f'update{className}By{upperKey}AndWhere', SaveObject.param(config), ConditionObject.param(config))

        # 条件改
        method_str += create_annotation(f'根据条件更新{remark}', "受影响行数", f'save{className} 更新的{remark}对象', f'condition{className} 条件{remark}对象')
        method_str += create_java_interface("Integer", f'update{className}', SaveObject.param(config), ConditionObject.param(config))

        # 设置空字段
        method_str += create_annotation(f'记录{key}设置其他字段为null', "受影响行数", f'{lowClassName} 设置成null的{remark}对象，对象中字段不为Null则是要设置成null的字段')
        method_str += create_java_interface("Integer", f'update{className}SetNullBy{upperKey}', ThisObject.param(config, False))
        return method_str


# 创建查询
class CreateMethodSelect:
    """
    创建单表查询语句
    """

    @staticmethod
    def create(config):
        lowClassName = StringUtil.first_char_lower_case(config["className"])
        className = config["className"]
        remark = config["remark"]
        upperKey = StringUtil.first_char_upper_case(config["key"]["attr"])
        key = config["key"]["attr"]
        keyType = config["key"]["type"]
        method_str = ""

        # 主键查
        method_str += create_annotation(f'根据{key}查询{remark}', f"{remark}对象", f'{key} {remark}的{key}')
        method_str += create_java_interface(className, f'select{className}By{upperKey}', f'{keyType} {key}')
        # 多主键查
        method_str += create_annotation(f'根据{key}列表查询{remark}', f"{remark}对象列表", f'list {remark}的{key}列表')
        method_str += create_java_interface(f'List<{className}>', f'select{className}In{upperKey}', f'List<{keyType}> list')
        # 多主键查，且携带条件
        method_str += create_annotation(f'根据{key}列表和其他条件查询{remark}', f"{remark}对象列表", f'list {remark}的{key}列表', ThisObject.annotation(config), FuzzySearch.annotation(config))
        method_str += create_java_interface(
            f'List<{className}>', f'select{className}In{upperKey}AndWhere',
            f'@Param("list") List<{keyType}> list',
            ThisObject.param(config),
            FuzzySearch.param(config)
        )

        # 多字段单查
        method_str += create_annotation(f'只查询一个{remark}', f"{remark}对象", ThisObject.annotation(config), f'index 获取的下标值', FuzzySearch.annotation(config))
        method_str += create_java_interface(
            className, f'selectOne{className}',
            ThisObject.param(config),
            f'@Param("index")Integer index',
            FuzzySearch.param(config)
        )

        # 普通查
        method_str += create_annotation(
            f'查询多个{remark}', f"{remark}对象列表",
            ThisObject.annotation(config), Page.annotation(), FuzzySearch.annotation(config), SplicingSQL.annotation(config))
        method_str += create_java_interface(
            f'List<{className}>', f'select{className}',
            ThisObject.param(config), Page.param(), FuzzySearch.param(config), SplicingSQL.param(config),
        )

        # 普通计数
        method_str += create_annotation(f'统计{remark}记录数', f"查询到的记录数", ThisObject.param(config), FuzzySearch.param(config))
        method_str += create_java_interface("Integer", f'count{className}', ThisObject.param(config), FuzzySearch.param(config))
        return method_str


# 创建一对一查询
class CreateMethodSelectOneToOne:
    """
    创建一对一查询语句
    """

    @staticmethod
    def create(config, importSet: set):
        lowClassName = StringUtil.first_char_lower_case(config["className"])
        className = config["className"]
        remark = config["remark"]
        method_str = ""
        if config.get(JsonKey.oneToOne) is None or len(config.get(JsonKey.oneToOne)) == 0:
            return ""

        for obj in config["oneToOne"]:
            objClassName = obj["className"]
            objLowClassName = StringUtil.first_char_lower_case(objClassName)
            objRemark = obj["remark"]
            importSet.add(f'{obj[JsonKey.package]}')
            # 一对一内联查询
            method_str += create_annotation(f'内联一对一查询{objRemark}',
                                            f"{remark}对象列表",
                                            ThisObject.annotation(config),
                                            ThisObject.annotation(obj),
                                            Page.annotation(),
                                            FuzzySearch.annotation(config),
                                            FuzzySearch.annotation(obj, "1", objRemark),
                                            SplicingSQL.annotation(config)
                                            )
            method_str += create_java_interface(
                f"List<{className}>", f'find{className}OneToOne{objClassName}',
                ThisObject.param(config),
                ThisObject.param(obj),
                Page.param(),
                FuzzySearch.param(config),
                FuzzySearch.param(obj, "1"),
                SplicingSQL.param(config)
            )
            # 一对一内联计数
            method_str += create_annotation(f'内联一对一统计{objRemark}', f"查询到的记录数",
                                            ThisObject.annotation(config),
                                            ThisObject.annotation(obj),
                                            FuzzySearch.annotation(config),
                                            FuzzySearch.annotation(obj, "1", objRemark),
                                            )
            method_str += create_java_interface(
                f"Integer", f'countFind{className}OneToOne{objClassName}',
                ThisObject.param(config),
                ThisObject.param(obj),
                FuzzySearch.param(config),
                FuzzySearch.param(obj, "1"),
            )
            # 一对一获取对方
            method_str += create_annotation(f'内联一对一查询{objRemark}，只返回{objRemark}',
                                            f"{objRemark}对象列表",
                                            ThisObject.annotation(config),
                                            ThisObject.annotation(obj),
                                            Page.annotation(),
                                            FuzzySearch.annotation(config),
                                            FuzzySearch.annotation(obj, "1", objRemark),
                                            SplicingSQL.annotation(config)
                                            )
            method_str += create_java_interface(
                f"List<{objClassName}>", f'linkOneToOne{objClassName}',
                ThisObject.param(config),
                ThisObject.param(obj),
                Page.param(),
                FuzzySearch.param(config),
                FuzzySearch.param(obj, "1"),
                SplicingSQL.param(config)
            )

            # 一对一外联
            method_str += create_annotation(f'外联一对一查询{objRemark}，只返回{objRemark}',
                                            f"{remark}对象列表",
                                            ThisObject.annotation(config),
                                            ThisObject.annotation(obj),
                                            Page.annotation("", remark),
                                            Page.annotation("1", objRemark),
                                            FuzzySearch.annotation(config),
                                            FuzzySearch.annotation(obj, "1", objRemark),
                                            SplicingSQL.annotation(config)
                                            )
            method_str += create_java_interface(
                f"List<{className}>", f'query{className}OneToOne{objClassName}',
                ThisObject.param(config),
                ThisObject.param(obj),
                Page.param(),
                Page.param("1"),
                FuzzySearch.param(config),
                FuzzySearch.param(obj, "1"),
                SplicingSQL.param(config)
            )

            # 一对一外联计数
            method_str += create_annotation(f'外联一对一统计{objRemark}',
                                            f"查询到的记录数",
                                            ThisObject.annotation(config),
                                            ThisObject.annotation(obj),
                                            Page.annotation("", remark),
                                            Page.annotation("1", objRemark),
                                            FuzzySearch.annotation(config),
                                            FuzzySearch.annotation(obj, "1", objRemark),
                                            )
            method_str += create_java_interface(
                f"Integer", f'countQuery{className}OneToOne{objClassName}',
                ThisObject.param(config),
                ThisObject.param(obj),
                Page.param(),
                Page.param("1"),
                FuzzySearch.param(config),
                FuzzySearch.param(obj, "1"),
            )

        return method_str


# 创建一对多查询
class CreateMethodSelectOneToMany:
    """
    创建一对多查询语句
    """

    @staticmethod
    def create(config, importSet: set):
        lowClassName = StringUtil.first_char_lower_case(config["className"])
        className = config["className"]
        remark = config["remark"]
        method_str = ""
        if config.get(JsonKey.oneToMany) is None or len(config.get(JsonKey.oneToMany)) == 0:
            return ""

        for obj in config["oneToMany"]:
            objClassName = obj["className"]
            objLowClassName = StringUtil.first_char_lower_case(objClassName)
            objRemark = obj["remark"]
            importSet.add(f'{obj[JsonKey.package]}')

            # 一对多内联查询
            method_str += create_annotation(f'内联一对多查询{objRemark}，双方均可分页',
                                            f"{remark}对象列表",
                                            ThisObject.annotation(config),
                                            ThisObject.annotation(obj),
                                            f'onePage {remark}分页对象',
                                            f'manyPage {objRemark}分页对象',
                                            FuzzySearch.annotation(config),
                                            FuzzySearch.annotation(obj, "1", objRemark),
                                            SplicingSQL.annotation(config)
                                            )
            method_str += create_java_interface(
                f"List<{className}>", f'find{className}OneToMany{objClassName}',
                ThisObject.param(config),
                ThisObject.param(obj),
                f'@Param("onePage") Page onePage',
                f'@Param("manyPage") Page manyPage',
                FuzzySearch.param(config),
                FuzzySearch.param(obj, "1"),
                SplicingSQL.param(config)
            )

            # 一对多内联统计
            method_str += create_annotation(f'内联一对多统计{objRemark}，双方均可分页',
                                            f"查询到的记录数",
                                            ThisObject.annotation(config),
                                            ThisObject.annotation(obj),
                                            f'onePage {remark}分页对象',
                                            f'manyPage {objRemark}分页对象',
                                            FuzzySearch.annotation(config),
                                            FuzzySearch.annotation(obj, "1", objRemark),
                                            )
            method_str += create_java_interface(
                f"Integer", f'countFind{className}OneToMany{objClassName}',
                ThisObject.param(config),
                ThisObject.param(obj),
                f'@Param("onePage") Page onePage',
                f'@Param("manyPage") Page manyPage',
                FuzzySearch.param(config),
                FuzzySearch.param(obj, "1"),
            )
            # 一对多反获取对方
            method_str += create_annotation(f'内联一对多查询{objRemark}，只返回{objRemark}',
                                            f"{objRemark}对象列表",
                                            ThisObject.annotation(config),
                                            ThisObject.annotation(obj),
                                            f'onePage {remark}分页对象',
                                            f'manyPage {objRemark}分页对象',
                                            FuzzySearch.annotation(config),
                                            FuzzySearch.annotation(obj, "1", objRemark),
                                            SplicingSQL.annotation(config)
                                            )
            method_str += create_java_interface(
                f"List<{objClassName}>", f'linkOneToMany{objClassName}',
                ThisObject.param(config),
                ThisObject.param(obj),
                f'@Param("onePage") Page onePage',
                f'@Param("manyPage") Page manyPage',
                FuzzySearch.param(config),
                FuzzySearch.param(obj, "1"),
                SplicingSQL.param(config)
            )
            # 一对多外联
            method_str += create_annotation(f'外联一对多查询{objRemark}，双方均可分页',
                                            f"{remark}对象列表",
                                            ThisObject.annotation(config),
                                            ThisObject.annotation(obj),
                                            f'onePage {remark}分页对象',
                                            f'manyPage {objRemark}分页对象',
                                            FuzzySearch.annotation(config),
                                            FuzzySearch.annotation(obj, "1", objRemark),
                                            SplicingSQL.annotation(config)
                                            )
            method_str += create_java_interface(
                f"List<{className}>", f'query{className}OneToMany{objClassName}',
                ThisObject.param(config),
                ThisObject.param(obj),
                f'@Param("onePage") Page onePage',
                f'@Param("manyPage") Page manyPage',
                FuzzySearch.param(config),
                FuzzySearch.param(obj, "1"),
                SplicingSQL.param(config)
            )
            # 一对多外联统计
            method_str += create_annotation(f'外联一对多查询{objRemark}统计，双方均可分页',
                                            f"查询到的记录数",
                                            ThisObject.annotation(config),
                                            ThisObject.annotation(obj),
                                            f'onePage {remark}分页对象',
                                            f'manyPage {objRemark}分页对象',
                                            FuzzySearch.annotation(config),
                                            FuzzySearch.annotation(obj, "1", objRemark),
                                            )
            method_str += create_java_interface(
                f"Integer", f'countQuery{className}OneToMany{objClassName}',
                ThisObject.param(config),
                ThisObject.param(obj),
                f'@Param("onePage") Page onePage',
                f'@Param("manyPage") Page manyPage',
                FuzzySearch.param(config),
                FuzzySearch.param(obj, "1"),
            )

        return method_str


# 创建多对多查询
class CreateMethodSelectManyToMany:
    """
    创建多对多查询语句
    """

    @staticmethod
    def create(config):
        lowClassName = StringUtil.first_char_lower_case(config["className"])
        className = config["className"]
        remark = config["remark"]
        method_str = ""
        if config.get(JsonKey.manyToMany) is None or len(config.get(JsonKey.manyToMany)) == 0:
            return ""
        for obj in config["manyToMany"]:
            toClassName = obj["to"]["className"]
            toLowClassName = StringUtil.first_char_lower_case(toClassName)
            toRemark = obj["to"]["remark"]
            manyClassName = obj["many"]["className"]
            manyLowClassName = StringUtil.first_char_lower_case(manyClassName)
            manyRemark = obj["many"]["remark"]
            # 多对多内联
            method_str += create_annotation(f'内联多对多查询{remark},根据{toRemark}联查{manyRemark}',
                                            f"{className}对象列表",
                                            ThisObject.annotation(config),
                                            Page.annotation(),
                                            FuzzySearch.annotation(config),
                                            SplicingSQL.annotation(config),
                                            )
            method_str += create_java_interface(
                f'List<{className}>', f'find{className}ManyToManyLink{toClassName}On{manyClassName}',
                ThisObject.param(config),
                Page.param(),
                FuzzySearch.param(config),
                SplicingSQL.param(config),
            )
            # 多对多外联
            method_str += create_annotation(f'内联多对多查询{remark},根据{toRemark}联查{manyRemark}',
                                            f"{className}对象列表",
                                            ThisObject.annotation(config),
                                            Page.annotation(),
                                            FuzzySearch.annotation(config),
                                            SplicingSQL.annotation(config),
                                            )
            method_str += create_java_interface(
                f'List<{className}>', f'query{className}ManyToManyLink{toClassName}On{manyClassName}',
                ThisObject.param(config),
                Page.param(),
                FuzzySearch.param(config),
                SplicingSQL.param(config),
            )
        return method_str


# 创建外键查询
class CreateMethodSelectForeignKey:

    @staticmethod
    def create(config):
        lowClassName = StringUtil.first_char_lower_case(config["className"])
        className = config["className"]
        remark = config["remark"]
        method_str = ""
        if config.get(JsonKey.oneToOne) is None or len(config.get(JsonKey.oneToOne)) == 0:
            return ""

        for obj in config["oneToOne"]:
            # 多外键键查，且携带条件
            attr = None
            for i in config[JsonKey.attr.self]:
                if i[JsonKey.attr.filed] == obj[JsonKey.foreignKey]:
                    attr = i
                    break
            if attr is None:
                continue
            method_str += create_annotation(
                f'根据{attr[JsonKey.attr.remark]}列表和其他条件查询{remark}',
                f"{remark}对象列表",
                f'list {remark}的{attr[JsonKey.attr.remark]}列表',
                ThisObject.annotation(config),
                FuzzySearch.param(config)
            )
            method_str += create_java_interface(
                f'List<{className}>', f'select{className}In{StringUtil.first_char_upper_case(attr[JsonKey.attr.attr])}AndWhere',
                f'@Param("list") List<{attr[JsonKey.attr.type]}> list',
                ThisObject.param(config),
                FuzzySearch.param(config)
            )
        return method_str


# 创建方法
class CreateMethod:
    """
    创建接口方法
    """

    @staticmethod
    def create(config: dict, importSet: set):
        data = ""
        # 增
        data += CreateMethodInsert.create(config)
        # 删
        data += CreateMethodDelete.create(config)
        # 改
        data += CreateMethodUpdate.create(config)
        # 查
        data += CreateMethodSelect.create(config)
        # 一对一
        data += CreateMethodSelectOneToOne.create(config, importSet)
        # 一对多
        data += CreateMethodSelectOneToMany.create(config, importSet)
        # 多对多
        data += CreateMethodSelectManyToMany.create(config)
        # 外键查
        data += CreateMethodSelectForeignKey.create(config)
        return data
