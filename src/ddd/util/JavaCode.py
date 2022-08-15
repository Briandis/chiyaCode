from src.util import StringUtil

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
    "RequestMapping": "org.springframework.web.bind.annotation.RequestMapping"
}


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
        if self.volatile:
            volatile = " volatile"
        if self.static:
            static = " static"
            if self.final:
                final = " final"
        data = ""
        if self.annotation is not None:
            data += f'{indent}/** {self.annotation} */\n'
        for i in self.mate_value:
            data += f'{indent}{i}\n'
        data += f'{indent}{volatile}{self.scope}{static}{final} {self.type} {self.name};\n'
        return data


class Function:
    def __init__(
            self,
            scope: str,
            result: Attribute,
            name: str,
            annotation: str = None,
            **parameter: Attribute
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
        # 类型所需要导入的包
        self.import_set = set()
        # 注解所引用的包
        self.mate_value = []
        # 提交的参数
        self.parameter = parameter
        # 其他类型，则将类型信息装入对象中
        if self.result is not None:
            for i in self.result.import_set:
                self.import_set.add(i)

    # 添加参数
    def add_parameter(self):
        pass

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

    # 构造文件对象
    def create(self):
        pass


class JavaCode:
    def __init__(self, package: str, class_name: str, annotation: str):
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
        self.attribute = []

    # 添加类的属性
    def add_attr(self, attr: Attribute):
        """
        添加对应的属性
        :param attr:属性对象
        :return: Node
        """
        self.attribute.append(attr)
        for i in attr.import_set:
            self.add_import(i)

    # 添加类中的方法
    def add_function(self):
        pass

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
            data += f'{i};\n'
        return data

    # 创建类注释
    def _create_annotation(self):
        data = '\n'
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
        data = f'public interface {self.class_name} {{\n'
        if self.is_class:
            i = ""
            if self.is_abstract:
                i = " abstract"
            data = f'public{i} class {self.class_name} {{\n'
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
        data += self._create_class_end()
        return data
