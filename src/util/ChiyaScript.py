import re
import uuid
from typing import List, Dict, Tuple


class LoggerUtil:

    @staticmethod
    def padding(list_data, padding_count=None, padding=" "):
        """
        填充字符串
        :param list_data:字符串列表
        :param padding_count: 填充的数量
        :param padding: 填充字符
        :return: 字符
        """
        if padding_count is None:
            padding_count = []
        result = ""
        index = 0
        for string in list_data:
            string = f'{string}'
            size = 0
            if len(padding_count) > index:
                size = padding_count[index] - len(string)
                if size < 0:
                    size = 0
            result += string + padding * size
            index += 1
        return result


class Variable:
    def __init__(self):
        """
        变量
        """
        self.user = {}
        """ 用户变量空间 """
        self.system = {}
        """ 系统匿名空间 """

    def __str__(self):
        return self.user.__str__()


class VariableSystem:

    def __init__(self):
        """
        变量系统
        """
        self.variable: List[Variable] = []
        """ 变量 """
        self.variable_set_stack = []
        """ 变量赋值栈 """
        self.variable_get_stack = []
        """ 变量获取栈 """

    def set_system_variable(self, is_global: bool, key, value=None):
        """
        存储变量
        :param is_global:是否是全局变量
        :param key: 变量名称
        :param value: 值
        """
        if len(self.variable) == 0:
            self.variable.append(Variable())
        stack_frame = 0 if is_global else -1
        self.variable[stack_frame].system[key] = value

    def set_variable(self, is_global: bool, key, value=None):
        """
        存储变量
        :param is_global:是否是全局变量
        :param key: 变量名称
        :param value: 值
        """
        if len(self.variable) == 0:
            self.variable.append(Variable())
        stack_frame = 0 if is_global else -1
        self.variable[stack_frame].user[key] = value

    def set_global_variable(self, *data):
        """
        设置全局变量
        :param data:变量信息
        """
        if len(data) > 1:
            self.set_variable(True, data[0], data[1])
        if len(data) == 1:
            self.variable_set_stack.append((True, data[0]))

    def load_local_variable(self, data: dict):
        """
        加载局部变量
        :param data: 字典树
        """
        for field, value in data.items():
            self.set_variable(False, field, value)

    def set_local_variable(self, *data):
        """
        设置局部变量
        :param data:变量信息
        """
        if len(data) > 1:
            self.set_variable(False, data[0], data[1])
        if len(data) == 1:
            self.variable_set_stack.append((False, data[0]))

    def get_global_variable(self, *data):
        """
        获取全局变量
        :param data: 获取变量
        """
        if len(data) > 0:
            self.variable_get_stack.append((True, data))

    def get_local_variable(self, *data):
        """
        获取局部变量
        :param data: 获取变量
        """
        if len(data) > 0:
            self.variable_get_stack.append((False, data))

    def get(self, name, is_global=False):
        """
        获取var对象
        :param name:变量名称
        :param is_global:是否是全局变量
        """
        if is_global:
            if len(self.variable) > 0:
                if name in self.variable[0].user:
                    return self.variable[0].user[name]
        else:
            for stack_variable in self.variable[::-1]:
                if name in stack_variable.user:
                    return stack_variable.user[name]
        raise KeyError(f'尚未定义变量{name}')

    def check_not_self_function(self, function):
        """
        检查是否为自身的方法
        :param function:方法
        :return True：不是，false:是
        """
        return function not in [self.get_global_variable, self.get_local_variable, self.set_global_variable, self.set_local_variable]

    def get_pop(self, function, param):
        """
        获取栈的出栈
        :param function:当前执行的方法
        :param param:参数
        """
        if len(self.variable_get_stack) > 0 and self.check_not_self_function(function):
            while len(self.variable_get_stack) > 0:
                index = len(self.variable_get_stack) - 1
                is_global, data = self.variable_get_stack.pop()
                if len(data) > 1:
                    index = int(data[1]) - 1

                if len(param) <= index:
                    # 如果参数少，扩增参数
                    for i in range(index - len(param) + 1):
                        param.append(None)
                param[index] = self.get(data[0], is_global)

    def call_set(self, function):
        """
        执行方法后设置值
        :param function:方法
        :return: 回调
        """
        if len(self.variable_set_stack) > 0 and self.check_not_self_function(function):
            stack_variable, set_data = self.variable_set_stack.pop()

            def call(data):
                self.set_variable(stack_variable, set_data, data)

            return call
        return None

    def function_set_param(self, param):
        """
        接收方法参数至局部变量
        :param param:参数
        """
        if "param" not in self.variable[-1].system:
            raise ValueError(f"调用方法缺少参数{param}")
        function_param = self.variable[-1].system["param"]
        data = None
        if len(function_param) > 0:
            data = function_param.pop()
        self.set_variable(False, param, data)

    def function_return(self, param):
        """
        方法返回
        :param param:参数
        """
        if len(self.variable) > 1:
            if "return" not in self.variable[-2].system:
                self.variable[-2].system["return"] = []
            self.variable[-2].system["return"].append(self.get(param))

    def function_get_return(self, param):
        """
        获取方法返回
        :param param:参数
        """
        if "return" not in self.variable[-1].system:
            raise ValueError(f"方法没有接收到返回值{param}")
        if len(self.variable) > 1:
            data = self.variable[-1].system["return"].pop()
            self.set_variable(False, param, data)


