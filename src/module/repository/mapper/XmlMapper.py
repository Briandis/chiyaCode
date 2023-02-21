from src.java.CodeConfig import CodeConfig, Field
from src.xml import MapperTag
from src.xml.MapperUtil import MapperUtil


class XmlMapperCode:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig):
        mapper = MapperTag.Mapper(config.module.mapperXml.get_package())
        mapper.add_tag(MapperTag.LineNote("本文件是提供给用户编写SQL的文件，用户可以放心的在此编写SQL，但需注意，后续生成不要生成该文件"))
        mapper.add_blank_line()

        mapper.add_tag(MapperTag.LineNote("resultMap映射关系"))
        ResultMapBlock.create(config, mapper)

        mapper.add_blank_line()
        return MapperTag.XmlMapper(mapper).create()


class ResultMapBlock:
    """
    ResultMap标签块
    """

    @staticmethod
    def result_map_collection(code_config: CodeConfig, collection: CodeConfig, xml_mapper: MapperTag.Mapper, generated_result: set, many_to_many=False):
        """
        生成单表的ResultMap
        :param code_config: 本表配置
        :param collection: 一对多另一方的配置
        :param xml_mapper: XML代码
        :param generated_result: 生成的唯一ID
        :param many_to_many: 是否是多对多，默认不是
        :return: ResultMap标签块
        """
        name = MapperUtil.result_map_name(code_config, collection, False, not many_to_many, many_to_many)
        if name in generated_result:
            return
        generated_result.add(name)
        result_map = MapperTag.ResultMap(name, code_config.module.entity.get_package())
        result_map.set_extends(f'{code_config.module.mapperXml.get_package()}.{name}')
        if many_to_many:
            xml_mapper.add_tag(MapperTag.LineNote(f'{code_config.module.entity.remark}多对多{collection.module.entity.remark}的ResultMap'))
        else:
            xml_mapper.add_tag(MapperTag.LineNote(f'{code_config.module.entity.remark}一对多{collection.module.entity.remark}的ResultMap'))
        xml_mapper.add_tag(result_map)

    @staticmethod
    def result_map_association(code_config: CodeConfig, association: CodeConfig, xml_mapper: MapperTag.Mapper, generated_result: set):
        """
        生成单表的ResultMap
        :param code_config: 本表配置
        :param association: 一对一另一方的配置
        :param xml_mapper: XML代码
        :param generated_result: 生成的唯一ID
        """
        name = MapperUtil.result_map_name(code_config, association, True)
        if name in generated_result:
            return
        generated_result.add(name)

        result_map = MapperTag.ResultMap(name, code_config.module.entity.get_package())
        result_map.set_extends(f'{code_config.module.mapperXml.get_package()}.{name}')
        xml_mapper.add_tag(MapperTag.LineNote(f'{code_config.module.entity.remark}一对一{association.module.entity.remark}的ResultMap'))
        xml_mapper.add_tag(result_map)

    @staticmethod
    def result_map(code_config: CodeConfig, xml_mapper: MapperTag.Mapper, generated_result: set):
        """
        生成单表的ResultMap
        :param code_config: 配置
        :param xml_mapper: XML代码
        :param generated_result: 生成的唯一ID
        """
        name = MapperUtil.result_map_name(code_config)
        if name in generated_result:
            return

        result_map = MapperTag.ResultMap(name, code_config.module.entity.get_package())
        result_map.set_extends(f'{code_config.module.mapperXml.get_package()}.{name}')
        xml_mapper.add_tag(MapperTag.LineNote(f'{code_config.module.entity.remark}的ResultMap'))
        xml_mapper.add_tag(result_map)

    @staticmethod
    def create(code_config: CodeConfig, xml_mapper: MapperTag.Mapper):
        generated_result = set()
        # 单表的
        ResultMapBlock.result_map(code_config, xml_mapper, generated_result)
        # 多表的
        # 一对一
        for one_to_one in code_config.baseInfo.oneToOne:
            ResultMapBlock.result_map_association(code_config, one_to_one, xml_mapper, generated_result)
            ResultMapBlock.result_map(one_to_one, xml_mapper, generated_result)
        # 一对多
        for one_to_many in code_config.baseInfo.oneToMany:
            ResultMapBlock.result_map_collection(code_config, one_to_many, xml_mapper, generated_result)
            ResultMapBlock.result_map(one_to_many, xml_mapper, generated_result)
        # 一对多
        for many_to_many in code_config.baseInfo.manyToMany:
            ResultMapBlock.result_map_collection(code_config, many_to_many.many, xml_mapper, generated_result, True)
            ResultMapBlock.result_map(many_to_many.many, xml_mapper, generated_result)
