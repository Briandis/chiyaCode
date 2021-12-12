from src.util import stringUtil


def create_service_impl(config: dict):
    data = f'package {config["extradimensionalData"]["path_service_impl"]};\n\n'
    # 导包区
    data += "import java.util.List;\n"
    data += f'import {config["extradimensionalData"]["path_util"]}.Page;\n'
    data += "import org.springframework.beans.factory.annotation.Autowired;\n"
    data += "import org.springframework.stereotype.Service;\n"
    if config["extradimensionalData"]["path_service_impl"] != config["extradimensionalData"]["path_java_mapper"]:
        data += f'import {config["extradimensionalData"]["path_java_mapper"]}.{config["extradimensionalData"]["javaMapperName"]};\n'

    data += "\n"
    data += '@Service\n'
    data += f'public class {config["extradimensionalData"]["serviceImplName"]} implements {config["extradimensionalData"]["serviceName"]} {{\n\n{__create_method_impl(config)}}}'
    return data


def __create_method_impl(config: dict):
    tag = "\t"
    data = f'{tag}@Autowired\n'
    data += f'{tag}private {config["extradimensionalData"]["javaMapperName"]} {stringUtil.low_str_first(config["extradimensionalData"]["javaMapperName"])};\n'
    data += "\n"
    if config["extradimensionalData"].get("userAPI") == "true":
        data += __method_add(config)
        data += __method_delete_by_id(config)
        data += __method_update(config)
        data += __method_select_by_id(config)
        data += __method_select(config)
    if config["extradimensionalData"].get("adminAPI") == "true":
        data += __method_admin_add(config)
        data += __method_admin_delete_by_id(config)
        data += __method_admin_update(config)
        data += __method_admin_select_by_id(config)
        data += __method_admin_select(config)
    return data


def __method_add(config: dict):
    tag = "\t"
    method_code = f'{tag * 2}return {stringUtil.low_str_first(config["extradimensionalData"]["javaMapperName"])}.insert{config["className"]}({stringUtil.low_str_first(config["extradimensionalData"]["className"])}.to{config["className"]}()) > 0;\n'
    method_str = f'{tag}@Override\n'
    method_str += f'{tag}public boolean add{config["extradimensionalData"]["className"]}({config["extradimensionalData"]["className"]} {stringUtil.low_str_first(config["extradimensionalData"]["className"])}) {{\n{method_code}{tag}}}\n\n'
    return method_str


def __method_admin_add(config: dict):
    tag = "\t"
    method_code = f'{tag * 2}return {stringUtil.low_str_first(config["extradimensionalData"]["javaMapperName"])}.insert{config["className"]}({stringUtil.low_str_first(config["extradimensionalData"]["className"])}.to{config["className"]}()) > 0;\n'
    method_str = f'{tag}@Override\n'
    method_str += f'{tag}public boolean adminAdd{config["extradimensionalData"]["className"]}({config["extradimensionalData"]["className"]} {stringUtil.low_str_first(config["extradimensionalData"]["className"])}) {{\n{method_code}{tag}}}\n\n'
    return method_str


def __method_delete_by_id(config: dict):
    tag = "\t"
    method_str = f'{tag}@Override\n'
    temp = ""
    if config.get("fuzzySearch") == "true" and "keyWordList" in config and len(config["keyWordList"]) > 0:
        temp = ", null"
    method_code = f'{tag * 2}return {stringUtil.low_str_first(config["extradimensionalData"]["javaMapperName"])}.delete{config["className"]}By{stringUtil.upper_str_first(config["extradimensionalData"]["key"]["inAttr"])}AndWhere({config["extradimensionalData"]["key"]["attr"]}, new {config["extradimensionalData"]["className"]}().to{config["className"]}(){temp}) > 0;\n'
    method_str += f'{tag}public boolean delete{config["extradimensionalData"]["className"]}By{stringUtil.upper_str_first(config["extradimensionalData"]["key"]["attr"])}({config["extradimensionalData"]["key"]["type"]} {config["extradimensionalData"]["key"]["attr"]}) {{\n{method_code}{tag}}}\n\n'
    return method_str