class Command:

    def __init__(self, function, param: list | tuple | None, source_code: str | None, line: int, param_index: tuple | list | None):
        """
        指令
        :param function: 映射的方法
        :param param: 参数
        :param source_code:源码
        :param line: 源码行数
        :param param_index:参数映射的位置
        """
        self.line = line
        """ 当前行数 """
        self.function = function
        """ 映射的方法 """
        self.param = param
        """ 映射方法的参数 """
        self.source_code = source_code
        """ 源码 """
        self.param_index = param_index
        """ 参数映射位置 """

    def execute(self, variable_system: VariableSystem, logger=None):
        """
        执行命令
        :param variable_system:变量系统
        :param logger:日志
        """
        if logger is None:
            logger = []
        # 定义返回操作
        call_set = variable_system.call_set(self.function)
        # 有参数的情况下
        if self.param is None:
            logger.append(None)
            result = self.function()
        else:
            if self.param_index is None:
                param = [*self.param]
            else:
                param = []
                # 参数转换
                for index in self.param_index:
                    param.append(self.param[index - 1])
            # 从变量栈中获取值，并且对参数进替换，只有在该执行方法不同的情况下
            variable_system.get_pop(self.function, param)
            logger.append(param)
            # 执行
            result = self.function(*param)

        if call_set is not None:
            logger.append(result)
            call_set(result)


class CommandFunction:

    def __init__(self, command, old_command, function, parameter_index):
        """
        命令映射的方法
        :param command:指令
        :param old_command:映射前指令
        :param function: 方法
        :param parameter_index:映射下标
        """
        self.command = command
        """ 指令 """
        self.old_command = old_command
        """ 映射前指令 """
        self.param_index = parameter_index
        """ 参数所映射的下标 """
        self.function = function
        """ 执行的方法 """


class ScriptKeyword:
    def __init__(self):
        """
        脚本关键字
        """
        self.code_start = []
        """ 模块开始 """
        self.code_end = []
        """ 模块结束 """
        self.call_script = []
        """ 调用其他模块 """
        self.note_line = []
        """ 单行注释符号 """
        self.note_multiple = []
        """ 多行注释符号 """
        self.set_global_variable = []
        """ 全局变量声明 """
        self.get_global_variable = []
        """ 全局变量获取 """
        self.set_local_variable = []
        """ 局部变量声明 """
        self.get_local_variable = []
        """ 局部变量获取 """
        self.load_local_variable = []
        """ 加载局部变量 """
        self.if_block = []
        """ 分支控制 """
        self.else_block = []
        """ 否则处理块 """
        self.end_if = []
        """ 结束分支块 """
        self.function_param = []
        """ 方法声明接收参数 """
        self.function_return = []
        """ 方法返回的参数 """
        self.function_get_return = []
        """ 获取方法返回 """

        self.loop_start = []
        """ 循环开始 """
        self.loop_end = []
        """ 循环结束 """
        self.jump_loop = []
        """ 跳出循环 """
        self.loop_break = []
        """ 终止循环 """


class CommandBlock:
    def __init__(self, name):
        """
        编译的代码块
        :param name:名称
        """
        self.name = name
        """ 名称 """
        self.command_list: List[Command] = []
        """ 指令 """

    def append(self, command: Command):
        """
        添加指令
        :param command:指令
        """
        self.command_list.append(command)

    def size(self) -> int:
        """
        获取指令长度
        :return:
        """
        return len(self.command_list)

    def get(self, index):
        """
        获取指令
        :param index:下标
        :return:
        """
        return self.command_list[index]


class CompileStack:

    def __init__(self):
        """
        编译栈
        """
        self.root = CommandBlock("root")
        """ 根节点 """
        self.stack: List[CommandBlock] = [self.root]
        """ 栈 """

    def append(self, data: CommandBlock):
        """
        添加栈
        :param data:代码
        """
        self.stack.append(data)

    def pop(self) -> CommandBlock:
        """
        出栈
        :return: 指令模块
        """
        return self.stack.pop()

    def add(self, name: str):
        """
        添加一个新模板
        :param name: 模块名称
        """
        self.stack.append(CommandBlock(self.stack[-1].name + name))

    def size(self) -> int:
        """
        获取大小
        :return:栈大小
        """
        return len(self.stack)

    def get_call_name(self, name) -> tuple:
        """
        获取调用模块名称
        :param name:调用的模块
        :return:
        """
        call_module = (f'{self.root.name}.{name}',)
        return call_module

    def __getitem__(self, item):
        return self.stack[item]

    def __setitem__(self, item, data):
        self.stack[item] = [data]


