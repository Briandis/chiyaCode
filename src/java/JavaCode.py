from abc import abstractmethod

from src.java.CodeConfig import CodeConfig
from src.util.chiyaUtil import StringUtil

import_dirt = {
    "Date": "java.util.Date",
    "List": "java.util.List",
    "Autowired": "org.springframework.beans.factory.annotation.Autowired",
    "Qualifier": "org.springframework.beans.factory.annotation.Qualifier",
    "Result": "chiya.core.base.result.Result",
    "RestController": "org.springframework.web.bind.annotation.RestController",
    "GetMapping": "org.springframework.web.bind.annotation.GetMapping",
    "PostMapping": "org.springframework.web.bind.annotation.PostMapping",
    "PutMapping": "org.springframework.web.bind.annotation.PutMapping",
    "DeleteMapping": "org.springframework.web.bind.annotation.DeleteMapping",
    "Controller": "org.springframework.stereotype.Controller",
    "ResponseBody": "org.springframework.web.bind.annotation.ResponseBody",
    "JSON": "com.alibaba.fastjson.JSON",
    "Page": "chiya.core.base.page.Page",
    "Service": "org.springframework.stereotype.Service",
    "Mapper": "org.apache.ibatis.annotations.Mapper",
    "Param": "org.apache.ibatis.annotations.Param",
    "RequestMapping": "org.springframework.web.bind.annotation.RequestMapping",
    "BigDecimal": "java.math.BigDecimal",
    "BaseRedisService": "chiya.web.redis.BaseRedisService",
    "ChiyaSecurity": "chiya.security.annotation.ChiyaSecurity",
    "ChiyaRole": "chiya.web.security.entity.ChiyaRole",
    "Repository": "org.springframework.stereotype.Repository"
}


def join(char, *args):
    data = ""
    for string in args:
        if string is not None:
            data += char + string
    return data


def switch_import(attribute_type: str):
    """
    查找是否符合默认的类型配置
    :param attribute_type:属性类型
    :return: 已知的所在路径
    """
    if StringUtil.is_null(attribute_type):
        return None
    start = attribute_type.find("@") + 1
    end = attribute_type.find("(")
    # 对注解类型过滤，得到原类型值
    if end == -1:
        end = None
    attr_type = attribute_type[start:end]
    # 过滤泛型
    end = attr_type.find("<")
    if end == -1:
        end = None
    # 对注解类型过滤，得到原类型值
    attr_type = attr_type[0:end]
    return import_dirt.get(attr_type)


class DefaultMate:
    """
    默认常见的注解
    """

    @staticmethod
    def SuppressWarnings():
        return '@SuppressWarnings("unchecked")'

    @staticmethod
    def Override():
        return "@Override"

    @staticmethod
    def Autowired():
        return "@Autowired"

    @staticmethod
    def Controller():
        return "@Controller"

    @staticmethod
    def ResponseBody():
        return "@ResponseBody"

    @staticmethod
    def Service():
        return "@Service"

    @staticmethod
    def Mapper():
        return "@Mapper"

    @staticmethod
    def Repository():
        return "@Repository"

    @staticmethod
    def Param(value=None):
        if value:
            return f'@Param("{value}")'
        return "@Param"

    @staticmethod
    def ChiyaSecurity(value=None):
        if value:
            return f'@ChiyaSecurity({value})'
        return "@ChiyaSecurity"

    @staticmethod
    def ChiyaRole(value=None):
        if value:
            return f'@ChiyaRole({value})'
        return "@ChiyaRole"

    @staticmethod
    def RequestMapping(*args):
        if args:
            return f'@RequestMapping("{join("/", *args)}")'
        return "@RequestMapping"

    @staticmethod
    def Qualifier(value=None):
        if value:
            return f'@Qualifier("{value}")'
        return "@Qualifier"

    @staticmethod
    def RestController():
        return "@RestController"

    @staticmethod
    def GetMapping(*args):
        if args:
            return f'@GetMapping("{join("/", *args)}")'
        return "@GetMapping"

    @staticmethod
    def PostMapping(*args):
        if args:
            return f'@PostMapping("{join("/", *args)}")'
        return "@PostMapping"

    @staticmethod
    def PutMapping(*args):
        if args:
            return f'@PutMapping("{join("/", *args)}")'
        return "@PutMapping"

    @staticmethod
    def DeleteMapping(*args):
        if args:
            return f'@DeleteMapping("{join("/", *args)}")'
        return "@DeleteMapping"


