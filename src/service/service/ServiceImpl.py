from src.constant.ProtocolConstant import JsonKey
from src.util import StringUtil


class FuzzySearch:
    """
    模糊搜索处理类
    """

    @staticmethod
    def param(config):
        """
        获取模糊搜索的方法参数
        :param config: 配置
        :return: None|方法参数字符串
        """
        if config["config"]["fuzzySearch"]["enable"]:
            if len(config["config"]["fuzzySearch"]["data"]) != 0:
                return ", null"
        return ""


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
            return f', null'
        return ""


class CreateServiceImpl:
    """
    创建生成对象
    """

    @staticmethod
    def create(config: dict):
        return CreateFile.create(config)


class CreateFile:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config):
        importSet = set()
        methodData = CreateMethod.create(config, importSet)

        data = f'package {config["module"]["serviceImplements"]["path"]};\n'
        data += "\n"
        # 生成导包文件
        data += CreateImportData.create(config, importSet)
        data += "\n"
        # 文件本体内容
        data += f'@Service\n'
        data += f'public class {config["module"]["serviceImplements"]["className"]} implements {config["module"]["serviceInterface"]["className"]} {{\n'
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
        data = ""
        data += "import java.util.List;\n"
        data += f'import {config["module"]["Page"]["package"]};\n'
        data += "import org.springframework.stereotype.Service;\n"
        data += "import org.springframework.beans.factory.annotation.Autowired;\n"

        if config["path"] != config["module"]["serviceImplements"]["path"]:
            importSet.add(config["package"])
        if config["module"]["serviceInterface"]["path"] != config["module"]["serviceImplements"]["path"]:
            importSet.add(config["module"]["serviceInterface"]["package"])
        if config["module"]["mapperXml"]["path"] != config["module"]["serviceImplements"]["path"]:
            importSet.add(config["module"]["mapperXml"]["package"])

        for i in importSet:
            data += f'import {i};\n'
        return data


class CreateAttribute:
    """
    创建属性
    """

    @staticmethod
    def create(config, importSet: set):
        mapperClassName = config["module"]["mapperInterface"]["className"]
        lowMapperClassName = StringUtil.first_char_lower_case(mapperClassName)
        importSet.add(config["module"]["mapperInterface"]["package"])
        attr_str = ""
        attr_str += f'\t@Autowired\n'
        attr_str += f'\tprivate {mapperClassName} {lowMapperClassName};\n\n'
        return attr_str


class CreateMethodDefaultAPI:
    """
    创建默认方法
    """

    @staticmethod
    def create(config):
        lowClassName = StringUtil.first_char_lower_case(config["className"])
        className = config["className"]
        remark = config["remark"]
        method_str = ""
        name = CreateMethodDefaultAPI.methodName(config)
        key = None
        if "key" in config:
            key = config["key"]["attr"]
            upperKey = StringUtil.first_char_upper_case(key)
            keyType = config["key"]["type"]

        mapperClassName = config["module"]["mapperInterface"]["className"]
        lowMapperClassName = StringUtil.first_char_lower_case(mapperClassName)

        # 增
        method_str += StringUtil.create_annotation(f'添加{remark}', f'true:成功/false:失败', f'{lowClassName} {remark}对象')
        method_str += f'\t@Override\n'
        method_str += f'\tpublic boolean {name[0]}{className}({className} {lowClassName}){{\n'
        method_str += f'\t\treturn {lowMapperClassName}.insert{className}({lowClassName}) > 0;\n'
        method_str += f'\t}}\n\n'

        # 删除方法主键
        if key:
            method_str += StringUtil.create_annotation(f'删除{remark}', f'true:成功/false:失败', f'{key} {remark}的{key}')
            method_str += f'\t@Override\n'
            method_str += f'\tpublic boolean {name[1]}{className}({keyType} {key}){{\n'
            method_str += f'\t\treturn {lowMapperClassName}.delete{className}By{upperKey}({key}) > 0;\n'
            method_str += f'\t}}\n\n'
        else:
            method_str += StringUtil.create_annotation(f'删除{remark}', f'true:成功/false:失败', f'{lowClassName} {remark}')
            method_str += f'\t@Override\n'
            method_str += f'\tpublic boolean {name[1]}{className}({className} {lowClassName}){{\n'
            method_str += f'\t\treturn {lowMapperClassName}.delete{className}({lowClassName}{FuzzySearch.param(config)}) > 0;\n'
            method_str += f'\t}}\n\n'
        # 更新
        if key:
            method_str += StringUtil.create_annotation(f'修改{remark}', f'true:成功/false:失败', f'{lowClassName} {remark}对象')
            method_str += f'\t@Override\n'
            method_str += f'\tpublic boolean {name[2]}{className}({className} {lowClassName}){{\n'
            method_str += f'\t\treturn {lowMapperClassName}.update{className}By{upperKey}({lowClassName}) > 0;\n'
            method_str += f'\t}}\n\n'
        # 单个查询
        if key:
            method_str += StringUtil.create_annotation(f'获取一个{remark}', f'{remark}对象', f'{key} {remark}的{key}')
            method_str += f'\t@Override\n'
            method_str += f'\tpublic {className} {name[3]}{className}({keyType} {key}){{\n'
            method_str += f'\t\treturn {lowMapperClassName}.select{className}By{upperKey}({key});\n'
            method_str += f'\t}}\n\n'
        # 多个查询
        method_str += StringUtil.create_annotation(f'获取多个{remark}', f'{remark}对象列表', f'{lowClassName} {remark}对象', f'page 分页对象')
        method_str += f'\t@Override\n'
        method_str += f'\tpublic List<{className}> {name[4]}{className}({className} {lowClassName}, Page page){{\n'
        method_str += f'\t\tif (page != null) {{\n'
        method_str += f'\t\t\tpage.setMax({lowMapperClassName}.count{className}({lowClassName}{FuzzySearch.param(config)}));\n'
        method_str += f'\t\t}}\n'
        method_str += f'\t\treturn {lowMapperClassName}.select{className}({lowClassName}, page{FuzzySearch.param(config)}{SplicingSQL.param(config)});\n'
        method_str += f'\t}}\n\n'

        method_str += "\n"
        return method_str

    @staticmethod
    def methodName(config: dict) -> list:
        data = config["config"]["methodName"]["default"]
        lists = data.split(",")
        if config["config"]["methodName"]["enable"]:
            lists = config["config"]["methodName"]["value"].split(",")
        return lists


