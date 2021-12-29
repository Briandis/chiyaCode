from src.util import StringUtil


class CreateFile:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config):
        importSet = set()
        isRestful = config["config"]["restful"]["enable"]
        if isRestful:
            importSet.add("org.springframework.web.bind.annotation.RestController")
            importSet.add("org.springframework.web.bind.annotation.GetMapping")
            importSet.add("org.springframework.web.bind.annotation.PostMapping")
            importSet.add("org.springframework.web.bind.annotation.PutMapping")
            importSet.add("org.springframework.web.bind.annotation.DeleteMapping")
        else:
            importSet.add("org.springframework.stereotype.Controller")
            importSet.add("org.springframework.web.bind.annotation.ResponseBody")

        importSet.add("org.springframework.web.bind.annotation.RequestMapping")
        methodData = CreateMethod.create(config, importSet)

        data = f'package {config["controller"]["path"]};\n'
        data += "\n"
        # 生成导包文件
        data += CreateImportData.create(config, importSet)
        data += "\n"
        # 文件本体内容
        if isRestful:
            data += '@RestController\n'
            data += f'@RequestMapping("/{StringUtil.first_char_lower_case(config["className"])}")\n'
            data += f'public class {config["controller"]["className"]} {{\n'
        else:
            data += '@Controller\n'
            data += f'@RequestMapping("/{StringUtil.first_char_lower_case(config["className"])}")\n'
            data += f'public class {config["controller"]["className"]} {{\n'
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
        data += f'import {config["Page"]["package"]};\n'
        data += "import org.springframework.beans.factory.annotation.Autowired;\n"
        data += "import org.springframework.beans.factory.annotation.Qualifier;\n"
        data += "import chiya.core.base.result.Result;\n"

        if config["controller"]["path"] != config["path"]:
            importSet.add(config["package"])

        if config["controller"]["path"] != config["serviceInterface"]["path"]:
            importSet.add(config["serviceInterface"]["package"])

        for i in importSet:
            data += f'import {i};\n'
        return data


class CreateAttribute:
    """
    创建属性
    """

    @staticmethod
    def create(config, importSet: set):
        serviceClassName = config["serviceInterface"]["className"]
        lowServiceClassName = StringUtil.first_char_lower_case(serviceClassName)
        serviceImplClassName = config["serviceImplements"]["className"]
        lowServiceImplClassName = StringUtil.first_char_lower_case(serviceImplClassName)
        attr_str = ""
        attr_str += f'\t@Autowired\n'
        attr_str += f'\t@Qualifier("{lowServiceImplClassName}")\n'
        attr_str += f'\tprivate {serviceClassName} {lowServiceClassName};\n\n'
        return attr_str