class Attribute:
    def __init__(
            self,
            attribute_type: str,
            name: str,
            annotation: str = None,
            package: str = None,
            scope: str = "private",
            static: bool = False,
            final: bool = False,
            volatile: bool = False,
    ):
        """
        :param attribute_type:属性类型
        :param name:  属性名称
        :param name:  属性注释信息
        :param package 属性类型所对应的包
        :param scope: 作用域
        :param static 静态变量
        :param final: 常量修饰
        :param volatile: 线程可见
        """
        # 作用域
        self.scope = scope
        # 类型
        self.type = attribute_type
        # 名称
        self.name = name
        # 字段注释
        self.annotation = annotation
        # 是否是静态类
        self.static = static
        # 是否常量
        self.final = final
        # 线程变量可见
        self.volatile = volatile
        # 类型所需要导入的包
        self.import_set = set()
        # 如果导入的包存在，则自动装配
        if not StringUtil.is_null(package):
            self.import_set.add(package)
        self._check_default_import(attribute_type)
        # 注解所引用的包
        self.mate_value = []

    # 添加类注解
    def add_mate(self, value: str, package: str = None):
        """
        添加类的注解
        :param value: 注解的内容
        :param package: 注解所在的包
        :return: 对象自身
        """
        self.mate_value.append(value)
        if package is not None:
            self.import_set.add(package)
        self._check_default_import(value)
        return self

    # 检查类型是否是默认的
    def _check_default_import(self, value: str):
        """
        检查默认的配置中，有无这个对象的引用地址
        :param value: 对象的类型
        :return: 默认中存在的地址
        """
        # 默认注解中加入的值进行装配
        import_what = switch_import(value)
        if import_what is not None:
            self.import_set.add(import_what)

    # 构建文本信息
    def create(self, indentation: int = 1):
        """
        构建文本信息
        :param indentation: 缩进的函数
        :return: 属性文本信息
        """
        indent = '\t' * indentation
        static = ""
        final = ""
        volatile = ""
        scope = ""
        if self.volatile:
            volatile = "volatile "
        if self.static:
            static = "static "
            if self.final:
                final = "final "
        if self.scope is not None:
            scope = self.scope + " "
        data = ""
        if self.annotation is not None:
            data += f'{indent}/** {self.annotation} */\n'
        for i in self.mate_value:
            data += f'{indent}{i}\n'

        data += f'{indent}{scope}{volatile}{static}{final}{self.type} {self.name};\n'
        return data


