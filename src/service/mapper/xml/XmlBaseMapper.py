from src.service.mapper.xml.method.Delete import CreateMethodDelete
from src.service.mapper.xml.method.Insert import CreateMethodInsert
from src.service.mapper.xml.method.ResultMap import CreateResultMap
from src.service.mapper.xml.method.Select import CreateMethodSelect
from src.service.mapper.xml.method.SelectXtoX import CreateMethodSelectXToX
from src.service.mapper.xml.method.SqlFragment import CreateSqlFragment
from src.service.mapper.xml.method.Update import CreateMethodUpdate
from src.service.mapper.xml.method.XmlPretreatment import XmlPretreatment


class CreateFile:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config):
        data = '<?xml version="1.0" encoding="UTF-8"?>\n'
        data += '<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">\n'
        data += f'<mapper namespace="{config["module"]["baseMapperInterface"]["package"]}">\n'
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
        beanConfig, tables, tableMy = XmlPretreatment.pretreatment(config)
        data = ""
        data += CreateSqlFragment.create(config, tables, tableMy)
        data += CreateResultMap.create(beanConfig)
        data += CreateMethodInsert.create(config)
        data += CreateMethodDelete.create(config)
        data += CreateMethodUpdate.create(config)
        data += CreateMethodSelect.create(config)
        data += CreateMethodSelectXToX.create(beanConfig)
        return data
