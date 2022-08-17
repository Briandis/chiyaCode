import json
import os

from src.ddd.api import Controller
from src.structure.CodeConfig import CodeConfig, Field
from src.structure.CreateConfig import FileType
from src.util.OSUtil import save_file


class Generate:

    def __init__(self):
        path = "config"
        path = os.path.join(os.getcwd(), path)
        if not os.path.exists(path):
            raise FileNotFoundError("config文件夹不存在！！！！")
        list_file = os.listdir(path)
        self.data = []
        self.config = []
        for file in list_file:
            if ".json" in file:
                print(f"发现{file}")
                self.data.append(json.load(open(os.path.join(path, file), encoding="utf-8")))
        print(f"总共{len(self.data)}个文件")

    def code_config(self):
        """
        字典转对象配置
        """
        for d in self.data:
            config = CodeConfig()
            for i in config.__dict__:
                if config.__getattribute__(i) is None:
                    config.__setattr__(i, d.get(i))
            # 主键数据处理
            config.key = Field.create_field(d.get("key"))
            for attr in d.get("attr"):
                config.attr.append(Field.create_field(attr))
            # 模块处理
            for module in d["module"]:
                config.module.__getattribute__(module).set_field(d["module"][module])
            # 生成配置处理
            for key in d["config"]:
                value = d["config"][key]
                base_config = config.createConfig.__getattribute__(key)
                base_config.set_field(value)
            self.config.append(config)
            # for i in config.module.__dict__:
            #     print(config.module.__getattribute__(i).__dict__)
            # for i in config.createConfig.__dict__:
            #     print(i, config.createConfig.__getattribute__(i).__dict__)
            # for j in config.__dict__:
            #     print(j, config.__getattribute__(j))

    def generate(self):
        print("开始准备解析")
        self.code_config()
        for i in self.config:
            self.__parsing(i)

    def __parsing(self, config: CodeConfig):

        # 生成控制层
        if self.check_create(FileType.controller, config):
            string = Controller.CreateFile.create(config)
            save_file(config.module.controller.path, config.module.controller.className, "java", string)

    @staticmethod
    def check_create(create_type: str, config: CodeConfig):
        """
        检查文件是否能生成
        :param create_type: 生成的类型
        :param config: 配置信息
        :return: true:能/false:不能
        """
        create_list = config.createConfig.createFile.value
        if create_list is None:
            create_list = config.createConfig.createFile.default
        not_create_list = config.createConfig.notCreateFile.value
        if not_create_list is None:
            not_create_list = config.createConfig.notCreateFile.default
        return create_type in create_list and create_type not in not_create_list