class DefaultAttribute:
    """
    默认的属性
    """
    ReturnBoolean = Attribute("boolean", "b", "true:成功/false:失败")
    """
    返回布尔类型
    """
    Page = Attribute("Page", "page", f'分页对象')
    """
    分页对象
    """
    Result = Attribute("Result", "result", "Result 业务对象")
    """
    Result 业务对象
    """
    MapperInteger = Attribute("Integer", "integer", "受影响行数")
    """
    Mapper的受影响行数
    """

    @staticmethod
    def self_class(config: CodeConfig):
        """
        获取自身的类型
        :param config:配置文件
        :return: 自身对象
        """
        return Attribute(config.module.entity.className, config.module.entity.low_name(), f'{config.module.entity.remark}对象')

    @staticmethod
    def self_key(config: CodeConfig):
        """
        获取自身主键
        :param config:配置文件
        :return: 主键对象
        """
        return Attribute(config.baseInfo.key.type, config.baseInfo.key.attr, f'{config.module.entity.remark}的{config.baseInfo.key.attr}')

    @staticmethod
    def self_list_class(config: CodeConfig):
        """
        获取自身的列表类型
        :param config:配置文件
        :return: 自身对象
        """
        return Attribute(f'List<{config.module.entity.className}>', f'list{config.module.entity.className}', f'{config.module.entity.remark}对象列表')

    @staticmethod
    def get_service(config: CodeConfig):
        """
        获取service层的作为属性
        :param config: 配置文件
        :return: 业务层属性
        """
        return Attribute(
            config.module.serviceInterface.className,
            config.module.serviceInterface.low_name(),
            f'{config.module.entity.remark}业务接口',
            config.module.serviceInterface.get_package(),
        ).add_mate(DefaultMate.Autowired()).add_mate(DefaultMate.Qualifier(config.module.serviceImplements.low_name()))

    @staticmethod
    def get_domain(config: CodeConfig):
        """
        获取domain层的作为属性
        :param config: 配置文件
        :return: 业务层属性
        """
        return Attribute(
            config.module.domain.className,
            config.module.domain.low_name(),
            f'{config.module.entity.remark}领域层接口',
            config.module.domain.get_package(),
        ).add_mate(DefaultMate.Autowired()).add_mate(DefaultMate.Qualifier(config.module.domainImpl.low_name()))

    @staticmethod
    def get_repository(config: CodeConfig):
        """
        获取repository层的作为属性
        :param config: 配置文件
        :return: 业务层属性
        """
        return Attribute(
            config.module.repository.className,
            config.module.repository.low_name(),
            f'{config.module.entity.remark}仓库层接口',
            config.module.repository.get_package(),
        ).add_mate(DefaultMate.Autowired()).add_mate(DefaultMate.Qualifier(config.module.repositoryImpl.low_name()))

    @staticmethod
    def get_mapper(config: CodeConfig):
        """
        获取repository层的作为属性
        :param config: 配置文件
        :return: 业务层属性
        """
        return Attribute(
            config.module.mapperInterface.className,
            config.module.mapperInterface.low_name(),
            f'{config.module.entity.remark}mapper层',
            config.module.mapperInterface.get_package(),
        ).add_mate(DefaultMate.Autowired())


class FunctionBody:
    def __init__(self):
        self.indentation = 0
        # 代码块字符串
        self.java_code = []

    @abstractmethod
    def function_body(self, parameter: list[Attribute]):
        """
        方法处理
        :param parameter 传入的参数list[Attribute]
        """
        pass

    def create_code(self):
        """
        生成代码块
        :return: 代码块字符串
        """
        data = ""
        for i in self.java_code:
            data += i
        return data

    def line(self, data: str):
        """
        写入一行
        :param data: 一行内容
        """
        indent = '\t' * self.indentation
        self.java_code.append(f'{indent}{data}\n')

    def indent_add(self, data: str):
        """
        增加缩进
        """
        self.indentation = self.indentation + 1
        self.line(data)

    def indent_sub(self, data: str):
        """
        减少缩进
        """
        self.indentation = self.indentation - 1
        self.line(data)

    def line_foreach(self, variable: str, lists: str):
        """
        增加foreach迭代代码块
        :param variable: 迭代自变量
        :param lists: 迭代的列表
        """
        self.line(f'for ({variable} : {lists}) {{')
        self.indentation = self.indentation + 1

    def line_if(self, data: str):
        """
        增加if代码块行
        :param data:表达式
        """
        self.line(f'if ({data}) {{')
        self.indentation = self.indentation + 1

    def block_end(self):
        """
        代码块结束
        """
        self.indent_sub("}")

    def line_annotation(self, data: str):
        """
        增加一行注释
        :param data: 注释
        """
        if data is None:
            data = ""
        self.line(f'// {data}')

    def line_todo(self, data="后续行为编写"):
        self.line_annotation(f'TODO: {data}')

    def line_blank(self):
        """
        增加一行空行
        """
        self.line("")

    def line_if_one_block(self, if_value: str, data: str = ""):
        """
        单行if块块
        :param if_value: if条件
        :param data: 做什么操作
        """
        self.line(f'if ({if_value}) {{ {data} }}')