class CreateMethodDefaultAPI:
    """
    创建默认方法
    """

    @staticmethod
    def create(config):
        isRestful = config["config"]["restful"]["enable"]

        className = config["className"]
        lowClassName = StringUtil.first_char_lower_case(className)
        remark = config["remark"]
        method_str = ""
        name = CreateMethodDefaultAPI.methodName(config)
        key = config["key"]["attr"]
        upperKey = StringUtil.first_char_upper_case(key)
        keyType = config["key"]["type"]

        serviceClassName = config["serviceInterface"]["className"]
        lowServiceClassName = StringUtil.first_char_lower_case(serviceClassName)

        # 增
        method_str += StringUtil.create_annotation(f'添加{remark}', f'Result业务对象', f'{lowClassName} {remark}对象')

        if isRestful:
            method_str += f'\t@PostMapping("/{lowClassName}")\n'
        else:
            method_str += f'\t@RequestMapping("/{name[0]}{className}")\n'

        method_str += f'\tpublic Result {name[0]}{className}({className} {lowClassName}){{\n'
        method_str += f'\t\tboolean b = false;\n'
        method_str += f'\t\tb = {lowServiceClassName}.{name[0]}{className}({lowClassName});\n'
        method_str += f'\t\treturn Result.judge(b);\n'
        method_str += f'\t}}\n'

        # 删除方法主键
        method_str += StringUtil.create_annotation(f'删除{remark},{key}必传', f'Result业务对象', f'{key} {remark}的{key}')

        if isRestful:
            method_str += f'\t@DeleteMapping("/{lowClassName}")\n'
        else:
            method_str += f'\t@RequestMapping("/{name[1]}{className}")\n'

        method_str += f'\tpublic Result {name[1]}{className}({keyType} {key}){{\n'
        method_str += f'\t\tboolean b = false;\n'
        method_str += f'\t\tif ({key} != null) {{\n'
        method_str += f'\t\t\tb = {lowServiceClassName}.{name[1]}{className}({key});\n'
        method_str += f'\t\t}}\n'
        method_str += f'\t\treturn Result.judge(b);\n'
        method_str += f'\t}}\n'

        # 更新
        method_str += StringUtil.create_annotation(f'修改{remark},{key}必传', f'Result业务对象', f'{lowClassName} {remark}对象')
        if isRestful:
            method_str += f'\t@PutMapping("/{lowClassName}")\n'
        else:
            method_str += f'\t@RequestMapping("/{name[2]}{className}")\n'

        method_str += f'\tpublic Result {name[2]}{className}({className} {lowClassName}){{\n'
        method_str += f'\t\tboolean b = false;\n'
        method_str += f'\t\tif ({lowClassName}.get{upperKey}() != null) {{\n'
        method_str += f'\t\t\tb = {lowServiceClassName}.{name[2]}{className}({lowClassName});\n'
        method_str += f'\t\t}}\n'
        method_str += f'\t\treturn Result.judge(b);\n'
        method_str += f'\t}}\n'

        # 单个查询
        method_str += StringUtil.create_annotation(f'获取一个{remark},{key}必传', f'Result业务对象', f'{key} {remark}的{key}')
        if isRestful:
            method_str += f'\t@GetMapping("/{lowClassName}")\n'
        else:
            method_str += f'\t@RequestMapping("/{name[3]}{className}")\n'

        method_str += f'\tpublic Result {name[3]}{className}({keyType} {key}){{\n'
        method_str += f'\t\tboolean b = false;\n'
        method_str += f'\t\tif ({key} != null) {{\n'
        method_str += f'\t\t\treturn Result.success({lowServiceClassName}.{name[3]}{className}({key}));\n'
        method_str += f'\t\t}}\n'
        method_str += f'\t\treturn Result.judge(b);\n'
        method_str += f'\t}}\n'
        # 多个查询
        method_str += StringUtil.create_annotation(f'获取多个{remark}', f'Result业务对象', f'{lowClassName} {remark}对象',
                                                   f'page 分页对象')
        if isRestful:
            method_str += f'\t@GetMapping("/{name[4]}{className}")\n'
        else:
            method_str += f'\t@RequestMapping("/{name[4]}{className}")\n'

        method_str += f'\tpublic Result {name[4]}{className}({className} {lowClassName}, Page page){{\n'
        method_str += f'\t\tList<{className}> list = {lowServiceClassName}.{name[4]}{className}({lowClassName}, page);\n'
        method_str += f'\t\treturn Result.success(list, page);\n'
        method_str += f'\t}}\n'
        # 多个查询

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
        isRestful = config["config"]["restful"]["enable"]
        lowClassName = StringUtil.first_char_lower_case(config["className"])
        className = config["className"]
        remark = config["remark"]
        method_str = ""
        name = CreateMethodExtraAPI.methodName(config)
        key = config["key"]["attr"]
        upperKey = StringUtil.first_char_upper_case(key)
        keyType = config["key"]["type"]
        serviceClassName = config["serviceInterface"]["className"]
        lowServiceClassName = StringUtil.first_char_lower_case(serviceClassName)

        extraName = config["config"]["extraAPI"]["default"].split(",")
        if config["config"]["extraAPI"]["value"] is not None:
            extraName = config["config"]["extraAPI"]["value"].split(",")

        for i in extraName:
            # 增
            method_str += StringUtil.create_annotation(f'添加{remark}', f'Result业务对象', f'{lowClassName} {remark}对象')

            if isRestful:
                method_str += f'\t@PostMapping("/{i}/{lowClassName}")\n'
            else:
                method_str += f'\t@RequestMapping("/{i}/{name[0]}{className}")\n'

            method_str += f'\tpublic Result {i}{name[0]}{className}({className} {lowClassName}){{\n'
            method_str += f'\t\tboolean b = false;\n'
            method_str += f'\t\tb = {lowServiceClassName}.{i}{name[0]}{className}({lowClassName});\n'
            method_str += f'\t\treturn Result.judge(b);\n'
            method_str += f'\t}}\n'

            # 删除方法主键
            method_str += StringUtil.create_annotation(f'删除{remark},{key}必传', f'Result业务对象', f'{key} {remark}的{key}')

            if isRestful:
                method_str += f'\t@DeleteMapping("/{i}/{lowClassName}")\n'
            else:
                method_str += f'\t@RequestMapping("/{i}/{name[1]}{className}")\n'

            method_str += f'\tpublic Result {i}{name[1]}{className}({keyType} {key}){{\n'
            method_str += f'\t\tboolean b = false;\n'
            method_str += f'\t\tif ({key} != null) {{\n'
            method_str += f'\t\t\tb = {lowServiceClassName}.{i}{name[1]}{className}({key});\n'
            method_str += f'\t\t}}\n'
            method_str += f'\t\treturn Result.judge(b);\n'
            method_str += f'\t}}\n'

            # 更新
            method_str += StringUtil.create_annotation(f'修改{remark},{key}必传', f'Result业务对象',
                                                       f'{lowClassName} {remark}对象')
            if isRestful:
                method_str += f'\t@PutMapping("/{i}/{lowClassName}")\n'
            else:
                method_str += f'\t@RequestMapping("/{i}/{name[2]}{className}")\n'

            method_str += f'\tpublic Result {i}{name[2]}{className}({className} {lowClassName}){{\n'
            method_str += f'\t\tboolean b = false;\n'
            method_str += f'\t\tif ({lowClassName}.get{upperKey}() != null) {{\n'
            method_str += f'\t\t\tb = {lowServiceClassName}.{i}{name[2]}{className}({lowClassName});\n'
            method_str += f'\t\t}}\n'
            method_str += f'\t\treturn Result.judge(b);\n'
            method_str += f'\t}}\n'

            # 单个查询
            method_str += StringUtil.create_annotation(f'获取一个{remark},{key}必传', f'Result业务对象', f'{key} {remark}的{key}')
            if isRestful:
                method_str += f'\t@GetMapping("/{i}/{lowClassName}")\n'
            else:
                method_str += f'\t@RequestMapping("/{i}/{name[3]}{className}")\n'

            method_str += f'\tpublic Result {i}{name[3]}{className}({keyType} {key}){{\n'
            method_str += f'\t\tboolean b = false;\n'
            method_str += f'\t\tif ({key} != null) {{\n'
            method_str += f'\t\t\treturn Result.success({lowServiceClassName}.{i}{name[3]}{className}({key}));\n'
            method_str += f'\t\t}}\n'
            method_str += f'\t\treturn Result.judge(b);\n'
            method_str += f'\t}}\n'
            # 多个查询
            method_str += StringUtil.create_annotation(f'获取多个{remark}', f'Result业务对象', f'{lowClassName} {remark}对象',
                                                       f'page 分页对象')
            if isRestful:
                method_str += f'\t@GetMapping("/{i}/{name[4]}{className}")\n'
            else:
                method_str += f'\t@RequestMapping("/{i}/{name[4]}{className}")\n'

            method_str += f'\tpublic Result {i}{name[4]}{className}({className} {lowClassName}, Page page){{\n'
            method_str += f'\t\tList<{className}> list = {lowServiceClassName}.{i}{name[4]}{className}({lowClassName}, page);\n'
            method_str += f'\t\treturn Result.success(list, page);\n'
            method_str += f'\t}}\n'

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
