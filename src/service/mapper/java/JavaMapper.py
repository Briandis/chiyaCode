class CreateFile:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config):
        importSet = set()
        methodData = CreateMethod.create(config, importSet)

        data = f'package {config["mapperInterface"]["path"]};\n'
        data += "\n"
        # 生成导包文件
        data += CreateImportData.create(config, importSet)
        data += "\n"
        # 文件本体内容
        data += f'@Mapper\n'
        data += f'public interface {config["mapperInterface"]["className"]} extend {config["baseMapperInterface"]["className"]} {{\n'
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
        data =""
        # data += "import java.util.List;\n"
        # data += f'import {config["Page"]["package"]};\n'
        data += f'import org.apache.ibatis.annotations.Mapper;\n'
        if config["mapperInterface"]["path"] != config["baseMapperInterface"]["path"]:
            importSet.add(config["baseMapperInterface"]["package"])

        for i in importSet:
            data += f'import {i};\n'
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