class Function:
    def __init__(
            self,
            scope: str,
            result: Attribute,
            name: str,
            annotation: str = None,
            *parameter: Attribute
    ):
        """
        :param scope:方法作用域，如为None，则默认无
        :param result: 返回值类型，如果为None，则返回void类型
        :param name: 方法名称
        :param annotation 方法注释
        :param parameter: 方法参数
        """
        # 作用域
        self.scope = scope
        #
        self.result = result
        # 名称
        self.name = name
        # 字段注释
        self.annotation = annotation
        # 方法体内容
        self.functionBody = None
        # 类型所需要导入的包
        self.import_set = set()
        # 注解所引用的包
        self.mate_value = []
        # 提交的参数
        self.parameter = []
        for i in parameter:
            if i is not None:
                self.parameter.append(i)
        # 是否是接口
        self.is_interface = False
        # 其他类型，则将类型信息装入对象中
        if self.result is not None:
            for i in self.result.import_set:
                self.import_set.add(i)
        # 参数类型导入赋值
        if self.parameter is not None:
            for i in self.parameter:
                for j in i.import_set:
                    self.import_set.add(j)

    # 添加参数
    def add_parameter(self, parameter: Attribute):
        """
        添加参数
        :param parameter: 属性对象
        :return: 自身
        """
        if parameter is None:
            return self
        self.parameter.append(parameter)
        for i in parameter.import_set:
            self.import_set.add(i)
        return self

    # 添加类注解
    def add_mate(self, value: str, package: str = None):
        """
        添加类的注解
        :param value: 注解的内容
        :param package: 注解所在的包
        :return: 对象自身
        """
        self.mate_value.append(value)
        if package is not None:
            self.import_set.add(package)
        self._check_default_import(value)
        return self

    def add_body(self, function: FunctionBody):
        """
        方法中的内容
        :param function:方法处理函数
        :return: 自身
        """
        self.functionBody = function
        return self

    def set_is_interface(self):
        """
        声明该方法是个接口
        :return: 自身
        """
        self.is_interface = True
        return self

    # 检查类型是否是默认的
    def _check_default_import(self, value: str):
        """
        检查默认的配置中，有无这个对象的引用地址
        :param value: 对象的类型
        :return: 默认中存在的地址
        """
        # 默认注解中加入的值进行装配
        import_what = switch_import(value)
        if import_what is not None:
            self.import_set.add(import_what)

    # 构造方法内容
    def _create_function(self, indentation=1):
        """
        构造方法内容
        :param indentation: 缩进
        :return: 方法内容字符串
        """
        indent = '\t' * indentation
        data = ""
        scope = ""
        if self.scope is not None:
            scope = self.scope + " "
        result = "void "
        if self.result is not None:
            result = self.result.type + " "

        data += f'{indent}{scope}{result}{self.name}('
        if self.parameter is not None:
            lists = []
            for param in self.parameter:
                lists.append(f'{param.type} {param.name}')
            data += StringUtil.string_join(", ", *lists)
        data += f') {{\n'
        if self.functionBody is not None:
            self.functionBody.indentation = indentation + 1
            self.functionBody.function_body(self.parameter)
            data += self.functionBody.create_code()
        data += f'{indent}}}\n'
        return data

    # 构造接口方法
    def _create_interface(self, indentation=1):
        """
        构造接口方法
        :param indentation: 缩进
        :return: 方法内容字符串
        """
        indent = '\t' * indentation
        data = ""
        result = "void "
        if self.result is not None:
            result = self.result.type + " "

        data += f'{indent}{result}{self.name}('
        if self.parameter is not None:
            lists = []
            count_len = 0
            for param in self.parameter:
                param_str = f'{param.type} {param.name}'
                lists.append(param_str)
                count_len += len(param_str)
            # 如果字符串大于85，则需要换行展示
            if count_len > 85:
                param_indent = '\t' * (indentation + 1)
                count = 0
                data += f'\n'
                for i in lists:
                    if count + 1 == len(lists):
                        data += f'{param_indent}{i}\n'
                    else:
                        data += f'{param_indent}{i},\n'
                    count += 1
                data += f'{indent}'
            else:
                data += StringUtil.string_join(", ", *lists)
        data += f');\n'
        return data

    # 构建注解代码段
    def _create_mate(self, indentation=1):
        """
        构建注解代码段
        :param indentation: 缩进
        :return: 注解代码段
        """
        indent = '\t' * indentation
        data = ""
        for i in self.mate_value:
            data += f'{indent}{i}\n'
        return data

    # 构建方法注释
    def _create_annotation(self, indentation=1):
        """
        构建方法注释块
        :param indentation:缩进
        :return: 注释字符串
        """
        indent = '\t' * indentation
        data = "\n"
        # 注释块
        data += f'{indent}/**\n'
        flag = True
        if self.annotation:
            data += f'{indent} * {self.annotation}\n'
            flag = False
        # 参数
        if self.parameter is not None and len(self.parameter) > 0:
            flag = False
            space = 0
            # 招到字符的最大值
            for param in self.parameter:
                i = len(param.name)
                if i > space:
                    space = i

            data += f'{indent} * \n'
            for param in self.parameter:
                if param.annotation:
                    data += f'{indent} * @param {param.name}{" " * (space - len(param.name))} {param.annotation}\n'
                else:
                    data += f'{indent} * @param {param.name}{" " * (space - len(param.name))} {param.name}\n'
        # 返回值
        if self.result is not None:
            flag = False
            data += f'{indent} * @return {self.result.annotation}\n'
        data += f'{indent} */\n'
        if flag:
            return "\n"
        return data

    # 构造方法代码块
    def create(self, indentation=1):
        """
        构造方法代码块
        :param indentation: 缩进
        :return: 方法代码块
        """
        data = ""
        data += self._create_annotation(indentation)
        data += self._create_mate(indentation)
        if self.is_interface:
            # 接口的情况
            data += self._create_interface(indentation)
        else:
            # 普通的方法
            data += self._create_function(indentation)
        return data