def __method_admin_delete_by_id(config: dict):
    tag = "\t"
    method_str = f'{tag}@Override\n'
    temp = ""
    if config.get("fuzzySearch") == "true" and "keyWordList" in config and len(config["keyWordList"]) > 0:
        temp = ", null"
    method_code = f'{tag * 2}return {stringUtil.low_str_first(config["extradimensionalData"]["javaMapperName"])}.delete{config["className"]}By{stringUtil.upper_str_first(config["extradimensionalData"]["key"]["inAttr"])}AndWhere({config["extradimensionalData"]["key"]["attr"]}, new {config["extradimensionalData"]["className"]}().to{config["className"]}(){temp}) > 0;\n'
    method_str += f'{tag}public boolean adminDelete{config["extradimensionalData"]["className"]}By{stringUtil.upper_str_first(config["extradimensionalData"]["key"]["attr"])}({config["extradimensionalData"]["key"]["type"]} {config["extradimensionalData"]["key"]["attr"]}) {{\n{method_code}{tag}}}\n\n'
    return method_str


def __method_update(config: dict):
    tag = "\t"
    method_str = f'{tag}@Override\n'
    method_code = f'{tag * 2}return {stringUtil.low_str_first(config["extradimensionalData"]["javaMapperName"])}.update{config["className"]}By{stringUtil.upper_str_first(config["extradimensionalData"]["key"]["inAttr"])}AndWhere({stringUtil.low_str_first(config["extradimensionalData"]["className"])}.to{config["className"]}(), new {config["extradimensionalData"]["className"]}().to{config["className"]}()) > 0;\n'
    method_str += f'{tag}public boolean update{config["extradimensionalData"]["className"]}({config["extradimensionalData"]["className"]} {stringUtil.low_str_first(config["extradimensionalData"]["className"])}) {{\n{method_code}{tag}}}\n\n'
    return method_str


def __method_admin_update(config: dict):
    tag = "\t"
    method_str = f'{tag}@Override\n'
    method_code = f'{tag * 2}return {stringUtil.low_str_first(config["extradimensionalData"]["javaMapperName"])}.update{config["className"]}By{stringUtil.upper_str_first(config["extradimensionalData"]["key"]["inAttr"])}AndWhere({stringUtil.low_str_first(config["extradimensionalData"]["className"])}.to{config["className"]}(), new {config["extradimensionalData"]["className"]}().to{config["className"]}()) > 0;\n'
    method_str += f'{tag}public boolean adminUpdate{config["extradimensionalData"]["className"]}({config["extradimensionalData"]["className"]} {stringUtil.low_str_first(config["extradimensionalData"]["className"])}) {{\n{method_code}{tag}}}\n\n'
    return method_str


def __method_select_by_id(config: dict):
    temp1 = ""
    if config.get("fuzzySearch") == "true" and "keyWordList" in config and len(config["keyWordList"]) > 0:
        temp1 = ", null"
    temp2 = ""
    if config.get("SQLInjection") == "true":
        temp2 = ", null"
    tag = "\t"
    method_str = f'{tag}@Override\n'
    method_code = f'{tag * 2}return new {config["extradimensionalData"]["className"]}({stringUtil.low_str_first(config["extradimensionalData"]["javaMapperName"])}.selectOne{config["className"]}(new {config["extradimensionalData"]["className"]}({config["extradimensionalData"]["key"]["attr"]}).to{config["className"]}(){temp1}, 0{temp2}));\n'
    method_str += f'{tag}public {config["extradimensionalData"]["className"]} select{config["extradimensionalData"]["className"]}By{stringUtil.upper_str_first(config["extradimensionalData"]["key"]["attr"])}({config["extradimensionalData"]["key"]["type"]} {config["extradimensionalData"]["key"]["attr"]}) {{\n{method_code}{tag}}}\n\n'
    return method_str


def __method_admin_select_by_id(config: dict):
    temp1 = ""
    if config.get("fuzzySearch") == "true" and "keyWordList" in config and len(config["keyWordList"]) > 0:
        temp1 = ", null"
    temp2 = ""
    if config.get("SQLInjection") == "true":
        temp2 = ", null"
    tag = "\t"
    method_str = f'{tag}@Override\n'
    method_code = f'{tag * 2}return new {config["extradimensionalData"]["className"]}({stringUtil.low_str_first(config["extradimensionalData"]["javaMapperName"])}.selectOne{config["className"]}(new {config["extradimensionalData"]["className"]}({config["extradimensionalData"]["key"]["attr"]}).to{config["className"]}(){temp1}, 0{temp2}));\n'
    method_str += f'{tag}public {config["extradimensionalData"]["className"]} adminSelect{config["extradimensionalData"]["className"]}By{stringUtil.upper_str_first(config["extradimensionalData"]["key"]["attr"])}({config["extradimensionalData"]["key"]["type"]} {config["extradimensionalData"]["key"]["attr"]}) {{\n{method_code}{tag}}}\n\n'
    return method_str


