from src.constant.ProtocolConstant import JsonKey


class CreateFile:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config):
        importSet = set()
        methodData = CreateMethod.create(config, importSet)

        data = f'package {config["path"]};\n'
        data += "\n"
        # 生成导包文件
        data += CreateImportData.create(config, importSet)
        data += "\n"
        # 注释块
        data += f'/**\n'
        data += f' * {config[JsonKey.remark]}\n'
        data += f' */\n'
        # 文件本体内容
        data += f'public class {config["className"]} extends {config["module"]["baseEntity"]["className"]}<{config["className"]}> {{\n'
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
        if config["path"] != config["module"]["baseEntity"]["path"]:
            importSet.add(config["module"]["baseEntity"]["package"])

        for i in importSet:
            data += f'import {i}\n'
        return data


# 创建方法
class CreateMethod:
    """
    创建接口方法
    """

    @staticmethod
    def create(config: dict, importSet: set):
        data = ""
        return data
