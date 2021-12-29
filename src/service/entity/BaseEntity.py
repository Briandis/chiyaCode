from src.constant.ProtocolConstant import JsonKey
from src.util import StringUtil


class CreateFile:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config):
        importSet = set()
        methodData = CreateMethod.create(config, importSet)

        data = f'package {config["baseEntity"]["path"]};\n'
        data += "\n"
        # 生成导包文件
        data += CreateImportData.create(config, importSet)
        data += "\n"
        # 文件本体内容
        data += f'/**\n'
        data += f' * {config[JsonKey.remark]}\n'
        data += f' */\n'
        data += f'@SuppressWarnings("unchecked")\n'
        data += f'public abstract class {config["baseEntity"]["className"]}<T> {{\n'
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
        if config["path"] != config["baseEntity"]["path"]:
            importSet.add(config["baseEntity"]["package"])
        if config["config"]["toJsonString"]["isFastJson"]:
            data += f'import com.alibaba.fastjson.JSON;\n'
        for i in importSet:
            data += f'import {i};\n'
        return data


class CreateAttribute:
    """
    创建属性
    """

    @staticmethod
    def create(config, importSet: set, attrs: list):
        attrs.append(config["key"])
        for attr in config["attr"]:
            attrs.append(attr)

        nameSet = set()
        if config.get("oneToOne"):
            for obj in config["oneToOne"]:
                objClassName = obj["className"]
                objLowClassName = StringUtil.first_char_lower_case(objClassName)
                objRemark = obj["remark"]
                if objLowClassName not in nameSet:
                    # 变量名去重
                    nameSet.add(objLowClassName)
                    attrs.append({
                        "attr": objLowClassName,
                        "type": objClassName,
                        "remark": objRemark,
                    })
                importSet.add(f'{obj["package"]}')

        importListFlag = False
        if config.get("oneToMany"):
            for obj in config["oneToMany"]:
                objClassName = obj["className"]
                objRemark = obj["remark"]
                attrName = f'list{objClassName}'
                if attrName not in nameSet:
                    # 变量名去重
                    nameSet.add(attrName)
                    attrs.append({
                        "attr": attrName,
                        "type": f'List<{objClassName}>',
                        "remark": objRemark,
                    })
                importListFlag = True
                importSet.add(f'{obj["package"]}')
        if config.get("manyToMany"):
            for to_many in config["manyToMany"]:
                objClassName = to_many["many"]["className"]
                objRemark = to_many["many"]["remark"]
                attrName = f'list{objClassName}'
                if attrName not in nameSet:
                    # 变量名去重
                    nameSet.add(attrName)
                    attrs.append({
                        "attr": attrName,
                        "type": f'List<{objClassName}>',
                        "remark": objRemark,
                    })
                    importListFlag = True
                importSet.add(f'{to_many["many"]["package"]}')
        attr_str = "\n"
        for attr in attrs:
            attr_str += StringUtil.create_annotation(attr["remark"])
            attr_str += f'\tprivate {attr["type"]} {attr["attr"]};\n'
            if attr["type"] == "Date":
                importSet.add("java.util.Date")
            if importListFlag:
                importSet.add("java.util.List")
            if attr["type"] == "BigDecimal":
                importSet.add("java.math.BigDecimal")
        attr_str += "\n"
        return attr_str


class CreateMethodGetSet:
    """
    创建get,set
    """

    @staticmethod
    def create(config, importSet: set, attrs: list):
        attr_str = ""
        for attr in attrs:
            upperAttr = StringUtil.first_char_upper_case(attr["attr"])
            attr_str += StringUtil.create_annotation(f'获取{attr["remark"]}', f'{attr["remark"]}')
            attr_str += f'\tpublic {attr["type"]} get{upperAttr}() {{\n'
            attr_str += f'\t\treturn {attr["attr"]};\n'
            attr_str += f'\t}}\n'
            attr_str += '\n'
        for attr in attrs:
            attrName = attr["attr"]
            upperAttr = StringUtil.first_char_upper_case(attr["attr"])

            attr_str += StringUtil.create_annotation(f'设置{attr["remark"]}', None, f'{attrName} {attr["remark"]}对象')
            attr_str += f'\tpublic void set{upperAttr}({attr["type"]} {attrName}) {{\n'
            attr_str += f'\t\tthis.{attrName} = {attrName};\n'
            attr_str += f'\t}}\n'
            attr_str += '\n'

        attr_str += "\n"
        return attr_str


class CreateMethodChain:
    """
    创建方法链
    """

    @staticmethod
    def create(config, importSet: set, attrs: list):
        attr_str = ""
        for attr in attrs:
            attrName = attr["attr"]
            upperAttr = StringUtil.first_char_upper_case(attr["attr"])

            attr_str += StringUtil.create_annotation(f'链式添加{attr["remark"]}', "对象本身", f'{attrName} {attr["remark"]}对象')
            attr_str += f'\tpublic T chain{upperAttr}({attr["type"]} {attrName}) {{\n'
            attr_str += f'\t\tthis.{attrName} = {attrName};\n'
            attr_str += f'\t\treturn (T) this;\n'
            attr_str += f'\t}}\n'
            attr_str += '\n'

        attr_str += "\n"
        return attr_str


class CreateMethodToString:
    """
    创建方toString方法
    """

    @staticmethod
    def create(config, importSet: set, attrs: list):
        attr_str = ""
        attr_str += "\t@Override\n"
        attr_str += "\tpublic String toString() {\n"
        if config["config"]["toJsonString"]["isFastJson"]:
            attr_str += "\t\treturn JSON.toJSONString(this);\n"
        else:
            attr_str += f'\t\tStringBuilder builder = new StringBuilder();\n'
            attr_str += f'\t\tbuilder.append("{{");\n'
            i = 0
            for attr in attrs:
                attrName = attr["attr"]
                lowAttrName = StringUtil.first_char_upper_case(attrName)

                attr_str += f'\t\tbuilder.append("\\"{attrName}\\" : \"\""+{attrName}+"\"" );\n'
                if i < len(attrs) - 1:
                    attr_str += f'\t\tbuilder.append(",");\n'
                i += 1
        attr_str += "\t}\n"
        attr_str += "\n"
        return attr_str


# 创建方法
class CreateMethod:
    """
    创建接口方法
    """

    @staticmethod
    def create(config: dict, importSet: set):
        data = ""
        attrs = []
        data += CreateAttribute.create(config, importSet, attrs)
        data += CreateMethodGetSet.create(config, importSet, attrs)
        if config["config"]["chain"]["enable"]:
            data += CreateMethodChain.create(config, importSet, attrs)
        if config["config"]["toJsonString"]["enable"]:
            data += CreateMethodToString.create(config, importSet, attrs)
        return data