def __method_select(config: dict):
    tag = "\t"
    method_str = f'{tag}@Override\n'
    temp_sql = ""
    if config.get("SQLInjection") == "true":
        temp_sql = ", null"
    key_word, key_attr, key_str = "", "", ""

    if config["extradimensionalData"].get("fuzzySearch") == "true" and "keyWordList" in config[
        "extradimensionalData"] and len(config["extradimensionalData"]["keyWordList"]) > 0:
        key_word_name = config.get("keyWord")
        if key_word_name is not None:
            key_word_name = key_word_name.strip()
        else:
            key_word_name = "keyWord"
        if key_word_name == "":
            key_word_name = "keyWord"
        key_word = f', String {key_word_name}'
        key_attr = f", {key_word_name}"
        temp_str = f'{tag * 3}{key_word_name} = "%" + {key_word_name} + "%";\n'
        key_str += f'{tag * 2}if ({key_word_name} != null) {{\n{temp_str}{tag * 2}}}\n'
    else:
        key_attr = ", null"
    if config.get("fuzzySearch") == "true" and "keyWordList" in config and len(config["keyWordList"]) > 0:
        pass
    else:
        key_str = ""
        key_attr = ""
    method_code = key_str
    method_code += f'{tag * 2}if (page != null) {{\n{tag * 3}page.setMax({stringUtil.low_str_first(config["extradimensionalData"]["javaMapperName"])}.count{config["className"]}({stringUtil.low_str_first(config["extradimensionalData"]["className"])}.to{config["className"]}(){key_attr}));\n{tag * 2}}}\n'
    method_code += f'{tag * 2}return {config["extradimensionalData"]["className"]}.toList({stringUtil.low_str_first(config["extradimensionalData"]["javaMapperName"])}.select{config["className"]}({stringUtil.low_str_first(config["extradimensionalData"]["className"])}.to{config["className"]}(){key_attr}, page{temp_sql}));\n'
    method_str += f'{tag}public List<{config["extradimensionalData"]["className"]}> select{config["extradimensionalData"]["className"]}({config["extradimensionalData"]["className"]} {stringUtil.low_str_first(config["extradimensionalData"]["className"])}{key_word}, Page page) {{\n{method_code}{tag}}}\n\n'
    return method_str


def __method_admin_select(config: dict):
    tag = "\t"
    method_str = f'{tag}@Override\n'
    temp_sql = ""
    if config.get("SQLInjection") == "true":
        temp_sql = ", null"
    key_word, key_attr, key_str = "", "", ""

    if config["extradimensionalData"].get("fuzzySearch") == "true" and "keyWordList" in config[
        "extradimensionalData"] and len(config["extradimensionalData"]["keyWordList"]) > 0:
        key_word_name = config.get("keyWord")
        if key_word_name is not None:
            key_word_name = key_word_name.strip()
        else:
            key_word_name = "keyWord"
        if key_word_name == "":
            key_word_name = "keyWord"
        key_word = f', String {key_word_name}'
        key_attr = f", {key_word_name}"
        temp_str = f'{tag * 3}{key_word_name} = "%" + {key_word_name} + "%";\n'
        key_str += f'{tag * 2}if ({key_word_name} != null) {{\n{temp_str}{tag * 2}}}\n'
    else:
        key_attr = ", null"
    if config.get("fuzzySearch") == "true" and "keyWordList" in config and len(config["keyWordList"]) > 0:
        pass
    else:
        key_str = ""
        key_attr = ""
    method_code = key_str
    method_code += f'{tag * 2}if (page != null) {{\n{tag * 3}page.setMax({stringUtil.low_str_first(config["extradimensionalData"]["javaMapperName"])}.count{config["className"]}({stringUtil.low_str_first(config["extradimensionalData"]["className"])}.to{config["className"]}(){key_attr}));\n{tag * 2}}}\n'
    method_code += f'{tag * 2}return {config["extradimensionalData"]["className"]}.toList({stringUtil.low_str_first(config["extradimensionalData"]["javaMapperName"])}.select{config["className"]}({stringUtil.low_str_first(config["extradimensionalData"]["className"])}.to{config["className"]}(){key_attr}, page{temp_sql}));\n'
    method_str += f'{tag}public List<{config["extradimensionalData"]["className"]}> adminSelect{config["extradimensionalData"]["className"]}({config["extradimensionalData"]["className"]} {stringUtil.low_str_first(config["extradimensionalData"]["className"])}{key_word}, Page page) {{\n{method_code}{tag}}}\n\n'
    return method_str