class RuntimeModule:

    def __init__(self, name, command_block: CommandBlock):
        """
        运行时模块信息
        :param name:名称
        :param command_block: 代码块
        """
        self.name = name
        """ 模块名称 """
        self.program_counter = 0
        """ 当前模块程序计数器 """
        self.command_block = command_block
        """ 当前指令模块 """

    def goto(self, program_counter):
        """
        指令跳转至
        :param program_counter:跳转的指令
        """
        self.program_counter = program_counter

    def last_command(self) -> Command | None:
        """
        上一条指令
        :return:指令
        """
        last = self.program_counter - 1 if self.program_counter > 0 else 0
        return self.command_block.get(last)

    def next(self) -> Command | None:
        """
        下一条指令
        :return:指令
        """
        if self.program_counter >= self.command_block.size():
            return None
        command = self.command_block.get(self.program_counter)
        self.program_counter += 1
        return command

    def now_command(self) -> Command | None:
        """
        获取当前指令
        :return: 指令
        """
        return self.command_block.get([self.program_counter])


class RuntimeStack:
    def __init__(self, command_block: CommandBlock, runtime_stack_size=10):
        """
        运行栈
        :param command_block:主方法代码块
        :param runtime_stack_size: 栈大小
        """
        self.root = RuntimeModule("main", command_block)
        """ 根节点 """
        self.stack: List[RuntimeModule] = [self.root]
        """ 运行栈 """
        self.runtime_stack_size = runtime_stack_size
        """ 运行时栈帧上限 """

    def size(self) -> int:
        """
        获取大小
        :return:栈大小
        """
        return len(self.stack)

    def append(self, module: RuntimeModule):
        """
        添加运行时数据
        :param module:模块
        """
        if self.size() > self.runtime_stack_size:
            raise OverflowError(f"栈溢出！！！请检查脚本是否存在递归！栈大小：{self.runtime_stack_size}")
        self.stack.append(module)

    def pop(self) -> RuntimeModule:
        """
        出栈
        :return: 指令模块
        """
        return self.stack.pop()

    def now_runtime_module(self) -> RuntimeModule:
        """
        获取当前最后一个模块
        :return:
        """
        return self.stack[-1]

    def next(self) -> Tuple[Command, RuntimeModule]:
        """
        获取吓一跳命令，回自动出栈
        :return:
        """
        command_module = self.now_runtime_module()
        # 栈中指令为空则出栈
        command = command_module.next()
        if command is None:
            self.stack.pop()
        return command, command_module

    def get_stack_info(self):
        """
        获取当前栈执行信息
        """
        script_stack = []
        for runtime_module in self.stack:
            error_data = [runtime_module.name, runtime_module.program_counter - 1, runtime_module.last_command().source_code, ]
            script_stack.append(LoggerUtil.padding(error_data, [18, 8]))
        return script_stack

    def reset(self):
        """
        重置栈
        """
        self.stack.clear()
        self.root.program_counter = 0
        self.stack.append(self.root)

    def goto(self, program_counter):
        """
        当前模块跳转至下一个指令
        :param program_counter:跳转的指令
        """
        self.now_runtime_module().goto(program_counter)


class CompileFlag:
    def __init__(self):
        """
        编译检查点
        """
        self.is_note_multiple = False
        """ 是多行注释 """
        self.if_block_stack = []
        """ 分支快栈 """
        self.loop_block_stack = []
        """ 循环分支块 """