class CreateMethodExtraAPI:
    """
    创建额外方法
    """

    @staticmethod
    def create(config):
        lowClassName = StringUtil.first_char_lower_case(config["className"])
        className = config["className"]
        remark = config["remark"]
        method_str = ""
        name = CreateMethodExtraAPI.methodName(config)
        key = None
        if "key" in config:
            key = config["key"]["attr"]
            upperKey = StringUtil.first_char_upper_case(key)
            keyType = config["key"]["type"]
        mapperClassName = config["module"]["mapperInterface"]["className"]
        lowMapperClassName = StringUtil.first_char_lower_case(mapperClassName)

        extraName = config["config"]["extraAPI"]["default"].split(",")
        if config["config"]["extraAPI"]["value"] is not None:
            extraName = config["config"]["extraAPI"]["value"].split(",")

        for i in extraName:
            # 增
            method_str += StringUtil.create_annotation(f'添加{remark}', f'true:成功/false:失败', f'{lowClassName} {remark}对象')
            method_str += f'\t@Override\n'
            method_str += f'\tpublic boolean {i}{name[0]}{className}({className} {lowClassName}){{\n'
            method_str += f'\t\treturn {lowMapperClassName}.insert{className}({lowClassName}) > 0;\n'
            method_str += f'\t}}\n\n'

            # 删除方法主键
            if key:
                method_str += StringUtil.create_annotation(f'删除{remark}', f'true:成功/false:失败', f'{key} {remark}的{key}')
                method_str += f'\t@Override\n'
                method_str += f'\tpublic boolean {i}{name[1]}{className}({keyType} {key}){{\n'
                method_str += f'\t\treturn {lowMapperClassName}.delete{className}By{upperKey}({key}) > 0;\n'
                method_str += f'\t}}\n\n'
            else:
                method_str += StringUtil.create_annotation(f'删除{remark}', f'true:成功/false:失败', f'{lowClassName} {remark}')
                method_str += f'\t@Override\n'
                method_str += f'\tpublic boolean {i}{name[1]}{className}({className} {lowClassName}){{\n'
                method_str += f'\t\treturn {lowMapperClassName}.delete{className}({lowClassName}{FuzzySearch.param(config)}) > 0;\n'
                method_str += f'\t}}\n\n'

            # 更新
            if key:
                method_str += StringUtil.create_annotation(f'修改{remark}', f'true:成功/false:失败', f'{lowClassName} {remark}对象')
                method_str += f'\t@Override\n'
                method_str += f'\tpublic boolean {i}{name[2]}{className}({className} {lowClassName}){{\n'
                method_str += f'\t\treturn {lowMapperClassName}.update{className}By{upperKey}({lowClassName}) > 0;\n'
                method_str += f'\t}}\n\n'
            # 单个查询
            if key:
                method_str += StringUtil.create_annotation(f'获取一个{remark}', f'{remark}对象', f'{key} {remark}的{key}')
                method_str += f'\t@Override\n'
                method_str += f'\tpublic {className} {i}{name[3]}{className}({keyType} {key}){{\n'
                method_str += f'\t\treturn {lowMapperClassName}.select{className}By{upperKey}({key});\n'
                method_str += f'\t}}\n\n'
            # 多个查询
            method_str += StringUtil.create_annotation(f'获取多个{remark}', f'{remark}对象列表', f'{lowClassName} {remark}对象', f'page 分页对象')
            method_str += f'\t@Override\n'
            method_str += f'\tpublic List<{className}> {i}{name[4]}{className}({className} {lowClassName}, Page page){{\n'
            method_str += f'\t\tif (page != null) {{\n'
            method_str += f'\t\t\tpage.setMax({lowMapperClassName}.count{className}({lowClassName}{FuzzySearch.param(config)}));\n'
            method_str += f'\t\t}}\n'
            method_str += f'\t\treturn {lowMapperClassName}.select{className}({lowClassName}, page{FuzzySearch.param(config)}{SplicingSQL.param(config)});\n'
            method_str += f'\t}}\n\n'

        method_str += "\n"
        return method_str

    @staticmethod
    def methodName(config: dict) -> list:
        data = config["config"]["methodName"]["default"]
        lists = data.split(",")
        if config["config"]["methodName"]["enable"]:
            lists = config["config"]["methodName"]["value"].split(",")
        for i in range(len(lists)):
            lists[i] = StringUtil.first_char_upper_case(lists[i])
        return lists


# 创建方法
class CreateMethod:
    """
    创建接口方法
    """

    @staticmethod
    def create(config: dict, importSet: set):
        data = "\n"
        data += CreateAttribute.create(config, importSet)
        if config["config"]["defaultAPI"]["enable"]:
            data += CreateMethodDefaultAPI.create(config)
        if config["config"]["extraAPI"]["enable"]:
            data += CreateMethodExtraAPI.create(config)
        return data
