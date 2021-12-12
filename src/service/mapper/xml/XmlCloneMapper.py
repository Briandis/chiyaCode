class CreateFile:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config):
        data = '<?xml version="1.0" encoding="UTF-8"?>\n'
        data += '<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">\n'
        data += f'<mapper namespace="{config["mapperInterface"]["package"]}">\n'
        data += "\n"
        data += CreateMethod.create(config)
        data += "</mapper>\n"
        return data


# 创建方法
class CreateMethod:
    """
    创建接口方法
    """

    @staticmethod
    def create(config: dict):
        data = ""
        return data