class CodeScript:

    def __init__(self):
        """
        脚本核心
        """
        self.command_map: Dict[str, CommandFunction] = {}
        """ 指令 """
        self.system_command: Dict[str, CommandFunction] = {}
        """ 系统指令 """

        self._placeholder = "\\{(\\d*?)\\}"
        """ 占位符 """
        self.script_keyword = ScriptKeyword()
        """ 关键字 """

        self.compile_stack: CompileStack = CompileStack()
        """ 编译栈 """
        self.script_module: Dict[str, CommandBlock] = {self.compile_stack.root.name: self.compile_stack.root}
        """ 脚本模块 """
        self.runtime_stack: RuntimeStack = RuntimeStack(self.compile_stack.root)
        """ 运行时栈帧 """
        self._compile_flag = CompileFlag()
        """ 编译用到的检查点 """
        self.variable = VariableSystem()
        """ 变量 """

    @staticmethod
    def _find_command(line_code, command_list):
        """
        查找改行对应的指令
        :param line_code:脚本一行
        :param command_list:指令列表
        :return:找到的指令
        """
        match = []
        # 指令匹配
        if command_list is None:
            return None
        # 直接传入指令
        if isinstance(command_list, str):
            if re.search(command_list, line_code):
                match.append(command_list)
        else:
            # 指令列表的情况
            for command in command_list:
                if command is None:
                    continue
                if re.search(command, line_code):
                    match.append(command)
        if len(match) == 0:
            return None
        command = match[0]
        if len(match) > 1:
            for i in range(len(match)):
                for j in range(i, len(match)):
                    if len(match[i]) > len(match[j]):
                        match[i], match[j] = match[j], match[i]
            command = match[-1]
        return command

    @staticmethod
    def _command_param(command, script_line):
        """
        解析指令对应的参数
        :param command: 指令
        :param script_line:脚本单行
        :return: 参数
        """
        params = re.findall(command, script_line)[0]
        if params == script_line:
            params = None
        if isinstance(params, str):
            params = (params,)
        return params

    def _load_module(self, module_name: str):
        """
        加载模块
        :param module_name:模块名称
        """
        module_code = self.script_module.get(module_name)
        if module_code is None:
            raise ImportError(f'{module_name}模块在脚本中不存在')
        return module_code

    def _call_module(self, module_name: str, *param):
        """
        调用并执行某个模块
        :param module_name:模块名称
        :param param:参数
        """
        module_code = self._load_module(module_name)
        # 运行栈添加信息
        self.runtime_stack.append(RuntimeModule(module_name, module_code))
        # 变量栈添加信息
        variable = Variable()
        if param is not None:
            variable.system["param"] = list(param)
        self.variable.variable.append(variable)

    def _return_call_module(self):
        """
        模块调用结束
        """
        self.runtime_stack.pop()
        # 变量栈出栈
        self.variable.variable.pop()

    @staticmethod
    def _character_escape(command, need_escape=None):
        """
        字符转义
        :param command:指令
        :param need_escape:转义的字符
        :return:转义后的指令
        """
        if need_escape is None:
            need_escape = [".", "(", ")", "{", "}", "?", "*", "+", "[", "]"]
        for char in need_escape:
            command = command.replace(char, f'\\{char}')
        return command

    def register_placeholder(self, placeholder_start, placeholder_end):
        """
        注冊佔位符
        :param placeholder_start:起始占位符
        :param placeholder_end:结束占位符
        """
        self._placeholder = self._character_escape(placeholder_start)
        self._placeholder += "(\\d*?)"
        if placeholder_end is not None:
            self._placeholder += self._character_escape(placeholder_end)

    def _command_replace(self, command):
        """
        指令转义替换
        :param command: 命令
        """
        if command is None:
            return None

        param_index = re.findall(self._placeholder, command)
        new_params = []
        if len(param_index) > 0:
            index = 0
            for char in param_index:
                index += 1
                if char == "":
                    new_params.append(index)
                else:
                    new_params.append(int(char))
        command = re.sub(self._placeholder, "|<TEMP_PLACEHOLDER>|", command)
        command = self._character_escape(command)
        command = command.replace("|<TEMP_PLACEHOLDER>|", "(.*?)")
        return f'^{command}$', new_params

    def _collection_add(self, collection, data):
        """
        集合添加数据
        :param collection: 要添加的集合
        :param data: 添加的数据
        """
        if isinstance(data, str):
            data = (data,)
        for item in data:
            command, param_index = self._command_replace(item)
            collection.append(command)

    def _check_placeholder(self, data, count=1):
        """
        检查占位符
        :param data:数据
        :param count:检查占位符的数量
        """
        if isinstance(data, str):
            data = (data,)
        for item in data:
            find_count = re.findall(self._placeholder, item)
            if len(find_count) < count:
                raise ValueError(f'注册的指令【{item}】至少需要【{count}】个占位符')

    def register_loop_start(self, commands, function):
        """
        定义循环开始命令
        :param commands:命令
        :param function:循环函数
        """
        self._check_placeholder(commands, 1)
        self._collection_add(self.script_keyword.loop_start, commands)
        # 同时注册指令
        self.register_system_command(commands, function)

    def register_loop_end(self, *commands):
        """
        定义循环结束命令
        :param commands:命令
        """
        self._collection_add(self.script_keyword.loop_end, commands)

    def register_jump_loop(self, *commands):
        """
        定义跳出循环命令
        :param commands:命令
        """
        self._collection_add(self.script_keyword.jump_loop, commands)

    def register_loop_break(self, *commands):
        """
        定义终止循环命令
        :param commands:命令
        """
        self._collection_add(self.script_keyword.loop_break, commands)

    def register_start_block(self, *block_start):
        """
        定义代码块开始
        :param block_start:脚本模块起始
        """
        self._check_placeholder(block_start, 1)
        self._collection_add(self.script_keyword.code_start, block_start)

    def register_end_block(self, *block_end):
        """
        定义代码结束
        :param block_end: 脚本模块结束
        """
        self._collection_add(self.script_keyword.code_end, block_end)

    def register_invoke(self, *invoke_command):
        """
        注册调用命令
        :param invoke_command:调用命令
        """
        self._check_placeholder(invoke_command, 1)
        self._collection_add(self.script_keyword.call_script, invoke_command)

    def register_note_line(self, *data):
        """
        注册单行注释
        :param data:调用命令
        """
        self._check_placeholder(data, 1)
        self._collection_add(self.script_keyword.note_line, data)

    def register_note_multiple(self, *data):
        """
        注册多行注释
        :param data:调用命令
        """
        self._collection_add(self.script_keyword.note_multiple, data)

    def register_load_local_variable(self, commands, function):
        """
        注册加载局部变量
        :param commands:调用命令
        :param function:映射的方法
        """
        self._check_placeholder(commands, 1)
        self._collection_add(self.script_keyword.load_local_variable, commands)
        # 同时注册指令
        self.register_system_command(commands, function)

    def register_set_local_variable(self, *data):
        """
        注册局部变量定义
        :param data:调用命令
        """
        self._check_placeholder(data, 1)
        self._collection_add(self.script_keyword.set_local_variable, data)

    def register_get_local_variable(self, *data):
        """
        注册获取局部变量
        :param data:调用命令
        """
        self._check_placeholder(data, 1)
        self._collection_add(self.script_keyword.get_local_variable, data)

    def register_set_global_variable(self, *data):
        """
        注册全局变量定义
        :param data:调用命令
        """
        self._check_placeholder(data, 1)
        self._collection_add(self.script_keyword.set_global_variable, data)

    def register_get_global_variable(self, *data):
        """
        注册获取全局变量
        :param data:调用命令
        """
        self._check_placeholder(data, 1)
        self._collection_add(self.script_keyword.get_global_variable, data)

    def register_if_block(self, commands, function):
        """
        注册分支判断逻辑
        :param commands:调用命令
        :param function:执行的判断方法
        """
        self._check_placeholder(commands, 1)
        self._collection_add(self.script_keyword.if_block, commands)
        # 同时注册指令
        self.register_system_command(commands, function)

    def register_function_param(self, commands):
        """
        注册方法接收参数
        :param commands:调用命令
        """
        self._check_placeholder(commands, 1)
        self._collection_add(self.script_keyword.function_param, commands)
        # 同时注册指令

    def register_function_return(self, commands):
        """
        注册方法返回参数
        :param commands:调用命令
        """
        self._check_placeholder(commands, 1)
        self._collection_add(self.script_keyword.function_return, commands)

    def register_function_get_return(self, commands):
        """
        注册获取方法返回参数
        :param commands:调用命令
        """
        self._check_placeholder(commands, 1)
        self._collection_add(self.script_keyword.function_get_return, commands)

    def register_else_block(self, commands):
        """
        注册分支判断逻辑
        :param commands:调用命令
        """
        self._collection_add(self.script_keyword.else_block, commands)

    def register_end_if_block(self, commands):
        """
        注册分支判断逻辑
        :param commands:调用命令
        """
        self._collection_add(self.script_keyword.end_if, commands)

    def register_system_command(self, commands, function):
        """
        注册系统指令
        :param commands:
        :param function:
        :return:
        """
        if isinstance(commands, str):
            commands = (commands,)
        for item in commands:
            command, param_index = self._command_replace(item)
            self.system_command[command] = CommandFunction(command, item, function, param_index)

    def register_command(self, commands, function):
        """
        注册命令和执行的方法
        :param commands: 命令
        :param function: 执行的方法
        """
        if isinstance(commands, str):
            commands = (commands,)
        for item in commands:
            command, param_index = self._command_replace(item)
            self.command_map[command] = CommandFunction(command, item, function, param_index)

    def judge_statement(self, script_line, module_code: CommandBlock, line: int):
        """
        判断脚本是不是声明
        :param script_line:单行脚本
        :param module_code:模块代码
        :param line:源码行数
        :return: 是/不是
        """
        # 单行注释
        command = self._find_command(script_line, self.script_keyword.note_line)
        if command is not None:
            # 直接跳过
            return True

        # 多行注释
        command = self._find_command(script_line, self.script_keyword.note_multiple)
        if command is not None:
            self._compile_flag.is_note_multiple = not self._compile_flag.is_note_multiple
            # 只要读取到多行标识，一律跳过改行
            return True
        # 如果多行注释标识成立，则略过
        if self._compile_flag.is_note_multiple:
            return True

        # 循环开始
        command = self._find_command(script_line, self.script_keyword.loop_start)
        if command is not None:
            # 第一个参数为迭代对象，第二个为变量
            param = [None, *self._command_param(command, script_line)]
            flag_name = uuid.uuid4().__str__()
            jump_end = {"var": flag_name, "start": len(module_code.command_list), "end": -1, "loop_index": 0}
            self._compile_flag.loop_block_stack.append(jump_end)

            def loop_switch(*data):
                param[0] = data[0]
                self.variable.set_system_variable(False, flag_name, jump_end)
                loop_flag, item = self.system_command[command].function(data[0], jump_end["loop_index"])
                jump_end["loop_index"] += 1
                # 拿到循环条件
                if loop_flag:
                    self.variable.set_variable(False, param[1], item)
                    if len(data) > 2:
                        self.variable.set_variable(False, param[2], jump_end["loop_index"] - 1)
                    jump_end["loop"] = loop_flag
                else:
                    self.runtime_stack.goto(jump_end["end"])
                    jump_end["loop_index"] = 0

            module_code.append(Command(loop_switch, param, script_line, line, None))
            return True

        # 跳出循环
        command = self._find_command(script_line, self.script_keyword.jump_loop)
        if command is not None:
            if len(self._compile_flag.loop_block_stack) == 0:
                raise ValueError(f"缺少条件语句块！！！{line} {script_line}")
            jump_end = self._compile_flag.loop_block_stack[-1]

            def jump_start():
                # 回到开始的地方
                self.runtime_stack.goto(jump_end["start"])

            module_code.append(Command(jump_start, None, script_line, line, None))
            return True
        # 终止循环
        command = self._find_command(script_line, self.script_keyword.jump_loop)
        if command is not None:
            if len(self._compile_flag.loop_block_stack) == 0:
                raise ValueError(f"缺少条件语句块！！！{line} {script_line}")
            jump_end = self._compile_flag.loop_block_stack[-1]

            def loop_end():
                # 终止
                self.runtime_stack.goto(jump_end["end"])
                jump_end["loop_index"] = 0

            module_code.append(Command(loop_end, None, script_line, line, None))
            return True
        # 结束循环
        command = self._find_command(script_line, self.script_keyword.loop_end)
        if command is not None:
            if len(self._compile_flag.loop_block_stack) == 0:
                return False
            jump_end = self._compile_flag.loop_block_stack.pop()
            jump_end["end"] = len(module_code.command_list) + 1

            def loop_switch(*data):
                if jump_end["loop"]:
                    self.runtime_stack.goto(jump_end["start"])

            module_code.append(Command(loop_switch, None, script_line, line, None))
            return True
        # 分支块
        command = self._find_command(script_line, self.script_keyword.if_block)
        if command is not None:
            param = (None, *self._command_param(command, script_line))
            flag_name = uuid.uuid4().__str__()
            jump_end = {"var": flag_name, "end": -1}
            self._compile_flag.if_block_stack.append(jump_end)

            def if_block(*data):
                self.variable.set_system_variable(False, flag_name, jump_end)
                result = self.system_command[command].function(*data)
                if not result:
                    if "else" in jump_end:
                        self.runtime_stack.goto(jump_end["else"])
                    else:
                        self.runtime_stack.goto(jump_end["end"])

            module_code.append(Command(if_block, param, script_line, line, None))
            return True

        # 否则分支快
        command = self._find_command(script_line, self.script_keyword.else_block)
        if command is not None:
            if len(self._compile_flag.if_block_stack) == 0:
                raise ValueError(f"缺少条件语句块！！！{line} {script_line}")
            jump_end = self._compile_flag.if_block_stack[-1]
            # 标记否则的位置
            jump_end["else"] = len(module_code.command_list) + 1

            def jump():
                self.runtime_stack.goto(jump_end["end"])

            # 在if条件内的区域设置跳转到结束的标记
            module_code.append(Command(jump, None, script_line, line, None))
            jump_end["end"] = len(module_code.command_list)
            return True

        # 结束分支块
        command = self._find_command(script_line, self.script_keyword.end_if)
        if command is not None:
            if len(self._compile_flag.if_block_stack) == 0:
                return False
            jump_end = self._compile_flag.if_block_stack.pop()
            jump_end["end"] = len(module_code.command_list)
            return True

        # 局部变量加载
        command = self._find_command(script_line, self.script_keyword.load_local_variable)
        if command is not None:
            # 调用获取
            def run_load_data(*data):
                init_data = self.system_command[command].function(data)
                self.variable.load_local_variable(init_data)

            # 加载
            module_code.append(Command(run_load_data, self._command_param(command, script_line), script_line, line, None))
            return True

        # 局部变量声明
        command = self._find_command(script_line, self.script_keyword.set_local_variable)
        if command is not None:
            # 把要赋值的变量传入栈中
            module_code.append(Command(self.variable.set_local_variable, self._command_param(command, script_line), script_line, line, None))
            return True
        # 全局变量声明
        command = self._find_command(script_line, self.script_keyword.set_global_variable)
        if command is not None:
            # 把要赋值的变量传入栈中
            module_code.append(Command(self.variable.set_global_variable, self._command_param(command, script_line), script_line, line, None))
            return True

        # 局部变量获取
        command = self._find_command(script_line, self.script_keyword.get_local_variable)
        if command is not None:
            # 把要获取的变量传入栈中，传入原始元组，因为该指令可能存在坐标
            module_code.append(Command(self.variable.get_local_variable, self._command_param(command, script_line), script_line, line, None))
            return True
        # 全局变量获取
        command = self._find_command(script_line, self.script_keyword.get_global_variable)
        if command is not None:
            # 把要获取的变量传入栈中，传入原始元组，因为该指令可能存在坐标
            module_code.append(Command(self.variable.get_global_variable, self._command_param(command, script_line), script_line, line, None))
            return True

        # 方法参数获取
        command = self._find_command(script_line, self.script_keyword.function_param)
        if command is not None:
            # 把要获取的变量传入栈中，传入原始元组，因为该指令可能存在坐标
            module_code.append(Command(self.variable.function_set_param, self._command_param(command, script_line), script_line, line, None))
            return True

        # 方法参数返回
        command = self._find_command(script_line, self.script_keyword.function_return)
        if command is not None:
            # 把要获取的变量传入栈中，传入原始元组，因为该指令可能存在坐标
            module_code.append(Command(self.variable.function_return, self._command_param(command, script_line), script_line, line, None))
            return True

        # 获取方法返回参数
        command = self._find_command(script_line, self.script_keyword.function_get_return)
        if command is not None:
            # 把要获取的变量传入栈中，传入原始元组，因为该指令可能存在坐标
            module_code.append(Command(self.variable.function_get_return, self._command_param(command, script_line), script_line, line, None))
            return True

        # 代码起始位置
        command = self._find_command(script_line, self.script_keyword.code_start)
        if command is not None:
            self.compile_stack.add(f".{self._command_param(command, script_line)[0]}")
            return True

        # 代码结束位置
        command = self._find_command(script_line, self.script_keyword.code_end)
        if command is not None:
            module_info = self.compile_stack.pop()
            module_info.command_list.append(Command(self._return_call_module, None, script_line, line, None))
            self.script_module[module_info.name] = module_info
            if len(self._compile_flag.if_block_stack) != 0:
                raise ValueError(f'第{line}行，{script_line}，缺少条件结束标志！！！')
            return True

        # 如果调用脚本
        command = self._find_command(script_line, self.script_keyword.call_script)
        if command is not None:
            call_module = self._command_param(command, script_line)
            # 此处装配调用模块和前缀
            module_name = self.compile_stack.get_call_name(call_module[0])
            module_param = [module_name[0]]
            if len(call_module) > 1:
                module_param.extend(call_module[1:])
            module_code.append(Command(self._call_module, tuple(module_param), script_line, line, None))
            return True
        return False

    def analyze(self, text: str):
        """
        解析脚本
        :param text: 脚本
        """
        script_list = text.split("\n")
        line = 0
        commands = self.command_map.keys()
        for script_line in script_list:
            line += 1
            # 每次都拿栈中的最后一个的代码块
            module_code = self.compile_stack[-1]
            # 空格处理
            script_line = script_line.strip()
            if "" == script_line:
                continue
            if self.judge_statement(script_line, module_code, line):
                continue

            command = self._find_command(script_line, commands)
            if command is None:
                raise ValueError(f'第{line}行语句并未找到对应指令：', script_line)
            param = self._command_param(command, script_line)
            # 要方法，参数，行数、源码
            module_code.append(Command(self.command_map[command].function, param, script_line, line, self.command_map[command].param_index))
        # 对没有声明结束标识的，将其封装成模块
        for i in range(1, self.compile_stack.size()):
            module_info = self.compile_stack.pop()
            module_info.append(Command(self._return_call_module, None, None, line, None))
            self.script_module[module_info.name] = module_info
            if len(self._compile_flag.if_block_stack) != 0:
                raise ValueError("模块中缺少条件结束标志，在主模块中！！！")

    def execute(self, need_logger=False, need_reset=True, logger=None):
        """
        :param need_logger:需要记录日志
        :param need_reset:是需要重新加载
        :param logger:日志
        执行指令
        """
        if logger is None:
            logger = []
        if need_reset:
            self.runtime_stack.reset()
        command = None
        runtime_module = None
        try:
            while True:
                # 运行栈为空，则程序结束
                if self.runtime_stack.size() == 0:
                    break

                command, runtime_module = self.runtime_stack.next()
                if command is None:
                    continue
                line_logger = [runtime_module.name, runtime_module.program_counter, command.source_code]
                if need_logger:
                    logger.append(line_logger)
                command.execute(self.variable, line_logger)
        except Exception as exception:
            logger.append([runtime_module.name, runtime_module.program_counter, command.source_code, "执行脚本出错", exception])
            stack_info = self.runtime_stack.get_stack_info()
            msg = ""
            for info in stack_info:
                msg += f'\t{info}\n'
            error_list = ["执行脚本出错！！！", runtime_module.name, command.line, command.source_code, exception, "\n", msg]
            raise RuntimeError(LoggerUtil.padding(error_list, [13, 22, 8, 22, 35]))
        return logger

    def analyze_and_execute(self, text: str):
        """
        执行脚本
        :param text: 脚本
        """
        self.analyze(text)
        self.execute()

    def show_module(self):
        """
        打印当前注册的模块
        """
        for name, command_block in self.script_module.items():
            print("模块", name)
            for code in command_block.command_list:
                print("\t", code.source_code)
            print()

    def execute_module(self, module_name, need_logger=False):
        """
        直接执行某个模块
        :param module_name:模块名称
        :param need_logger:需要记录日志
        """

        if isinstance(module_name, str):
            module_name = (module_name,)
        log = []
        for name in module_name:
            try:
                self.runtime_stack.stack.clear()
                # 初始化变量栈
                self.variable.variable.append(Variable())

                # 需要在主方法结束的最后添加要直接执行的代码
                command_block = CommandBlock(self.runtime_stack.root.name)
                command_block.command_list.extend(self.runtime_stack.root.command_block.command_list)
                command_block.append(Command(self._call_module, self.compile_stack.get_call_name(name), "SYSTEM_CALL", -1, None))

                runtime_module = RuntimeModule(self.runtime_stack.root.name, command_block)
                self.runtime_stack.append(runtime_module)

                if need_logger:
                    log.append([name, 0, "模块开始运行"])
                self.execute(need_logger, False, log)
                if need_logger:
                    log.append([name, 0, "模块执行完毕"])
            except Exception as exception:
                print(exception)
                if need_logger:
                    log.append([name, -1, "因为异常终止"])
            finally:
                if need_logger:
                    log.append(())
        return log

    def show_command(self):
        for command in self.command_map.values():
            print(f'指令:{command.old_command}\t参数映射关系：{command.param_index}')


