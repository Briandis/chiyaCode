import re
from typing import List, Dict


class VariableSystem:

    def __init__(self):
        """
        变量系统
        """
        self.data = {}
        """ 变量 """
        self.variable_set_stack = []
        """ 变量赋值栈 """
        self.variable_get_stack = []
        """ 变量获取栈 """

    def set_variable(self, *data):
        """
        定义 变量
        :param data:变量信息
        """
        if len(data) > 1:
            self.set(data[0], data[1])
        if len(data) == 1:
            self.variable_set_stack.append(data[0])

    def get_variable(self, *data):
        """
        获取变量
        :param data: 获取变量
        """
        if len(data) > 0:
            self.variable_get_stack.append(data)

    def set(self, name, value):
        """
        设置变量
        :param name:名称
        :param value: 值
        """
        self.data[name] = value

    def get(self, name):
        """
        获取var对象
        :param name:变量名称
        """
        if name not in self.data:
            raise KeyError(f'{name}尚未定义')
        return self.data[name]


class Command:

    def __init__(self, function, param: tuple | None, source_code: str | None, line: int, param_index: tuple | list | None):
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

    def execute(self, variable_system: VariableSystem):
        """
        执行命令
        :param variable_system:变量系统
        """
        # 定义返回操作
        call_set = None
        if len(variable_system.variable_set_stack) > 0 and self.function != variable_system.get_variable:
            set_data = variable_system.variable_set_stack.pop()

            def call_set(data):
                variable_system.set(set_data[0], data)
        # 有参数的情况下
        if self.param is not None:
            if self.param_index is None:
                param = [*self.param]
            else:
                param = []
                # 参数转换
                for index in self.param_index:
                    param.append(self.param[index - 1])
            # 从变量栈中获取值，并且对参数进替换，只有在该执行方法不同的情况下
            if self.function != variable_system.get_variable and self.function != variable_system.set_variable:
                while len(variable_system.variable_get_stack) > 0:
                    index = len(variable_system.variable_get_stack) - 1
                    var = variable_system.variable_get_stack.pop()
                    if len(var) > 1:
                        index = int(var[1]) - 1
                    param[index] = variable_system.get(var[0])
            # 执行
            result = self.function(*param)
            if call_set is not None:
                # 将返回结果赋予变量
                call_set(result)

        else:
            result = self.function()
            if call_set is not None:
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
        self.set_variable = []
        """ 变量声明 """
        self.get_variable = []
        """ 变量获取 """
        self.function_variable = []
        """ 方法变量 """


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

    def next(self) -> (Command, RuntimeModule):
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
            script_stack.append(f'\t{runtime_module.name} : {runtime_module.last_command().source_code} line:{runtime_module.program_counter - 1}')
        return script_stack

    def reset(self):
        """
        重置栈
        """
        self.stack.clear()
        self.root.program_counter = 0
        self.stack.append(self.root)


class CompileFlag:
    def __init__(self):
        """
        编译检查点
        """
        self.is_note_multiple = False
        """ 是多行注释 """


class CodeScript:

    def __init__(self):
        """
        脚本核心
        """
        self.command_map: Dict[str, CommandFunction] = {}
        """ 指令 """
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
            match.sort()
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

    def _call_module(self, module_name: str):
        """
        调用并执行某个模块
        :param module_name:模块名称
        """
        module_code = self._load_module(module_name)
        self.runtime_stack.append(RuntimeModule(module_name, module_code))

    def _return_call_module(self):
        """
        模块调用结束
        """
        self.runtime_stack.pop()

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

    def register_set_variable(self, *data):
        """
        注册声明变量
        :param data:调用命令
        """
        self._check_placeholder(data, 1)
        self._collection_add(self.script_keyword.set_variable, data)

    def register_get_variable(self, *data):
        """
        注册获取变量
        :param data:调用命令
        """
        self._check_placeholder(data, 1)
        self._collection_add(self.script_keyword.get_variable, data)

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

        # 变量声明
        command = self._find_command(script_line, self.script_keyword.set_variable)
        if command is not None:
            # 把要赋值的变量传入栈中
            # commands, param_index = self._command_replace(command)
            module_code.append(Command(self.variable.set_variable, self._command_param(command, script_line), script_line, line, None))
            return True

        # 变量获取
        command = self._find_command(script_line, self.script_keyword.get_variable)
        if command is not None:
            # 把要获取的变量传入栈中，传入原始元组，因为该指令可能存在坐标
            module_code.append(Command(self.variable.get_variable, self._command_param(command, script_line), script_line, line, None))
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
            return True

        # 如果调用脚本
        command = self._find_command(script_line, self.script_keyword.call_script)
        if command is not None:
            call_module = self._command_param(command, script_line)[0]
            # 此处装配调用模块和前缀
            call_module = self.compile_stack.get_call_name(call_module)
            module_code.append(Command(self._call_module, call_module, script_line, line, None))
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

    def execute(self, need_logger=False, need_reset=True):
        """
        :param need_logger:需要记录日志
        :param need_reset:是需要重新加载
        执行指令
        """
        if need_reset:
            self.runtime_stack.reset()
        command = None
        logger = []
        try:
            while True:
                # 运行栈为空，则程序结束
                if self.runtime_stack.size() == 0:
                    break

                command, runtime_module = self.runtime_stack.next()
                if command is None:
                    continue
                if need_logger:
                    logger.append(f'{runtime_module.name}:\t{runtime_module.program_counter}\t{command.source_code}')
                command.execute(self.variable)
        except:
            stack_info = self.runtime_stack.get_stack_info()
            msg = ""
            for info in stack_info:
                msg += info + "\n"
            raise RuntimeError(f"脚本执行出错！！！line: {command.line}\tparam: {command.param}\t{command.source_code}\n{msg}")
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
            self.runtime_stack.stack.clear()
            # 需要在主方法结束的最后添加要直接执行的代码

            command_block = CommandBlock(self.runtime_stack.root.name)
            command_block.command_list.extend(self.runtime_stack.root.command_block.command_list)
            command_block.append(Command(self._call_module, self.compile_stack.get_call_name(name), "SYSTEM_CALL", -1, None))

            runtime_module = RuntimeModule(self.runtime_stack.root.name, command_block)
            self.runtime_stack.append(runtime_module)

            if need_logger:
                log.append(f'{name}模块开始直接执行')
            module_log = self.execute(need_logger, False)
            if need_logger:
                for item in module_log:
                    log.append('\t' + item)
                log.append(f'{name}模块执行完毕\n')
        return log

    def show_command(self):
        for command in self.command_map.values():
            print(f'指令:{command.old_command}\t参数映射关系：{command.param_index}')
