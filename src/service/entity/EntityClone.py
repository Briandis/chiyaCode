from src.util import StringUtil


class CreateFile:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config):
        importSet = set()
        methodData = CreateMethod.create(config, importSet)

        data = f'package {config["module"]["entityClone"]["path"]};\n'
        data += "\n"
        data += f'import java.util.ArrayList;\n'
        data += f'import java.util.List;\n'
        # 生成导包文件
        data += CreateImportData.create(config, importSet)
        data += "\n"
        # 文件本体内容
        data += f'public class {config["module"]["entityClone"]["className"]} {{\n'
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
        if config["path"] != config["module"]["entityClone"]["path"]:
            importSet.add(config["package"])
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
        attrs.append([config["module"]["entityClone"]["key"]])
        for attr in config["module"]["entityClone"]["attr"]:
            attrs.append(attr)
        attr_str = ""
        for attr in attrs:
            attr_str += StringUtil.create_annotation(attr["remark"])
            attr_str += f'\tprivate {attr["type"]} {attr["attr"]};\n'
            if attr["type"] == "Date":
                importSet.add("java.util.Date")
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
            attr_str += StringUtil.create_annotation(f'获取{attr["remark"]}', f'{attr["remark"]}')
            attr_str += f'\tpublic {attr["type"]} get{StringUtil.first_char_upper_case(attr["attr"])}() {{\n'
            attr_str += f'\t\treturn {attr["attr"]};\n'
            attr_str += f'\t}}\n'
            attr_str += '\n'
        for attr in attrs:
            attrName = attr["attr"]
            lowAttrName = StringUtil.first_char_upper_case(attrName)

            attr_str += StringUtil.create_annotation(f'设置{attr["remark"]}', None, f'{lowAttrName} {attr["remark"]}对象')
            attr_str += f'\tpublic void set{attrName}({attr["type"]} {lowAttrName}) {{\n'
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
            lowAttrName = StringUtil.first_char_upper_case(attrName)

            attr_str += StringUtil.create_annotation(f'链式添加{attr["remark"]}', "对象本身", f'{lowAttrName} {attr["remark"]}对象')
            attr_str += f'\tpublic T chain{attrName}({attr["type"]} {lowAttrName}) {{\n'
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


class CreateMethodConstruction:
    """
    创建方构造方法
    """

    @staticmethod
    def create(config, importSet: set, attrs: list):
        className = config["module"]["entityClone"]["className"]
        remark = config["module"]["entityClone"]["remark"]
        key = config["module"]["entityClone"]["key"]["attr"]
        upperKey = StringUtil.first_char_upper_case(key)
        keyType = config["module"]["entityClone"]["key"]["type"]
        baseClassName = config["className"]
        lowBaseClassName = StringUtil.first_char_lower_case(config["className"])
        baseKey = config["module"]["entityClone"]["key"]["inAttr"]
        upperBaseKey = StringUtil.first_char_upper_case(baseKey)
        attr_str = ""
        # 空构造方法
        attr_str += f'\tpublic {className}() {{}}\n\n'
        # 主键构造方法
        attr_str += f'\tpublic {className}({keyType} {key}) {{\n\n'
        attr_str += f'\t\tif ({key} == null){{ throw new NullPointerException(); }}\n'
        attr_str += f'\t\tthis.{key} = {key};\n'
        attr_str += f'\t}}\n'
        # 克隆对象构造方法
        attr_str += f'\tpublic {className}({baseClassName} {lowBaseClassName}) {{\n\n'
        attr_str += f'\t\tif ({lowBaseClassName} != null){{\n'
        attr_str += f'\t\t\tthis.{key} = {lowBaseClassName}.get{upperBaseKey}();\n'
        for attr in config["module"]["entityClone"]["attr"]:
            if "inAttr" in attr and attr["inAttr"] is not None:
                attr_str += f'\t\t\tthis.{attr["attr"]} = {lowBaseClassName}.get{StringUtil.first_char_upper_case(attr["inAttr"])}();\n'
        attr_str += f'\t\t}}\n'
        attr_str += f'\t}}\n'
        # 转换克隆对象
        attr_str += StringUtil.create_annotation(f'{remark}转{config["remark"]}', f'{config["remark"]}对象')
        attr_str += f'\tpublic {baseClassName} to{baseClassName}() {{\n\n'
        attr_str += f'\t\t{baseClassName} {lowBaseClassName} = new {baseClassName}();\n'
        attr_str += f'\t\t{lowBaseClassName}.set{upperBaseKey}({key});\n'
        for attr in config["entityClone"]["attr"]:
            if "inAttr" in attr and attr["inAttr"] is not None:
                attr_str += f'\t\t{lowBaseClassName}.set{StringUtil.first_char_upper_case(attr["inAttr"])}({attr["attr"]});\n'
        attr_str += f'\t\treturn {lowBaseClassName};\n'
        attr_str += f'\t}}\n'
        # 列表转换
        attr_str += StringUtil.create_annotation(f'{config["remark"]}转{remark}', f'{remark}列表', f'lists {config["remark"]}列表')
        attr_str += f'\tpublic static List<{className}> toList(List<{baseClassName}> lists) {{\n\n'
        attr_str += f'\t\tif (lists == null) {{ return null; }}\n'
        attr_str += f'\t\tList<{className}> list = new ArrayList<{className}>();\n'
        attr_str += f'\t\tfor ({baseClassName} {lowBaseClassName} : lists) {{\n'
        attr_str += f'\t\t\tlist.add(new {className}({lowBaseClassName}));\n'
        attr_str += f'\t\t}}\n'
        attr_str += f'\t\tGameLabelMap;\n'
        attr_str += f'\t}}\n'

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
        data += CreateMethodConstruction.create(config, importSet, attrs)
        data += CreateMethodGetSet.create(config, importSet, attrs)
        if config["config"]["chain"]["enable"]:
            data += CreateMethodChain.create(config, importSet, attrs)
        if config["config"]["toJsonString"]["enable"]:
            data += CreateMethodToString.create(config, importSet, attrs)
        return data