class ChiyaScript:

    @staticmethod
    def _if_equal(a, *b):
        print(a, b)
        return a == b[0]

    @staticmethod
    def _if(*a):
        return a

    @staticmethod
    def _loop(list_data, loop_index):
        if isinstance(list_data, int):
            return list_data > loop_index, loop_index
        if loop_index < len(list_data):
            return True, list_data[loop_index]
        return False, None

    @staticmethod
    def _init_script():
        script = CodeScript()

        script.register_start_block("module {}", "模块 {}")
        script.register_end_block("end", "结束")
        script.register_invoke("call {}", "invoke {}", "run {}", "调用 {}")

        script.register_function_param("@param {}")
        script.register_function_return("@return {}")
        script.register_function_get_return("@result {}")

        script.register_if_block(["if=={}", "if {}=={}"], ChiyaScript._if_equal)
        script.register_if_block(["if{}"], ChiyaScript._if)
        script.register_else_block("else")
        script.register_end_if_block("end if")

        script.register_loop_start(["loop {}", "loop {} {}", "loop {},{}"], ChiyaScript._loop)
        script.register_loop_end("end loop")
        script.register_jump_loop("next")
        script.register_loop_break("break")

        script.register_set_local_variable("@var {}", "@var {}={}")
        script.register_get_local_variable("@get {}", "@get {}->{}")

        script.register_set_global_variable("@push {}", "@push {}={}")
        script.register_get_global_variable("@pull {}", "@pull {}->{}")

        script.register_note_line("//{}", "#{}")
        script.register_note_multiple("/*{}", "/*", "*/")
        script.register_command(["print{}"], print)
        return script

    def __init__(self):
        self.script = self._init_script()

    def analyze(self, script: str):
        """
        解析脚本
        :param script: 脚本
        """
        self.script.analyze(script)

    def execute(self, need_logger=False, need_reset=True):
        """
        :param need_logger:需要记录日志
        :param need_reset:是需要重新加载
        执行指令
        """
        return self.script.execute(need_logger, need_reset)

    def analyze_and_execute(self, text: str):
        """
        执行脚本
        :param text: 脚本
        """
        self.script.analyze(text)
        self.script.execute()

    def execute_module(self, module_name, need_logger=False):
        """
        直接执行某个模块
        :param module_name:模块名称
        :param need_logger:需要记录日志
        """
        return self.script.execute_module(module_name, need_logger)

    @staticmethod
    def show_log(logger: list):
        padding = [20, 8, 22, 35, 20, 20]
        for log in logger:
            print(LoggerUtil.padding(log, padding))
