from src.constant.ProtocolConstant import JsonKey
from src.util import StringUtil
from src.util.StringUtil import create_annotation


class CreateFile:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config):
        importSet = set()
        methodData = CreateMethod.create(config, importSet)

        data = f'package {config["baseMapperInterface"]["path"]};\n'
        data += "\n"
        # 生成导包文件
        data += CreateImportData.create(config, importSet)
        data += "\n"
        # 文件本体内容
        data += f'@Mapper\n'
        data += f'public interface {config["baseMapperInterface"]["className"]} {{\n\n'
        # 文件接口内容
        data += methodData
        data += "}"
        return data


# 创建导包
class CreateImportData:
    """
    创建导包文件
    """

    @staticmethod
    def create(config, importSet: set):
        data = "import java.util.List;\n"
        data += f'import {config["Page"]["package"]};\n'
        data += f'import org.apache.ibatis.annotations.Mapper;\n'
        data += f'import org.apache.ibatis.annotations.Param;\n'
        if config["path"] != config["serviceInterface"]["path"]:
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
        method_str += create_annotation(f'添加{remark}', "受影响行数", f'{lowClassName} {remark}')
        method_str += f'\tInteger insert{className}({className} {lowClassName});\n\n'
        # 添加多个
        method_str += create_annotation(f'添加多个{remark}', "受影响行数", f'list {remark}列表')
        method_str += f'\tInteger insert{className}List(@Param("list") List<{className}> list);\n\n'
        # 保存或更新，唯一索引方式
        method_str += create_annotation(f'添加或更新{remark}，根据唯一性索引', "受影响行数", f'list {remark}列表')
        method_str += f'\tInteger insertOrUpdate{className}ByUnique({className} {lowClassName});\n\n'
        # 保存或更新条件式
        method_str += create_annotation(f'添加或更新{remark}，根据查询条件', "受影响行数", f'save{className} 添加的{remark}对象',
                                        f'condition{className} {remark}条件对象')
        method_str += f'\tInteger insertOrUpdate{className}ByWhere(' \
                      f'@Param("save{className}") {className} save{className}, ' \
                      f'@Param("condition{className}") {className} condition{className}' \
                      f');\n\n'
        # 仅条件插入
        method_str += create_annotation(f'条件添加{remark}，查询条件存在的情况下', "受影响行数", f'save{className} 添加的{remark}对象',
                                        f'condition{className} {remark}条件对象')
        method_str += f'\tInteger insert{className}ByExistWhere(' \
                      f'@Param("save{className}") {className} save{className}, ' \
                      f'@Param("condition{className}") {className} condition{className}' \
                      f');\n\n'
        # 仅条件插入
        method_str += create_annotation(f'条件添加{remark}，查询条件不存在的情况下', "受影响行数", f'save{className} 添加的{remark}对象',
                                        f'condition{className} {remark}条件对象')
        method_str += f'\tInteger insert{className}ByNotExistWhere(' \
                      f'@Param("save{className}") {className} save{className}, ' \
                      f'@Param("condition{className}") {className} condition{className}' \
                      f');\n\n'
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
        method_str += f'\tInteger delete{className}By{upperKey}({keyType} {key});\n\n'

        # 多个主键删除
        method_str += create_annotation(f'根据{key}列表真删{remark}', "受影响行数", f'list {remark}的{key}列表')
        method_str += f'\tInteger delete{className}In{upperKey}(List<{keyType}> list);\n\n'

        # 主键条件删
        method_str += create_annotation(f'根据{key}和其他条件真删{remark}', "受影响行数", f'{key} {remark}的{key}',
                                        f'{lowClassName} {remark}条件对象')
        method_str += f'\tInteger delete{className}By{upperKey}AndWhere(' \
                      f'@Param("{key}") {keyType} {key}, ' \
                      f'@Param("{lowClassName}") {className} {lowClassName}' \
                      f');\n\n'
        # 条件删除
        method_str += create_annotation(f'根据条件真删{remark}', "受影响行数", f'{lowClassName} {remark}条件对象')
        method_str += f'\tInteger delete{className}({className} {lowClassName});\n\n'

        # 主键假删
        if config["config"]["falseDelete"]["enable"]:
            method_str += create_annotation(f'根据{key}假删{remark}', "受影响行数", f'{key} {remark}的{key}')
            method_str += f'\tInteger falseDelete{className}By{upperKey}({keyType} {key});\n\n'

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
        method_str += f'\tInteger update{className}By{upperKey}({className} {lowClassName});\n\n'
        # 不重复条件改
        method_str += create_annotation(f'根据{key}和不满足的条件更新{remark}，查询条件不满足时更新对象', "受影响行数",
                                        f'save{className} 更新的{remark}对象', f'condition{className} 不存在的{remark}对象')
        method_str += f'\tInteger update{className}ByNotRepeatWhere(' \
                      f'@Param("save{className}") {className} save{className}, ' \
                      f'@Param("condition{className}") {className} condition{className}' \
                      f');\n\n'
        # 条件更新ID
        method_str += create_annotation(f'根据{key}和其他的条件更新{remark}', "受影响行数", f'save{className} 更新的{remark}对象',
                                        f'condition{className} {remark}条件对象')
        method_str += f'\tInteger update{className}By{upperKey}AndWhere(' \
                      f'@Param("save{className}") {className} save{className}, ' \
                      f'@Param("condition{className}") {className} condition{className}' \
                      f');\n\n'

        # 条件改
        method_str += create_annotation(f'根据条件更新{remark}', "受影响行数", f'save{className} 更新的{remark}对象',
                                        f'condition{className} 条件{remark}对象')
        method_str += f'\tInteger update{className}(' \
                      f'@Param("save{className}") {className} save{className}, ' \
                      f'@Param("condition{className}") {className} condition{className}' \
                      f');\n\n'
        # 设置空字段
        method_str += create_annotation(f'记录{key}设置其他字段为null', "受影响行数",
                                        f'{lowClassName} 设置成null的{remark}对象，对象中字段不为Null则是要设置成null的字段')
        method_str += f'\tInteger update{className}SetNullBy{upperKey}({className} {lowClassName});\n\n'
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
        method_str += f'\t{className} select{className}By{upperKey}({keyType} {key});\n\n'
        # 多主键查
        method_str += create_annotation(f'根据{key}列表查询{remark}', f"{remark}对象列表", f'list {remark}的{key}列表')
        method_str += f'\tList<{className}> select{className}In{upperKey}(List<{keyType}> list);\n\n'
        # 多主键查，且携带条件
        method_str += create_annotation(f'根据{key}列表和其他条件查询{remark}', f"{remark}对象列表", f'list {remark}的{key}列表', f'{lowClassName} {remark}对象')
        method_str += f'\tList<{className}> select{className}In{upperKey}AndWhere(' \
                      f'@Param("list") List<{keyType}> list, ' \
                      f'@Param("{lowClassName}") {className} {lowClassName});\n\n'
        # 多字段单查
        method_str += create_annotation(f'只查询一个{remark}', f"{remark}对象", f'{lowClassName} {remark}对象', f'index 获取的下标值')
        method_str += f'\t{className} selectOne{className}(' \
                      f'@Param("{lowClassName}") {className} {lowClassName}, ' \
                      f'@Param("index")Integer index' \
                      f');\n\n'
        # 普通查
        if config[JsonKey.config.self][JsonKey.config.splicingSQL.self][JsonKey.config.splicingSQL.enable]:
            splicingSQL = config[JsonKey.config.self][JsonKey.config.splicingSQL.self][JsonKey.config.splicingSQL.value]
            method_str += create_annotation(f'查询多个{remark}', f"{remark}对象列表", f'{lowClassName} {remark}对象',
                                            f'page 分页对象', f'{splicingSQL} 拼接的sql语句')
            method_str += f'\tList<{className}> select{className}(' \
                          f'@Param("{lowClassName}") {className} {lowClassName}, ' \
                          f'@Param("page") Page page, ' \
                          f'@Param("{splicingSQL}") String {splicingSQL}' \
                          f');\n\n'
        else:
            method_str += create_annotation(f'查询多个{remark}', f"{remark}对象列表", f'{lowClassName} {remark}对象',
                                            f'page 分页对象')
            method_str += f'\tList<{className}> select{className}(' \
                          f'@Param("{lowClassName}") {className} {lowClassName}, ' \
                          f'@Param("page") Page page' \
                          f');\n\n'
        # 普通计数
        method_str += create_annotation(f'统计{remark}记录数', f"查询到的记录数", f'{lowClassName} {remark}对象')
        method_str += f'\tInteger count{className}(@Param("{lowClassName}") {className} {lowClassName});\n\n'
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
        splicingSQL = None
        sqlP = ""
        if config[JsonKey.config.self][JsonKey.config.splicingSQL.self][JsonKey.config.splicingSQL.enable]:
            sqlValue = config[JsonKey.config.self][JsonKey.config.splicingSQL.self][JsonKey.config.splicingSQL.value]
            splicingSQL = f'{sqlValue} 拼接的SQL'
            sqlP = f', @Param("{sqlValue}") String {sqlValue}'

        for obj in config["oneToOne"]:
            objClassName = obj["className"]
            objLowClassName = StringUtil.first_char_lower_case(objClassName)
            objRemark = obj["remark"]
            importSet.add(f'{obj[JsonKey.package]}')
            # 一对一内联查询
            method_str += create_annotation(f'内联一对一查询{objRemark}',
                                            f"{remark}对象列表",
                                            f'{lowClassName} {remark}对象',
                                            f'{objLowClassName} {objRemark}对象',
                                            f'page 分页对象',
                                            splicingSQL,
                                            )
            method_str += f'\tList<{className}> find{className}OneToOne{objClassName}(' \
                          f'@Param("{lowClassName}") {className} {lowClassName}, ' \
                          f'@Param("{objLowClassName}") {objClassName} {objLowClassName}, ' \
                          f'@Param("page") Page page' \
                          f'{sqlP}' \
                          f');\n\n'
            # 一对一内联计数
            method_str += create_annotation(f'内联一对一统计{objRemark}',
                                            f"查询到的记录数",
                                            f'{lowClassName} {remark}对象',
                                            f'{objLowClassName} {objRemark}对象',
                                            )
            method_str += f'\tInteger countFind{className}OneToOne{objClassName}(' \
                          f'@Param("{lowClassName}") {className} {lowClassName}, ' \
                          f'@Param("{objLowClassName}") {objClassName} {objLowClassName}' \
                          f');\n\n'
            # 一对一获取对方
            method_str += create_annotation(f'内联一对一查询{objRemark}，只返回{objRemark}',
                                            f"{objRemark}对象列表",
                                            f'{lowClassName} {remark}对象',
                                            f'{objLowClassName} {objRemark}对象',
                                            f'page 分页对象',
                                            splicingSQL,
                                            )
            method_str += f'\tList<{objClassName}> linkOneToOne{objClassName}(' \
                          f'@Param("{lowClassName}") {className} {lowClassName}, ' \
                          f'@Param("{objLowClassName}") {objClassName} {objLowClassName}, ' \
                          f'@Param("page") Page page' \
                          f'{sqlP}' \
                          f');\n\n'
            # 一对一外联
            method_str += create_annotation(f'外联一对一查询{objRemark}，只返回{objRemark}',
                                            f"{remark}对象列表",
                                            f'{lowClassName} {remark}对象',
                                            f'{objLowClassName} {objRemark}对象',
                                            f'page {remark}的分页对象',
                                            f'page1 {objRemark}的分页对象',
                                            splicingSQL,
                                            )
            method_str += f'\tList<{className}> query{className}OneToOne{objClassName}(' \
                          f'@Param("{lowClassName}") {className} {lowClassName}, ' \
                          f'@Param("{objLowClassName}") {objClassName} {objLowClassName}, ' \
                          f'@Param("page") Page page, ' \
                          f'@Param("page1") Page page1' \
                          f'{sqlP}' \
                          f');\n\n'

            # 一对一外联计数
            method_str += create_annotation(f'外联一对一统计{objRemark}',
                                            f"查询到的记录数",
                                            f'{lowClassName} {remark}对象',
                                            f'{objLowClassName} {objRemark}对象',
                                            f'page {remark}的分页对象',
                                            f'page1 {objRemark}的分页对象',
                                            )
            method_str += f'\tInteger countQuery{className}OneToOne{objClassName}(' \
                          f'@Param("{lowClassName}") {className} {lowClassName}, ' \
                          f'@Param("{objLowClassName}") {objClassName} {objLowClassName}, ' \
                          f'@Param("page") Page page, ' \
                          f'@Param("page1") Page page1' \
                          f');\n\n'

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
        splicingSQL = None
        sqlP = ""
        if config[JsonKey.config.self][JsonKey.config.splicingSQL.self][JsonKey.config.splicingSQL.enable]:
            sqlValue = config[JsonKey.config.self][JsonKey.config.splicingSQL.self][JsonKey.config.splicingSQL.value]
            splicingSQL = f'{sqlValue} 拼接的SQL'
            sqlP = f', @Param("{sqlValue}") String {sqlValue}'

        for obj in config["oneToMany"]:
            objClassName = obj["className"]
            objLowClassName = StringUtil.first_char_lower_case(objClassName)
            objRemark = obj["remark"]
            importSet.add(f'{obj[JsonKey.package]}')

            # 一对多内联查询
            method_str += create_annotation(f'内联一对多查询{objRemark}，双方均可分页',
                                            f"{remark}对象列表",
                                            f'{lowClassName} {remark}对象',
                                            f'{objLowClassName} {objRemark}对象',
                                            f'onePage {remark}分页对象',
                                            f'manyPage {objRemark}分页对象',
                                            splicingSQL,
                                            )
            method_str += f'\tList<{className}> find{className}OneToMany{objClassName}(' \
                          f'@Param("{lowClassName}") {className} {lowClassName}, ' \
                          f'@Param("{objLowClassName}") {objClassName} {objLowClassName}, ' \
                          f'@Param("onePage") Page onePage, ' \
                          f'@Param("manyPage") Page manyPage' \
                          f'{sqlP}' \
                          f');\n\n'
            # 一对多内联统计
            method_str += create_annotation(f'内联一对多统计{objRemark}，双方均可分页',
                                            f"查询到的记录数",
                                            f'{lowClassName} {remark}对象',
                                            f'{objLowClassName} {objRemark}对象',
                                            f'onePage {remark}分页对象',
                                            f'manyPage {objRemark}分页对象',
                                            )
            method_str += f'\tInteger countFind{className}OneToMany{objClassName}(' \
                          f'@Param("{lowClassName}") {className} {lowClassName}, ' \
                          f'@Param("{objLowClassName}") {objClassName} {objLowClassName}, ' \
                          f'@Param("onePage") Page onePage, ' \
                          f'@Param("manyPage") Page manyPage' \
                          f');\n\n'
            # 一对多反获取对方
            method_str += create_annotation(f'内联一对多查询{objRemark}，只返回{objRemark}',
                                            f"{remark}对象列表",
                                            f'{lowClassName} {remark}对象',
                                            f'{objLowClassName} {objRemark}对象',
                                            f'onePage {remark}分页对象',
                                            f'manyPage {objRemark}分页对象',
                                            splicingSQL,
                                            )
            method_str += f'\tList<{objClassName}> linkOneToMany{objClassName}(' \
                          f'@Param("{lowClassName}") {className} {lowClassName}, ' \
                          f'@Param("{objLowClassName}") {objClassName} {objLowClassName}, ' \
                          f'@Param("onePage") Page onePage, ' \
                          f'@Param("manyPage") Page manyPage' \
                          f'{sqlP}' \
                          f');\n\n'
            # 一对多外联
            method_str += create_annotation(f'外联一对多查询{objRemark}，双方均可分页',
                                            f"{remark}对象列表",
                                            f'{lowClassName} {remark}对象',
                                            f'{objLowClassName} {objRemark}对象',
                                            f'onePage {remark}分页对象',
                                            f'manyPage {objRemark}分页对象',
                                            splicingSQL,
                                            )
            method_str += f'\tList<{className}> query{className}OneToMany{objClassName}(' \
                          f'@Param("{lowClassName}") {className} {lowClassName}, ' \
                          f'@Param("{objLowClassName}") {objClassName} {objLowClassName}, ' \
                          f'@Param("onePage") Page onePage, ' \
                          f'@Param("manyPage") Page manyPage' \
                          f'{sqlP}' \
                          f');\n\n'

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
                                            f'{lowClassName} {className}对象',
                                            f'page 分页对象',
                                            )
            method_str += f'\tList<{className}> find{className}ManyToManyLink{toClassName}On{manyClassName}(' \
                          f'@Param("{lowClassName}") {className} {lowClassName}, ' \
                          f'@Param("page") Page page' \
                          f');\n\n'
            # 多对多外联
            method_str += create_annotation(f'内联多对多查询{remark},根据{toRemark}联查{manyRemark}',
                                            f"{className}对象列表",
                                            f'{lowClassName} {className}对象',
                                            f'page 分页对象',
                                            )
            method_str += f'\tList<{className}> query{className}ManyToManyLink{toClassName}On{manyClassName}(' \
                          f'@Param("{lowClassName}") {className} {lowClassName}, ' \
                          f'@Param("page") Page page' \
                          f');\n\n'
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
            method_str += create_annotation(f'根据{attr[JsonKey.attr.remark]}列表和其他条件查询{remark}', f"{remark}对象列表", f'list {remark}的{attr[JsonKey.attr.remark]}列表', f'{lowClassName} {remark}对象')
            method_str += f'\tList<{className}> select{className}In{StringUtil.first_char_upper_case(attr[JsonKey.attr.attr])}AndWhere(' \
                          f'@Param("list") List<{attr[JsonKey.attr.type]}> list, ' \
                          f'@Param("{lowClassName}") {className} {lowClassName});\n\n'
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
