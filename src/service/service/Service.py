from src.util import StringUtil


class CreateService:
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

        data = f'package {config["module"]["serviceInterface"]["path"]};\n'
        data += "\n"
        # 生成导包文件
        data += CreateImportData.create(config, importSet)
        data += "\n"
        # 文件本体内容
        data += f'public interface {config["module"]["serviceInterface"]["className"]} {{\n'
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

        if config["path"] != config["module"]["serviceInterface"]["path"]:
            importSet.add(config["package"])
        for i in importSet:
            data += f'import {i};\n'
        return data


class CreateMethodDefaultAPI:
    """
    创建默认方法
    """

    @staticmethod
    def create(config):
        lowClassName = StringUtil.first_char_lower_case(config["className"])
        className = config["className"]
        remark = config["remark"]
        method_str = "\n"
        name = CreateMethodDefaultAPI.methodName(config)
        key = config["key"]["attr"]
        keyType = config["key"]["type"]

        # 增
        method_str += StringUtil.create_annotation(f'添加{remark}', f'true:成功/false:失败', f'{lowClassName} {remark}对象')
        method_str += f'\tboolean {name[0]}{className}({className} {lowClassName});\n\n'
        # 删除方法主键
        method_str += StringUtil.create_annotation(f'删除{remark}', f'true:成功/false:失败', f'{key} {remark}的{key}')
        method_str += f'\tboolean {name[1]}{className}({keyType} {key});\n\n'
        # 更新
        method_str += StringUtil.create_annotation(f'修改{remark}', f'true:成功/false:失败', f'{lowClassName} {remark}对象')
        method_str += f'\tboolean {name[2]}{className}({className} {lowClassName});\n\n'
        # 单个查询
        method_str += StringUtil.create_annotation(f'获取一个{remark}', f'{remark}对象', f'{key} {remark}的{key}')
        method_str += f'\t{className} {name[3]}{className}({keyType} {key});\n\n'
        # 多个查询
        method_str += StringUtil.create_annotation(f'获取多个{remark}', f'{remark}对象列表', f'{lowClassName} {remark}对象', f'page 分页对象')
        method_str += f'\tList<{className}> {name[4]}{className}({className} {lowClassName}, Page page);\n\n'

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
        key = config["key"]["attr"]
        keyType = config["key"]["type"]

        extraName = config["config"]["extraAPI"]["default"].split(",")
        if config["config"]["extraAPI"]["value"] is not None:
            extraName = config["config"]["extraAPI"]["value"].split(",")
        for i in extraName:
            # 增
            method_str += StringUtil.create_annotation(f'添加{remark}', f'true:成功/false:失败', f'{lowClassName} {remark}对象')
            method_str += f'\tboolean {i}{name[0]}{className}({className} {lowClassName});\n\n'
            # 删除方法主键
            method_str += StringUtil.create_annotation(f'删除{remark}', f'true:成功/false:失败', f'{key} {remark}的{key}')
            method_str += f'\tboolean {i}{name[1]}{className}({keyType} {key});\n\n'
            # 更新
            method_str += StringUtil.create_annotation(f'修改{remark}', f'true:成功/false:失败', f'{lowClassName} {remark}对象')
            method_str += f'\tboolean {i}{name[2]}{className}({className} {lowClassName});\n\n'
            # 单个查询
            method_str += StringUtil.create_annotation(f'获取一个{remark}', f'{remark}对象', f'{key} {remark}的{key}')
            method_str += f'\t{className} {i}{name[3]}{className}({keyType} {key});\n\n'
            # 多个查询
            method_str += StringUtil.create_annotation(f'获取多个{remark}', f'{remark}对象列表', f'{lowClassName} {remark}对象', f'page 分页对象')
            method_str += f'\tList<{className}> {i}{name[4]}{className}({className} {lowClassName}, Page page);\n\n'

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
        data = ""
        if config["config"]["defaultAPI"]["enable"]:
            data += CreateMethodDefaultAPI.create(config)
        if config["config"]["extraAPI"]["enable"]:
            data += CreateMethodExtraAPI.create(config)
        return data