class JavaCode:
    def __init__(self, package: str, class_name: str, annotation: str = None):
        """
        初始化方法
        :param package:包所在路径，允许为空
        :param class_name: 类名
        :param annotation: 类注释
        """
        # 包
        self.package = package
        # 类名
        self.class_name = class_name
        # 注释
        self.annotation = annotation
        # 导入的包
        self.import_set = set()
        # 类上加载的注解
        self.mate_value = []
        # 是否是类
        self.is_class = True
        # 是否是抽象类
        self.is_abstract = False
        # 属性列表
        self.attribute: [Attribute] = []
        # 方法列表
        self.function: [Function] = []
        # 继承的类型
        self.extends: [Attribute] = []
        # 实现的类
        self.implements: [Attribute] = []

    # 添加类的继承关系
    def add_extend(self, attr: Attribute):
        """
        添加类的继承关系
        :param attr:属性对象
        :return: Node
        """
        if attr is None:
            return
        self.extends.append(attr)
        for i in attr.import_set:
            self.add_import(i)

    # 添加类的实现关系
    def add_implement(self, attr: Attribute):
        """
        添加类的实现关系
        :param attr:属性对象
        :return: Node
        """
        if attr is None:
            return
        self.implements.append(attr)
        for i in attr.import_set:
            self.add_import(i)

    # 添加类的属性
    def add_attr(self, attr: Attribute):
        """
        添加对应的属性
        :param attr:属性对象
        :return: Node
        """
        if attr is None:
            return
        self.attribute.append(attr)
        for i in attr.import_set:
            self.add_import(i)

    def get_attr_name(self, index):
        """
        获取属性的名称
        :param index: 下标
        :return:
        """
        return self.attribute[index].name

    # 添加类中的方法
    def add_function(self, function: Function):
        """
        添加方法
        :param function:
        :return:
        """
        if function is None:
            return
        self.function.append(function)
        for i in function.import_set:
            self.add_import(i)

    # 添加导入的包
    def add_import(self, package: str):
        """
        添加导入的包
        :param package:包路径
        :return: None
        """
        if package is None:
            return
        finds = package.rsplit(".", 1)
        # 如果引入的跑所在的目录相同，则不引入
        if finds[0] != self.package:
            self.import_set.add(package)

    # 添加类注解
    def add_mate(self, value: str, package: str = None):
        """
        添加类的注解
        :param value: 注解的内容
        :param package: 注解所在的包
        :return: None
        """
        self.mate_value.append(value)
        if package is not None:
            self.import_set.add(package)
        self._check_default_import(value)

    # 打开当前包
    def _create_packet(self):
        """
        打开当前包
        :return: package xxx.xxx\n;
        """
        data = ""
        # 如果包不为空，则导入当前所在文件夹的包
        if not StringUtil.is_null(self.package):
            data += f'package {self.package};\n'
        return data

    # 构建导包
    def _create_import(self):
        """
        构建导包
        :return:字符串
        """
        lists = list(self.import_set)
        lists.sort()
        data = "\n"
        for i in lists:
            data += f'import {i};\n'
        return data

    # 创建类注解
    def _create_mate(self):
        data = ""
        for i in self.mate_value:
            data += f'{i}\n'
        return data

    # 创建类注释
    def _create_annotation(self):
        data = '\n'
        if self.annotation:
            data += f'/**\n'
            data += f' * {self.annotation}\n'
            data += f' */\n'
        return data

    # 构造类头信息
    def _create_class(self):
        """
        构造类头信息
        :return: 类头信息文本
        """
        data = f'public interface {self.class_name}'
        if self.is_class:
            i = ""
            if self.is_abstract:
                i = " abstract"
            data = f'public{i} class {self.class_name}'
        if len(self.extends) > 0:
            data += f' extends'
            for i in self.extends:
                data += f' {i.type}'
        if len(self.implements) > 0:
            data += f' implements'
            for i in self.implements:
                data += f' {i.type}'
        data += f' {{\n'
        return data

    # 构建属性信息
    def _create_attribute(self):
        """
        构建属性信息
        :return: 属性的字符串
        """
        data = ""
        for attr in self.attribute:
            data += attr.create()
        return data

    # 构建方法信息
    def _create_function(self):
        """
        构建方法信息
        :return: 方法的字符串
        """
        data = ""
        for attr in self.function:
            data += attr.create()
        return data

    @staticmethod
    def _create_class_end():
        return f"}}\n"

    def _check_default_import(self, value: str):
        """
        检查默认的配置中，有无这个对象的引用地址
        :param value: 对象的类型
        :return: 默认中存在的地址
        """
        # 默认注解中加入的值进行装配
        import_what = switch_import(value)
        if import_what is not None:
            self.import_set.add(import_what)

    def create(self):
        """
        构建文件内容
        :return: 文件中的代码
        """
        data = ""
        data += self._create_packet()
        data += self._create_import()
        data += self._create_annotation()
        data += self._create_mate()
        data += self._create_class()
        data += self._create_attribute()
        data += self._create_function()
        data += self._create_class_end()
        return data
