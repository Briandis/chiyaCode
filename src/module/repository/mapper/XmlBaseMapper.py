from src.java.CodeConfig import CodeConfig, Field
from src.module.base.BaseApi import MapperApi, MapperApiNote
from src.xml import MapperTag
from src.xml.MapperTag import BlockTag
from src.xml.MapperUtil import MapperUtil


class XmlBaseMapperCode:
    """
    创建整个文件内容，主要是文件流程的组装
    """

    @staticmethod
    def create(config: CodeConfig):
        mapper = MapperTag.Mapper(config.module.baseMapperXml.get_package())
        mapper.add_tag(MapperTag.LineNote("本XML为自动生成，请勿在本文件中修改或新增任何内容！！！"))
        mapper.add_tag(MapperTag.LineNote(f"如需修改或新增，请移步至{config.module.mapperXml.className}.xml文件中，以防止重新生成的文件替换编写的代码！"))
        mapper.add_blank_line()
        # 生成SQL片段
        mapper.add_tag(MapperTag.LineNote("SQL片段"))
        XmlSqlBlock.create(config, mapper)
        mapper.add_blank_line()
        mapper.add_tag(MapperTag.LineNote("resultMap映射关系"))
        ResultMapBlock.create(config, mapper)
        mapper.add_tag(MapperTag.LineNote("Insert语句块"))
        InsertBlock.create(config, mapper)
        mapper.add_tag(MapperTag.LineNote("Delete语句块"))
        DeleteBlock.create(config, mapper)
        mapper.add_tag(MapperTag.LineNote("Update语句块"))
        UpdateBlock.create(config, mapper)
        mapper.add_tag(MapperTag.LineNote("Select单表语句块"))
        SelectBlock.create(config, mapper)
        # 一对一查询块
        SelectOneToOneBlock.create(config, mapper)
        # 一对多查询块
        SelectOneToManyBlock.create(config, mapper)
        # 多对多
        SelectManyToManyBlock.create(config, mapper)
        # 外键查询
        SelectInForeignKey.create(config, mapper)
        mapper.add_blank_line()
        return MapperTag.XmlMapper(mapper).create()


class XmlSqlBlock:
    """
    SQL片段标签
    """

    @staticmethod
    def get_field_alias(field: Field):
        """
        获取字段的别名用于SQL片段
        :param field: 字段
        :return: 含有别名的字符串
        """
        if field.alias is None:
            return ""
        return F' AS {field.alias}'

    @staticmethod
    def sql_tag(code_config: CodeConfig):
        """
        生成SQL的标签
        :param code_config:配置
        :return: SQL的标签
        """
        sql_tag = MapperTag.Sql(MapperUtil.sql_tag_name(code_config))
        # 拼接字符串，如果存在表的别名情况，说明是和自身重复
        sql_data = ""
        if code_config.baseInfo.key is not None:
            sql_data = f'{code_config.baseInfo.get_table_alias()}.{code_config.baseInfo.key.field}{XmlSqlBlock.get_field_alias(code_config.baseInfo.key)}, '
        for field in code_config.baseInfo.attr:
            sql_data += f'{code_config.baseInfo.get_table_alias()}.{field.field}{XmlSqlBlock.get_field_alias(field)}, '
        # 把字符串放入标签种，并且去除最后的逗号
        sql_tag.add_data(sql_data.strip(', '))
        return sql_tag

    @staticmethod
    def create(code_config: CodeConfig, xml_mapper: MapperTag.Mapper):
        """
        构建SQL块
        :param code_config:配置
        :param xml_mapper: XML的标签块
        :return: 自身
        """
        sql_set = set()
        # 一对一的块
        for one_to_one in code_config.baseInfo.oneToOne:
            # 该配置存在字段冲突，需要生成SQL字段的片段，并且没有生成过
            if one_to_one.baseInfo.need_sql_block() and one_to_one.baseInfo.tableName not in sql_set:
                xml_mapper.add_tag(XmlSqlBlock.sql_tag(one_to_one))
                sql_set.add(one_to_one.baseInfo.tableName)
        # 一对多的块
        for one_to_many in code_config.baseInfo.oneToMany:
            # 该配置存在字段冲突，需要生成SQL字段的片段，并且没有生成过
            if one_to_many.baseInfo.need_sql_block() and one_to_many.baseInfo.tableName not in sql_set:
                xml_mapper.add_tag(XmlSqlBlock.sql_tag(one_to_many))
                sql_set.add(one_to_many.baseInfo.tableName)
        # 多对多的块
        for many_to_many in code_config.baseInfo.manyToMany:
            # 该配置存在字段冲突，需要生成SQL字段的片段，并且没有生成过
            if many_to_many.many.baseInfo.need_sql_block() and many_to_many.many.baseInfo.tableName not in sql_set:
                xml_mapper.add_tag(XmlSqlBlock.sql_tag(many_to_many.many))
                sql_set.add(many_to_many.many.baseInfo.tableName)


class ResultMapBlock:
    """
    ResultMap标签块
    """

    @staticmethod
    def add_result(code_config: CodeConfig, tag: MapperTag.ResultMap | MapperTag.Association | MapperTag.Collection, need_alias=True):
        """
        根据配置装配该映射标签
        :param code_config:配置
        :param tag: 映射标签
        :param need_alias: 需要使用别名
        :return:
        """
        if code_config.baseInfo.key is not None:
            if need_alias:
                tag.set_id(code_config.baseInfo.key.get_field(), code_config.baseInfo.key.attr)
            else:
                tag.set_id(code_config.baseInfo.key.field, code_config.baseInfo.key.attr)
        for field in code_config.baseInfo.attr:
            if need_alias:
                tag.set_result(field.get_field(), field.attr)
            else:
                tag.set_result(field.field, field.attr)

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

        association_tag = MapperTag.Collection(f'list{collection.module.entity.className}', collection.module.entity.get_package())
        # 装配各个标签的映射字段
        ResultMapBlock.add_result(code_config, result_map)
        ResultMapBlock.add_result(collection, association_tag)
        # 装配标签
        result_map.add_tag(association_tag)

        if many_to_many:
            xml_mapper.add_tag(MapperTag.LineNote(f'{code_config.module.entity.remark}多对多{collection.module.entity.remark}的ResultMap'))
        else:
            xml_mapper.add_tag(MapperTag.LineNote(f'{code_config.module.entity.remark}一对多{collection.module.entity.remark}的ResultMap'))
        xml_mapper.add_tag(result_map)
        xml_mapper.add_blank_line()

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
        association_tag = MapperTag.Association(association.module.entity.low_name(), association.module.entity.get_package())
        # 装配各个标签的映射字段
        ResultMapBlock.add_result(code_config, result_map)
        ResultMapBlock.add_result(association, association_tag)
        # 装配标签
        result_map.add_tag(association_tag)

        xml_mapper.add_tag(MapperTag.LineNote(f'{code_config.module.entity.remark}一对一{association.module.entity.remark}的ResultMap'))
        xml_mapper.add_tag(result_map)
        xml_mapper.add_blank_line()

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
        ResultMapBlock.add_result(code_config, result_map, False)

        xml_mapper.add_tag(MapperTag.LineNote(f'{code_config.module.entity.remark}的ResultMap'))
        xml_mapper.add_tag(result_map)
        xml_mapper.add_blank_line()

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


class InsertBlock:
    """
    Insert标签块
    """

    @staticmethod
    def __insert(code_config: CodeConfig):
        """
        插入语句块，单个
        :param code_config: 生成配置
        :return: 插入标签块
        """
        insert = MapperTag.Insert(MapperApi.Insert.insert(code_config))
        if code_config.baseInfo.key is not None:
            insert.set_use_generated_keys("true")
            insert.set_key_column(code_config.baseInfo.key.field)
            insert.set_key_property(code_config.baseInfo.key.attr)

        insert.add_data(f"INSERT INTO {MapperUtil.get_table_name(code_config)} (").indent_increase()
        insert.add_tag(BlockTag.trim_if_block(code_config, is_field=True, is_attr=False)).indent_decrease()
        insert.add_data(") VALUES (")
        insert.add_tag(BlockTag.trim_if_block(code_config, is_attr=True))
        insert.add_data(")")
        return insert

    @staticmethod
    def __insert_list(code_config: CodeConfig):
        """
        插入语句块，多个
        :param code_config: 生成配置
        :return: 插入标签块
        """
        insert = MapperTag.Insert(MapperApi.Insert.insert_list(code_config))
        if code_config.baseInfo.key is not None:
            insert.set_use_generated_keys("true")
            insert.set_key_column(code_config.baseInfo.key.field)
            insert.set_key_property(code_config.baseInfo.key.attr)

        insert.add_data(f"INSERT INTO {MapperUtil.get_table_name(code_config)} (").indent_increase()
        insert.add_data(MapperUtil.join_all_field(code_config)).indent_decrease()
        insert.add_data(") VALUES ")
        insert.add_tag(BlockTag.foreach_block(code_config))
        return insert

    @staticmethod
    def __insert_or_update_unique(code_config: CodeConfig):
        """
        插入语句块，插入或更新，根据唯一性
        :param code_config: 生成配置
        :return: 插入标签块
        """
        insert = MapperTag.Insert(MapperApi.Insert.insert_or_update_by_unique(code_config))
        if code_config.baseInfo.key is not None:
            insert.set_use_generated_keys("true")
            insert.set_key_column(code_config.baseInfo.key.field)
            insert.set_key_property(code_config.baseInfo.key.attr)

        insert.add_data(f"INSERT INTO {MapperUtil.get_table_name(code_config)} (").indent_increase()
        insert.add_tag(BlockTag.trim_if_block(code_config, is_field=True, is_attr=False)).indent_decrease()
        insert.add_data(") VALUES (").indent_increase()
        insert.add_tag(BlockTag.trim_if_block(code_config, is_attr=True)).indent_decrease()
        insert.add_data(") ON DUPLICATE KEY UPDATE")
        insert.add_tag(BlockTag.trim_if_block(code_config, is_field=True, is_attr=True, need_key=False))
        return insert

    @staticmethod
    def __insert_or_update_where(code_config: CodeConfig):
        """
        插入语句块，插入或更新，根据查询条件
        :param code_config: 生成配置
        :return: 插入标签块
        """
        insert = MapperTag.Insert(MapperApi.Insert.insert_or_update_by_where(code_config))

        select_key = MapperTag.SelectKey(code_config.get_class_name(condition=True), code_config.baseInfo.key.field, code_config.baseInfo.key.type)
        select_key.add_data("SELECT IFNULL ((").indent_increase()
        select_key.add_data(f'SELECT {code_config.baseInfo.key.field} FROM {MapperUtil.get_table_name(code_config)}')

        select_key.add_tag(BlockTag.where_if_block(code_config, code_config.get_class_name(condition=True), need_data=False)).indent_decrease()
        select_key.add_data("),NULL)")
        insert.add_tag(select_key)

        # 插入块
        if_tag = MapperTag.If(
            f'{code_config.get_class_name(condition=True)}.{code_config.baseInfo.key.field}==null',
            f"INSERT INTO {MapperUtil.get_table_name(code_config)} ("
        ).add_tag(BlockTag.trim_if_block(code_config, var_name=code_config.get_class_name(save=True), is_field=True, is_attr=False)) \
            .add_data(") VALUES (") \
            .add_tag(BlockTag.trim_if_block(code_config, var_name=code_config.get_class_name(save=True), is_attr=True)) \
            .add_data(")")
        insert.add_tag(if_tag)
        # 更新块
        if_tag = MapperTag.If(
            f'{code_config.get_class_name(condition=True)}.{code_config.baseInfo.key.field}!=null',
            f"UPDATE {MapperUtil.get_table_name(code_config)} "
        ).add_tag(BlockTag.set_if_block(code_config, var_name=code_config.get_class_name(save=True))) \
            .add_data(f"WHERE {code_config.baseInfo.key.field} = #{{{code_config.get_class_name(condition=True)}.{code_config.baseInfo.key.attr}}}")
        insert.add_tag(if_tag)
        return insert

    @staticmethod
    def __insert_by_exist(code_config: CodeConfig):
        """
        插入语句块，条件存在，则插入
        :param code_config: 生成配置
        :return: 插入标签块
        """
        insert = MapperTag.Insert(MapperApi.Insert.insert_by_exist_where(code_config))
        if code_config.baseInfo.key is not None:
            insert.set_use_generated_keys("true")
            insert.set_key_column(code_config.baseInfo.key.field)
            insert.set_key_property(code_config.baseInfo.key.attr)

        insert.add_data(f"INSERT INTO {MapperUtil.get_table_name(code_config)} (").indent_increase()
        insert.add_tag(BlockTag.trim_if_block(code_config, var_name=code_config.get_class_name(save=True), is_field=True, is_attr=False)).indent_decrease()
        insert.add_data(") SELECT ")
        insert.add_tag(BlockTag.trim_if_block(code_config, var_name=code_config.get_class_name(save=True), is_attr=True))
        insert.add_data("FROM DUAL WHERE EXISTS (").indent_increase()
        if code_config.baseInfo.key is not None:
            insert.add_data(f'SELECT {code_config.baseInfo.key.field} FROM {MapperUtil.get_table_name(code_config)}')
        else:
            insert.add_data(f'SELECT * FROM {MapperUtil.get_table_name(code_config)}')
        insert.add_tag(BlockTag.where_if_block(code_config, var_name=code_config.get_class_name(condition=True), need_data=False)).indent_decrease()
        insert.add_data(")")
        return insert

    @staticmethod
    def __insert_by_not_exist(code_config: CodeConfig):
        """
        插入语句块，条件不存在，则插入
        :param code_config: 生成配置
        :return: 插入标签块
        """
        insert = MapperTag.Insert(MapperApi.Insert.insert_by_not_exist_where(code_config))
        if code_config.baseInfo.key is not None:
            insert.set_use_generated_keys("true")
            insert.set_key_column(code_config.baseInfo.key.field)
            insert.set_key_property(code_config.baseInfo.key.attr)

        insert.add_data(f"INSERT INTO {MapperUtil.get_table_name(code_config)} (").indent_increase()
        insert.add_tag(BlockTag.trim_if_block(code_config, var_name=code_config.get_class_name(save=True), is_field=True, is_attr=False)).indent_decrease()
        insert.add_data(") SELECT ")
        insert.add_tag(BlockTag.trim_if_block(code_config, var_name=code_config.get_class_name(save=True), is_attr=True))
        insert.add_data("FROM DUAL WHERE NOT EXISTS (").indent_increase()
        if code_config.baseInfo.key is not None:
            insert.add_data(f'SELECT {code_config.baseInfo.key.field} FROM {MapperUtil.get_table_name(code_config)}')
        else:
            insert.add_data(f'SELECT * FROM {MapperUtil.get_table_name(code_config)}')
        insert.add_tag(BlockTag.where_if_block(code_config, var_name=code_config.get_class_name(condition=True), need_data=False)).indent_decrease()
        insert.add_data(")")
        return insert

    @staticmethod
    def create(code_config: CodeConfig, xml_mapper: MapperTag.Mapper):
        # 添加单条
        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.Insert.insert(code_config)))
        xml_mapper.add_tag(InsertBlock.__insert(code_config)).add_blank_line()
        # 添加多条
        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.Insert.insert_list(code_config)))
        xml_mapper.add_tag(InsertBlock.__insert_list(code_config)).add_blank_line()
        # 根据唯一性索引保存或更新
        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.Insert.insert_or_update_by_unique(code_config)))
        xml_mapper.add_tag(InsertBlock.__insert_or_update_unique(code_config)).add_blank_line()
        # 根据条件保存或更新
        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.Insert.insert_or_update_by_where(code_config)))
        xml_mapper.add_tag(InsertBlock.__insert_or_update_where(code_config)).add_blank_line()
        # 如果存在则插入
        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.Insert.insert_by_exist_where(code_config)))
        xml_mapper.add_tag(InsertBlock.__insert_by_exist(code_config)).add_blank_line()
        # 如果不存在则插入
        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.Insert.insert_by_not_exist_where(code_config)))
        xml_mapper.add_tag(InsertBlock.__insert_by_not_exist(code_config)).add_blank_line()


class DeleteBlock:

    @staticmethod
    def __delete_by_key(code_config: CodeConfig):
        """
        根据主键删除
        :param code_config:配置
        :return:删除标签
        """
        sql_tag = MapperTag.Delete(MapperApi.Delete.delete_by_id(code_config))
        sql_tag.add_data(f"DELETE FROM {MapperUtil.get_table_name(code_config)} WHERE {code_config.baseInfo.key.field} = #{{{code_config.baseInfo.key.attr}}}")
        return sql_tag

    @staticmethod
    def __delete_in_key(code_config: CodeConfig):
        """
        根据多个主键删除
        :param code_config:配置
        :return:删除标签
        """
        sql_tag = MapperTag.Delete(MapperApi.Delete.delete_in_id(code_config))
        sql_tag.add_data(f"DELETE FROM {MapperUtil.get_table_name(code_config)} WHERE {code_config.baseInfo.key.field} IN").indent_increase()
        sql_tag.add_tag(MapperTag.Foreach(opens="(", close=")").add_data("#{obj}")).indent_decrease()
        return sql_tag

    @staticmethod
    def __delete_by_key_and_where(code_config: CodeConfig):
        """
        根据主键删除
        :param code_config:配置
        :return:删除标签
        """
        sql_tag = MapperTag.Delete(MapperApi.Delete.delete_by_id_and_where(code_config))
        sql_tag.add_data(f"DELETE FROM {MapperUtil.get_table_name(code_config)}")
        sql_tag.add_tag(
            MapperTag.Where()
                .add_data(f'{code_config.baseInfo.key.field} = #{{{code_config.baseInfo.key.attr}}}')
                .add_tag(BlockTag.if_var_block(code_config, is_field=True, is_attr=True, start="AND ", end=""))
        )
        return sql_tag

    @staticmethod
    def __delete_by_where(code_config: CodeConfig):
        """
        根据主键删除
        :param code_config:配置
        :return:删除标签
        """
        sql_tag = MapperTag.Delete(MapperApi.Delete.delete(code_config))
        sql_tag.add_data(f"DELETE FROM {MapperUtil.get_table_name(code_config)}")
        sql_tag.add_tag(BlockTag.where_if_block(code_config, need_var=True))
        return sql_tag

    @staticmethod
    def create(code_config: CodeConfig, xml_mapper: MapperTag.Mapper):
        if code_config.baseInfo.key is not None:
            # 根据id删除
            xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.Delete.delete_by_id(code_config)))
            xml_mapper.add_tag(DeleteBlock.__delete_by_key(code_config)).add_blank_line()
            # 根据多个id删除
            xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.Delete.delete_in_id(code_config)))
            xml_mapper.add_tag(DeleteBlock.__delete_in_key(code_config)).add_blank_line()
            # 根据id和条件
            xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.Delete.delete_by_id_and_where(code_config)))
            xml_mapper.add_tag(DeleteBlock.__delete_by_key_and_where(code_config)).add_blank_line()
        # 根据条件
        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.Delete.delete(code_config)))
        xml_mapper.add_tag(DeleteBlock.__delete_by_where(code_config)).add_blank_line()


class UpdateBlock:

    @staticmethod
    def __update_by_key(code_config: CodeConfig):
        """
        根据主键更新
        :param code_config:配置
        :return:修改标签
        """
        sql_tag = MapperTag.Update(MapperApi.Update.update_by_id(code_config))
        sql_tag.add_data(f"UPDATE {MapperUtil.get_table_name(code_config)}")
        sql_tag.add_tag(BlockTag.set_if_block(code_config))
        sql_tag.add_data(f'WHERE {code_config.baseInfo.key.field} = #{{{code_config.baseInfo.key.attr}}}')
        return sql_tag

    @staticmethod
    def __update_by_where(code_config: CodeConfig):
        """
        根据条件更新
        :param code_config:配置
        :return:修改标签
        """
        sql_tag = MapperTag.Update(MapperApi.Update.update(code_config))
        sql_tag.add_data(f"UPDATE {MapperUtil.get_table_name(code_config)}")
        sql_tag.add_tag(BlockTag.set_if_block(code_config))
        where = MapperTag.Where()
        sql_tag.add_tag(where)
        where.add_tag(BlockTag.field_if(code_config.baseInfo.key, code_config.get_class_name(save=True), is_field=True, is_attr=True, start="AND ", end=""))
        where.add_tag(BlockTag.if_var_block(code_config, var_name=code_config.get_class_name(condition=True), is_field=True, is_attr=True))

        return sql_tag

    @staticmethod
    def __update_not_repeat(code_config: CodeConfig):
        """
        根据主键更新
        :param code_config:配置
        :return:修改标签
        """
        sql_tag = MapperTag.Update(MapperApi.Update.update_by_not_repeat_where(code_config))
        sql_tag.add_data(f"UPDATE {MapperUtil.get_table_name(code_config)}")
        sql_tag.add_tag(BlockTag.set_if_block(code_config, code_config.get_class_name(save=True)))
        if code_config.baseInfo.key is not None:
            sql_tag.add_data(f'WHERE {code_config.baseInfo.key.field} = #{{{code_config.baseInfo.key.attr}}}')
        else:
            sql_tag.add_data(f'WHERE')
        temp_str = ""
        if code_config.baseInfo.key is not None:
            temp_str += f'{code_config.get_class_name(condition=True)}.{code_config.baseInfo.key.attr}!=null'
        for attr in code_config.baseInfo.attr:
            temp_str += f' or {code_config.get_class_name(condition=True)}.{attr.attr}!=null'
        if_tag = MapperTag.If(f'{code_config.get_class_name(condition=True)}!=null and ({temp_str})')
        if_tag.add_data("AND NOT EXISTS (").indent_increase()
        if code_config.baseInfo.key is not None:
            if_tag.add_data(f'SELECT {code_config.baseInfo.key.field} FROM (SELECT * FROM {MapperUtil.get_table_name(code_config)}) AS t ')
        else:
            if_tag.add_data(f'SELECT * FROM (SELECT * FROM {MapperUtil.get_table_name(code_config)}) AS t ')
        if_tag.add_tag(BlockTag.where_if_block(code_config, var_name=code_config.get_class_name(condition=True), alias="t", need_data=False)).indent_decrease()
        if_tag.add_data(")")
        sql_tag.add_tag(if_tag)
        return sql_tag

    @staticmethod
    def __update_null(code_config: CodeConfig):
        """
        根据传入字段置null
        :param code_config:配置
        :return:修改标签
        """
        sql_tag = MapperTag.Update(MapperApi.Update.update_set_null_by_id(code_config))
        sql_tag.add_data(f"UPDATE {MapperUtil.get_table_name(code_config)}")
        set_tag = MapperTag.Set()
        sql_tag.add_tag(set_tag)
        for attr in code_config.baseInfo.attr:
            set_tag.add_tag(MapperTag.If(f'{attr.attr}!=null', f'{attr.field} = NULL,'))
        sql_tag.add_data(f'WHERE {code_config.baseInfo.key.field} = #{{{code_config.baseInfo.key.attr}}}')
        return sql_tag

    @staticmethod
    def create(code_config: CodeConfig, xml_mapper: MapperTag.Mapper):
        if code_config.baseInfo.key is not None:
            # 主键更新
            xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.Update.update_by_id(code_config)))
            xml_mapper.add_tag(UpdateBlock.__update_by_key(code_config)).add_blank_line()
        # 条件更新
        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.Update.update(code_config)))
        xml_mapper.add_tag(UpdateBlock.__update_by_where(code_config)).add_blank_line()
        # 不存在则更新
        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.Update.update_by_not_repeat_where(code_config)))
        xml_mapper.add_tag(UpdateBlock.__update_not_repeat(code_config)).add_blank_line()
        # 设置Null
        if code_config.baseInfo.key is not None:
            xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.Update.update_set_null_by_id(code_config)))
            xml_mapper.add_tag(UpdateBlock.__update_null(code_config)).add_blank_line()


class SelectBlock:
    @staticmethod
    def __select_by_key(code_config: CodeConfig):
        """
        根据id查询
        :param code_config:配置
        :return: Select标签
        """
        sql_tag = MapperTag.Select(MapperApi.Select.select_by_id(code_config))
        BlockTag.set_result(sql_tag, code_config)
        sql_tag.add_data(f'SELECT * FROM {MapperUtil.get_table_name(code_config)} WHERE {code_config.baseInfo.key.field} = #{{{code_config.baseInfo.key.attr}}}')
        return sql_tag

    @staticmethod
    def __select_in_key(code_config: CodeConfig):
        """
        根据多个id查询
        :param code_config:配置
        :return: Select标签
        """
        sql_tag = MapperTag.Select(MapperApi.Select.select_in_id(code_config))
        BlockTag.set_result(sql_tag, code_config)
        sql_tag.add_data(f'SELECT * FROM {MapperUtil.get_table_name(code_config)} WHERE {code_config.baseInfo.key.field} IN').indent_increase()
        sql_tag.add_tag(MapperTag.Foreach(opens="(", close=")").add_data("#{obj}")).indent_decrease()
        return sql_tag

    @staticmethod
    def __select_by_key_and_where(code_config: CodeConfig):
        """
        根据id和其他条件
        :param code_config:配置
        :return: Select标签
        """
        sql_tag = MapperTag.Select(MapperApi.Select.select_in_id_and_where(code_config))
        BlockTag.set_result(sql_tag, code_config)
        sql_tag.add_data(f'SELECT * FROM {MapperUtil.get_table_name(code_config)}')

        where_tag = MapperTag.Where()
        sql_tag.add_tag(where_tag)
        where_tag.add_data(f'{code_config.baseInfo.key.field} IN')
        where_tag.add_tag(MapperTag.Foreach(opens="(", close=")").add_data("#{obj}"))
        where_tag.add_tag(BlockTag.if_select_block(code_config))
        BlockTag.fuzzy_search(code_config, where_tag)
        return sql_tag

    @staticmethod
    def __select_one(code_config: CodeConfig):
        """
        根据id查询
        :param code_config:配置
        :return: Select标签
        """
        sql_tag = MapperTag.Select(MapperApi.Select.select_one(code_config))
        BlockTag.set_result(sql_tag, code_config)
        sql_tag.add_data(f'SELECT * FROM {MapperUtil.get_table_name(code_config)}')

        where_tag = MapperTag.Where()
        sql_tag.add_tag(where_tag)
        where_tag.add_tag(BlockTag.if_select_block(code_config))
        BlockTag.fuzzy_search(code_config, where_tag)
        sql_tag.add_data("LIMIT 1 OFFSET #{index}")
        return sql_tag

    @staticmethod
    def __select(code_config: CodeConfig):
        """
        根据条件查询
        :param code_config:配置
        :return: Select标签
        """
        sql_tag = MapperTag.Select(MapperApi.Select.select(code_config))
        BlockTag.set_result(sql_tag, code_config)
        sql_tag.add_data(f'SELECT * FROM {MapperUtil.get_table_name(code_config)}')

        where_tag = MapperTag.Where()
        sql_tag.add_tag(where_tag)
        where_tag.add_tag(BlockTag.if_select_block(code_config))
        BlockTag.fuzzy_search(code_config, where_tag)
        BlockTag.splicing_sql(code_config, sql_tag)
        sql_tag.add_tag(BlockTag.page_block())
        return sql_tag

    @staticmethod
    def __count(code_config: CodeConfig):
        """
        查询计数
        :param code_config:配置
        :return: Select标签
        """
        sql_tag = MapperTag.Select(MapperApi.Select.count(code_config))
        sql_tag.set_result_type("int")
        sql_tag.add_data(f'SELECT COUNT(*) FROM {MapperUtil.get_table_name(code_config)}')

        where_tag = MapperTag.Where()
        sql_tag.add_tag(where_tag)
        where_tag.add_tag(BlockTag.if_select_block(code_config))
        BlockTag.fuzzy_search(code_config, where_tag)
        return sql_tag

    @staticmethod
    def create(code_config: CodeConfig, xml_mapper: MapperTag.Mapper):
        if code_config.baseInfo.key is not None:
            # 根据ID查询
            xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.Select.select_by_id(code_config)))
            xml_mapper.add_tag(SelectBlock.__select_by_key(code_config)).add_blank_line()
            # 根据多个ID查询
            xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.Select.select_in_id(code_config)))
            xml_mapper.add_tag(SelectBlock.__select_in_key(code_config)).add_blank_line()
            # 根据ID和条件查询
            xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.Select.select_in_id_and_where(code_config)))
            xml_mapper.add_tag(SelectBlock.__select_by_key_and_where(code_config)).add_blank_line()
        # 只查询一个
        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.Select.select_in_id_and_where(code_config)))
        xml_mapper.add_tag(SelectBlock.__select_one(code_config)).add_blank_line()
        # 普通查询
        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.Select.select(code_config)))
        xml_mapper.add_tag(SelectBlock.__select(code_config)).add_blank_line()
        # 普通查询计数
        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.Select.count(code_config)))
        xml_mapper.add_tag(SelectBlock.__count(code_config)).add_blank_line()


class SelectOneToOneBlock:

    @staticmethod
    def __find_select(xml_mapper: MapperTag.Mapper, code_config: CodeConfig, other_config: CodeConfig):
        """
        内联一对一查询
        :param xml_mapper: xml块
        :param code_config:配置
        :param other_config: 另一方配置
        :return:
        """
        sql_tag = MapperTag.Select(MapperApi.SelectOneToOne.find_one_to_one(code_config, other_config))
        BlockTag.set_result(sql_tag, code_config, other_config, one_to_one=True)
        sql_tag.add_data(f'SELECT').indent_increase()
        BlockTag.add_include_tag(sql_tag, code_config, other_config)
        sql_tag.add_data(f'FROM {MapperUtil.get_table_name(code_config)}, {MapperUtil.get_table_name(other_config)}').indent_decrease()

        where_tag = MapperTag.Where()
        sql_tag.add_tag(where_tag)
        # 关联条件
        # 一对一中，对方的外键就指向我方的字段
        where_tag.add_data(f'{code_config.baseInfo.tableName}.{other_config.baseInfo.foreignKey} = {other_config.baseInfo.tableName}.{code_config.baseInfo.key.field}')
        where_tag.add_tag(BlockTag.if_select_block(code_config, alias=code_config.baseInfo.get_table_alias()))
        where_tag.add_tag(BlockTag.if_select_block(other_config, alias=other_config.baseInfo.get_table_alias()))

        BlockTag.fuzzy_search(code_config, where_tag, code_config.baseInfo.get_table_alias())
        BlockTag.fuzzy_search(other_config, where_tag, other_config.baseInfo.get_table_alias(), "1")
        BlockTag.splicing_sql(code_config, sql_tag)
        sql_tag.add_tag(BlockTag.page_block())

        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.SelectOneToOne.find_one_to_one(other_config)))
        xml_mapper.add_tag(sql_tag).add_blank_line()

    @staticmethod
    def __find_count(xml_mapper: MapperTag.Mapper, code_config: CodeConfig, other_config: CodeConfig):
        """
        一对一内联计数
        :param xml_mapper: 标签
        :param code_config: 配置
        :param other_config: 另一方配置
        """
        sql_tag = MapperTag.Select(MapperApi.SelectOneToOne.count_find_one_to_one(code_config, other_config))
        sql_tag.set_result_type("int")
        sql_tag.add_data(f'SELECT COUNT(*) FROM {MapperUtil.get_table_name(code_config)}, {MapperUtil.get_table_name(other_config)}')

        where_tag = MapperTag.Where()
        sql_tag.add_tag(where_tag)
        # 关联条件
        # 一对一中，对方的外键就指向我方的字段
        where_tag.add_data(f'{code_config.baseInfo.tableName}.{other_config.baseInfo.foreignKey} = {other_config.baseInfo.tableName}.{code_config.baseInfo.key.field}')
        where_tag.add_tag(BlockTag.if_select_block(code_config, alias=code_config.baseInfo.get_table_alias()))
        where_tag.add_tag(BlockTag.if_select_block(other_config, alias=other_config.baseInfo.get_table_alias()))

        BlockTag.fuzzy_search(code_config, where_tag, code_config.baseInfo.get_table_alias())
        BlockTag.fuzzy_search(other_config, where_tag, other_config.baseInfo.get_table_alias(), "1")

        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.SelectOneToOne.count_find_one_to_one(code_config)))
        xml_mapper.add_tag(sql_tag).add_blank_line()

    @staticmethod
    def __query_select(xml_mapper: MapperTag.Mapper, code_config: CodeConfig, other_config: CodeConfig):
        """
        一对一外联
        :param xml_mapper:标签
        :param code_config: 配置
        :param other_config: 其他配置
        """
        sql_tag = MapperTag.Select(MapperApi.SelectOneToOne.query_one_to_one(code_config, other_config))
        BlockTag.set_result(sql_tag, code_config, other_config, one_to_one=True)

        sql_tag.add_data(f'SELECT * FROM (').indent_increase()
        # 左临时表查询
        sql_tag.add_data(f"SELECT * FROM {MapperUtil.get_table_name(code_config)}")
        sql_tag.add_tag(BlockTag.where_if_block(code_config, need_var=True))
        BlockTag.fuzzy_search(code_config, sql_tag, code_config.baseInfo.get_table_alias())

        sql_tag.add_tag(BlockTag.page_block()).indent_decrease()

        sql_tag.add_data(f') AS temp_{code_config.baseInfo.tableName} LEFT JOIN (').indent_increase()
        # 右临时表查询
        if other_config.baseInfo.need_sql_block():
            sql_tag.add_data(f"SELECT").indent_increase()
            BlockTag.add_include_tag(sql_tag, other_config)
            sql_tag.indent_decrease()
            sql_tag.add_data(f'FROM {MapperUtil.get_table_name(other_config)}')
        else:
            sql_tag.add_data(f"SELECT * FROM {MapperUtil.get_table_name(other_config)}")
        sql_tag.add_tag(BlockTag.where_if_block(other_config, need_var=True))
        BlockTag.fuzzy_search(other_config, sql_tag, other_config.baseInfo.get_table_alias(), "1")
        sql_tag.add_tag(BlockTag.page_block("page1")).indent_decrease()
        sql_tag.add_data(f") AS temp_{other_config.baseInfo.tableName}")
        sql_tag.add_data(f'ON temp_{code_config.baseInfo.tableName}.{code_config.baseInfo.key.field} = temp_{other_config.baseInfo.tableName}.{other_config.baseInfo.foreignKey}')
        BlockTag.splicing_sql(code_config, sql_tag)

        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.SelectOneToOne.query_one_to_one(other_config)))
        xml_mapper.add_tag(sql_tag).add_blank_line()

    @staticmethod
    def __query_count(xml_mapper: MapperTag.Mapper, code_config: CodeConfig, other_config: CodeConfig):
        """
        一对一外联计数
        :param xml_mapper:标签
        :param code_config: 配置
        :param other_config: 其他配置
        """
        sql_tag = MapperTag.Select(MapperApi.SelectOneToOne.count_query_one_to_one(code_config, other_config))
        sql_tag.set_result_type("int")
        sql_tag.add_data(f'SELECT COUNT(DISTINCT temp_{code_config.baseInfo.tableName}.{code_config.baseInfo.key.field}) FROM (').indent_increase()
        # 左临时表查询
        sql_tag.add_data(f"SELECT * FROM {MapperUtil.get_table_name(code_config)}")
        sql_tag.add_tag(BlockTag.where_if_block(code_config, need_var=True))
        BlockTag.fuzzy_search(code_config, sql_tag, code_config.baseInfo.get_table_alias())
        sql_tag.add_tag(BlockTag.page_block()).indent_decrease()

        sql_tag.add_data(f') AS temp_{code_config.baseInfo.tableName} LEFT JOIN (').indent_increase()
        # 右临时表查询
        if other_config.baseInfo.need_sql_block():
            sql_tag.add_data(f"SELECT").indent_increase()
            BlockTag.add_include_tag(sql_tag, other_config)
            sql_tag.indent_decrease()
            sql_tag.add_data(f'FROM {MapperUtil.get_table_name(other_config)}')
        else:
            sql_tag.add_data(f"SELECT * FROM {MapperUtil.get_table_name(other_config)}")
        sql_tag.add_tag(BlockTag.where_if_block(other_config, need_var=True))
        BlockTag.fuzzy_search(other_config, sql_tag, other_config.baseInfo.get_table_alias(), "1")
        sql_tag.add_tag(BlockTag.page_block("page1")).indent_decrease()
        sql_tag.add_data(f") AS temp_{other_config.baseInfo.tableName}")
        sql_tag.add_data(f'ON temp_{code_config.baseInfo.tableName}.{code_config.baseInfo.key.field} = temp_{other_config.baseInfo.tableName}.{other_config.baseInfo.foreignKey}')

        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.SelectOneToOne.count_query_one_to_one(other_config)))
        xml_mapper.add_tag(sql_tag).add_blank_line()

    @staticmethod
    def __link_select(xml_mapper: MapperTag.Mapper, code_config: CodeConfig, other_config: CodeConfig):
        """
        一对一内联，只查另一方
        :param xml_mapper: xml块
        :param code_config:配置
        :param other_config: 另一方配置
        :return:
        """
        sql_tag = MapperTag.Select(MapperApi.SelectOneToOne.link_one_to_one(other_config))
        BlockTag.set_result(sql_tag, other_config)
        sql_tag.add_data(f'SELECT {other_config.baseInfo.tableName}.* FROM {MapperUtil.get_table_name(code_config)}, {MapperUtil.get_table_name(other_config)}')

        where_tag = MapperTag.Where()
        sql_tag.add_tag(where_tag)
        # 关联条件
        # 一对一中，对方的外键就指向我方的字段
        where_tag.add_data(f'{code_config.baseInfo.tableName}.{other_config.baseInfo.foreignKey} = {other_config.baseInfo.tableName}.{code_config.baseInfo.key.field}')
        where_tag.add_tag(BlockTag.if_select_block(code_config, alias=code_config.baseInfo.tableName))
        where_tag.add_tag(BlockTag.if_select_block(other_config, alias=other_config.baseInfo.tableName))

        BlockTag.fuzzy_search(code_config, where_tag, code_config.baseInfo.get_table_alias())
        BlockTag.fuzzy_search(other_config, where_tag, other_config.baseInfo.get_table_alias(), "1")
        BlockTag.splicing_sql(code_config, sql_tag)
        sql_tag.add_tag(BlockTag.page_block())

        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.SelectOneToOne.link_one_to_one(code_config, other_config)))
        xml_mapper.add_tag(sql_tag).add_blank_line()

    @staticmethod
    def create(code_config: CodeConfig, xml_mapper: MapperTag.Mapper):
        if code_config.baseInfo.key is not None:
            for one_to_one in code_config.baseInfo.oneToOne:
                xml_mapper.add_tag(MapperTag.LineNote("一对一查询块"))
                SelectOneToOneBlock.__find_select(xml_mapper, code_config, one_to_one)
                SelectOneToOneBlock.__find_count(xml_mapper, code_config, one_to_one)
                SelectOneToOneBlock.__query_select(xml_mapper, code_config, one_to_one)
                SelectOneToOneBlock.__query_count(xml_mapper, code_config, one_to_one)
                SelectOneToOneBlock.__link_select(xml_mapper, code_config, one_to_one)


class SelectOneToManyBlock:
    @staticmethod
    def __find_select(xml_mapper: MapperTag.Mapper, code_config: CodeConfig, other_config: CodeConfig):
        """
        内联一对一查询
        :param xml_mapper: xml块
        :param code_config:配置
        :param other_config: 另一方配置
        :return:
        """

        sql_tag = MapperTag.Select(MapperApi.SelectOneToMany.find_one_to_many(code_config, other_config))
        BlockTag.set_result(sql_tag, code_config, other_config, one_to_many=True)

        sql_tag.add_data(f'SELECT * FROM (').indent_increase()
        # 左临时表查询
        sql_tag.add_data(f"SELECT * FROM {MapperUtil.get_table_name(code_config)}")
        sql_tag.add_tag(BlockTag.where_if_block(code_config, need_var=True))
        BlockTag.fuzzy_search(code_config, sql_tag, code_config.baseInfo.get_table_alias())
        sql_tag.add_tag(BlockTag.page_block("onePage")).indent_decrease()

        sql_tag.add_data(f') AS temp_{code_config.baseInfo.tableName}, (').indent_increase()
        if other_config.baseInfo.need_sql_block():
            sql_tag.add_data(f"SELECT").indent_increase()
            BlockTag.add_include_tag(sql_tag, other_config)
            sql_tag.indent_decrease()
            sql_tag.add_data(f'FROM {MapperUtil.get_table_name(other_config)}')
        else:
            sql_tag.add_data(f"SELECT * FROM {MapperUtil.get_table_name(other_config)}")
        sql_tag.add_tag(BlockTag.where_if_block(other_config, need_var=True))
        BlockTag.fuzzy_search(other_config, sql_tag, other_config.baseInfo.get_table_alias(), "1")
        sql_tag.add_tag(BlockTag.page_block("manyPage")).indent_decrease()
        sql_tag.add_data(f") AS temp_{other_config.baseInfo.tableName}")
        sql_tag.add_data("WHERE").indent_increase()
        sql_tag.add_data(f'temp_{code_config.baseInfo.tableName}.{code_config.baseInfo.key.field} = temp_{other_config.baseInfo.tableName}.{other_config.baseInfo.foreignKey}').indent_decrease()
        BlockTag.splicing_sql(code_config, sql_tag)

        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.SelectOneToMany.find_one_to_many(other_config)))
        xml_mapper.add_tag(sql_tag).add_blank_line()

    @staticmethod
    def __find_count(xml_mapper: MapperTag.Mapper, code_config: CodeConfig, other_config: CodeConfig):
        """
        一对一内联计数
        :param xml_mapper: 标签
        :param code_config: 配置
        :param other_config: 另一方配置
        """
        sql_tag = MapperTag.Select(MapperApi.SelectOneToMany.count_find_one_to_many(code_config, other_config))
        sql_tag.set_result_type("int")

        sql_tag.add_data(f'SELECT count(*) FROM (').indent_increase()
        # 左临时表查询
        sql_tag.add_data(f"SELECT * FROM {MapperUtil.get_table_name(code_config)}")
        sql_tag.add_tag(BlockTag.where_if_block(code_config, need_var=True))
        BlockTag.fuzzy_search(code_config, sql_tag, code_config.baseInfo.get_table_alias())
        sql_tag.add_tag(BlockTag.page_block("onePage")).indent_decrease()

        sql_tag.add_data(f') AS temp_{code_config.baseInfo.tableName}, (').indent_increase()
        if other_config.baseInfo.need_sql_block():
            sql_tag.add_data(f"SELECT").indent_increase()
            BlockTag.add_include_tag(sql_tag, other_config)
            sql_tag.indent_decrease()
            sql_tag.add_data(f'FROM {MapperUtil.get_table_name(other_config)}')
        else:
            sql_tag.add_data(f"SELECT * FROM {MapperUtil.get_table_name(other_config)}")
        sql_tag.add_tag(BlockTag.where_if_block(other_config, need_var=True))
        BlockTag.fuzzy_search(other_config, sql_tag, other_config.baseInfo.get_table_alias(), "1")
        sql_tag.add_tag(BlockTag.page_block("manyPage")).indent_decrease()
        sql_tag.add_data(f") AS temp_{other_config.baseInfo.tableName}")
        sql_tag.add_data("WHERE").indent_increase()
        sql_tag.add_data(f'temp_{code_config.baseInfo.tableName}.{code_config.baseInfo.key.field} = temp_{other_config.baseInfo.tableName}.{other_config.baseInfo.foreignKey}').indent_decrease()
        BlockTag.splicing_sql(code_config, sql_tag)

        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.SelectOneToMany.count_find_one_to_many(code_config)))
        xml_mapper.add_tag(sql_tag).add_blank_line()

    @staticmethod
    def __query_select(xml_mapper: MapperTag.Mapper, code_config: CodeConfig, other_config: CodeConfig):
        """
        一对一外联
        :param xml_mapper:标签
        :param code_config: 配置
        :param other_config: 其他配置
        """
        sql_tag = MapperTag.Select(MapperApi.SelectOneToMany.query_one_to_many(code_config, other_config))
        BlockTag.set_result(sql_tag, code_config, other_config, one_to_many=True)

        sql_tag.add_data(f'SELECT * FROM (').indent_increase()
        # 左临时表查询
        sql_tag.add_data(f"SELECT * FROM {MapperUtil.get_table_name(code_config)}")
        sql_tag.add_tag(BlockTag.where_if_block(code_config, need_var=True))
        BlockTag.fuzzy_search(code_config, sql_tag, code_config.baseInfo.get_table_alias())
        sql_tag.add_tag(BlockTag.page_block("onePage")).indent_decrease()

        sql_tag.add_data(f') AS temp_{code_config.baseInfo.tableName} LEFT JOIN (').indent_increase()
        # 右临时表查询
        if other_config.baseInfo.need_sql_block():
            sql_tag.add_data(f"SELECT").indent_increase()
            BlockTag.add_include_tag(sql_tag, other_config)
            sql_tag.indent_decrease()
            sql_tag.add_data(f'FROM {MapperUtil.get_table_name(other_config)}')
        else:
            sql_tag.add_data(f"SELECT * FROM {MapperUtil.get_table_name(other_config)}")
        sql_tag.add_tag(BlockTag.where_if_block(other_config, need_var=True))
        BlockTag.fuzzy_search(other_config, sql_tag, other_config.baseInfo.get_table_alias(), "1")
        sql_tag.add_tag(BlockTag.page_block("ManyPage")).indent_decrease()
        sql_tag.add_data(f") AS temp_{other_config.baseInfo.tableName}")
        sql_tag.add_data(f'ON temp_{code_config.baseInfo.tableName}.{code_config.baseInfo.key.field} = temp_{other_config.baseInfo.tableName}.{other_config.baseInfo.foreignKey}')
        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.SelectOneToMany.query_one_to_many(other_config)))
        BlockTag.splicing_sql(code_config, sql_tag)
        xml_mapper.add_tag(sql_tag).add_blank_line()

    @staticmethod
    def __query_count(xml_mapper: MapperTag.Mapper, code_config: CodeConfig, other_config: CodeConfig):
        """
        一对一外联计数
        :param xml_mapper:标签
        :param code_config: 配置
        :param other_config: 其他配置
        """
        sql_tag = MapperTag.Select(MapperApi.SelectOneToMany.count_query_one_to_many(code_config, other_config))
        sql_tag.set_result_type("int")
        sql_tag.add_data(f'SELECT COUNT(DISTINCT temp_{code_config.baseInfo.tableName}.{code_config.baseInfo.key.field}) FROM (').indent_increase()
        # 左临时表查询
        sql_tag.add_data(f"SELECT * FROM {MapperUtil.get_table_name(code_config)}")
        sql_tag.add_tag(BlockTag.where_if_block(code_config, need_var=True))
        BlockTag.fuzzy_search(code_config, sql_tag, code_config.baseInfo.get_table_alias())

        sql_tag.add_tag(BlockTag.page_block("onePage")).indent_decrease()

        sql_tag.add_data(f') AS temp_{code_config.baseInfo.tableName} LEFT JOIN (').indent_increase()
        # 右临时表查询
        if other_config.baseInfo.need_sql_block():
            sql_tag.add_data(f"SELECT").indent_increase()
            BlockTag.add_include_tag(sql_tag, other_config)
            sql_tag.indent_decrease()
            sql_tag.add_data(f'FROM {MapperUtil.get_table_name(other_config)}')
        else:
            sql_tag.add_data(f"SELECT * FROM {MapperUtil.get_table_name(other_config)}")
        sql_tag.add_tag(BlockTag.where_if_block(other_config, need_var=True))
        BlockTag.fuzzy_search(other_config, sql_tag, other_config.baseInfo.get_table_alias(), "1")
        sql_tag.add_tag(BlockTag.page_block("manyPage")).indent_decrease()
        sql_tag.add_data(f") AS temp_{other_config.baseInfo.tableName}")
        sql_tag.add_data(f'ON temp_{code_config.baseInfo.tableName}.{code_config.baseInfo.key.field} = temp_{other_config.baseInfo.tableName}.{other_config.baseInfo.foreignKey}')
        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.SelectOneToMany.count_query_one_to_many(other_config)))
        xml_mapper.add_tag(sql_tag).add_blank_line()

    @staticmethod
    def __link_select(xml_mapper: MapperTag.Mapper, code_config: CodeConfig, other_config: CodeConfig):
        """
        一对一内联只查另一方
        :param xml_mapper: xml块
        :param code_config:配置
        :param other_config: 另一方配置
        :return:
        """
        sql_tag = MapperTag.Select(MapperApi.SelectOneToMany.link_one_to_many(other_config))
        BlockTag.set_result(sql_tag, other_config)
        sql_tag.add_data(f'SELECT {other_config.baseInfo.tableName}.* FROM {MapperUtil.get_table_name(code_config)}, {MapperUtil.get_table_name(other_config)}')

        where_tag = MapperTag.Where()
        sql_tag.add_tag(where_tag)
        # 关联条件
        # 一对一中，对方的外键就指向我方的字段
        where_tag.add_data(f'{code_config.baseInfo.tableName}.{code_config.baseInfo.key.field} = {other_config.baseInfo.tableName}.{other_config.baseInfo.foreignKey}')
        where_tag.add_tag(BlockTag.if_select_block(code_config, alias=code_config.baseInfo.tableName))
        where_tag.add_tag(BlockTag.if_select_block(other_config, alias=other_config.baseInfo.tableName))

        BlockTag.fuzzy_search(code_config, where_tag, code_config.baseInfo.get_table_alias())
        BlockTag.fuzzy_search(other_config, where_tag, other_config.baseInfo.get_table_alias(), "1")
        BlockTag.splicing_sql(code_config, sql_tag)
        sql_tag.add_tag(BlockTag.page_block())

        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.SelectOneToMany.link_one_to_many(code_config, other_config)))
        xml_mapper.add_tag(sql_tag).add_blank_line()

    @staticmethod
    def create(code_config: CodeConfig, xml_mapper: MapperTag.Mapper):
        if code_config.baseInfo.key is not None:
            for one_to_many in code_config.baseInfo.oneToMany:
                xml_mapper.add_tag(MapperTag.LineNote("一对多查询块"))
                SelectOneToManyBlock.__find_select(xml_mapper, code_config, one_to_many)
                SelectOneToManyBlock.__find_count(xml_mapper, code_config, one_to_many)
                SelectOneToManyBlock.__query_select(xml_mapper, code_config, one_to_many)
                SelectOneToManyBlock.__query_count(xml_mapper, code_config, one_to_many)
                SelectOneToManyBlock.__link_select(xml_mapper, code_config, one_to_many)


class SelectManyToManyBlock:
    @staticmethod
    def __find_select(xml_mapper: MapperTag.Mapper, code_config: CodeConfig, middle_config: CodeConfig, many_config: CodeConfig):
        """
        内联多对多查询
        :param xml_mapper: xml块
        :param code_config:配置
        :param middle_config: 中间配置
        :param many_config:多的配置
        :return:
        """
        sql_tag = MapperTag.Select(MapperApi.SelectManyToMany.find_many_to_many(code_config, middle_config, many_config))
        BlockTag.set_result(sql_tag, code_config, many_config, many_to_many=True)
        sql_tag.add_data(f'SELECT')
        if many_config.baseInfo.need_sql_block():
            BlockTag.add_include_tag(sql_tag, code_config, many_config)
        else:
            sql_tag.indent_increase().add_data("*").indent_decrease()
        sql_tag.add_data(f'FROM (').indent_increase()
        # 单表临时表查询
        sql_tag.add_data(f'SELECT * FROM {code_config.baseInfo.tableName}')
        where_tag = MapperTag.Where()
        sql_tag.add_tag(where_tag)
        where_tag.add_tag(BlockTag.if_select_block(code_config, alias=code_config.baseInfo.tableName))
        BlockTag.fuzzy_search(code_config, where_tag, code_config.baseInfo.get_table_alias())
        sql_tag.add_tag(BlockTag.page_block()).indent_decrease()
        # 其他表
        sql_tag.add_data(f") AS temp_{code_config.baseInfo.tableName}, {middle_config.baseInfo.tableName}, {many_config.baseInfo.tableName}")
        sql_tag.add_data("WHERE").indent_increase()
        sql_tag.add_data(f'temp_{code_config.baseInfo.tableName}.{code_config.baseInfo.key.field} = {middle_config.baseInfo.tableName}.{middle_config.baseInfo.foreignKey}')
        sql_tag.add_data(f'AND {middle_config.baseInfo.tableName}.{many_config.baseInfo.foreignKey} = {many_config.baseInfo.tableName}.{many_config.baseInfo.key.field}')
        sql_tag.indent_decrease()
        BlockTag.splicing_sql(code_config, sql_tag)
        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.SelectManyToMany.find_many_to_many(code_config, middle_config, many_config)))
        xml_mapper.add_tag(sql_tag).add_blank_line()

    @staticmethod
    def __query_select(xml_mapper: MapperTag.Mapper, code_config: CodeConfig, middle_config: CodeConfig, many_config: CodeConfig):
        """
        内联一对一查询
        :param xml_mapper: xml块
        :param code_config:配置
        :param middle_config: 中间配置
        :param many_config:多的配置
        :return:
        """
        sql_tag = MapperTag.Select(MapperApi.SelectManyToMany.query_many_to_many(code_config, middle_config, many_config))
        BlockTag.set_result(sql_tag, code_config, many_config, many_to_many=True)
        sql_tag.add_data(f'SELECT')
        if many_config.baseInfo.need_sql_block():
            BlockTag.add_include_tag(sql_tag, code_config, many_config)
        else:
            sql_tag.indent_increase().add_data("*").indent_decrease()
        sql_tag.add_data(f'FROM (').indent_increase()
        # 单表临时表查询
        sql_tag.add_data(f'SELECT * FROM {code_config.baseInfo.tableName}')
        where_tag = MapperTag.Where()
        sql_tag.add_tag(where_tag)
        where_tag.add_tag(BlockTag.if_select_block(code_config, alias=code_config.baseInfo.tableName))
        BlockTag.fuzzy_search(code_config, where_tag, code_config.baseInfo.get_table_alias())
        sql_tag.add_tag(BlockTag.page_block()).indent_decrease()
        # 其他表
        sql_tag.add_data(f") AS temp_{code_config.baseInfo.tableName} LEFT JOIN {middle_config.baseInfo.tableName}").indent_increase()
        sql_tag.add_data(f"ON temp_{code_config.baseInfo.tableName}.{code_config.baseInfo.key.field} = {middle_config.baseInfo.tableName}.{middle_config.baseInfo.foreignKey}").indent_decrease()
        sql_tag.add_data(f"{middle_config.baseInfo.tableName} LEFT JOIN {many_config.baseInfo.tableName}").indent_increase()
        sql_tag.add_data(f'ON {middle_config.baseInfo.tableName}.{many_config.baseInfo.foreignKey} = {many_config.baseInfo.tableName}.{many_config.baseInfo.key.field}').indent_decrease()

        BlockTag.splicing_sql(code_config, sql_tag)

        xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.SelectManyToMany.query_many_to_many(code_config, middle_config, many_config)))
        xml_mapper.add_tag(sql_tag).add_blank_line()

    @staticmethod
    def create(code_config: CodeConfig, xml_mapper: MapperTag.Mapper):
        if code_config.baseInfo.key is not None:
            for many_to_many in code_config.baseInfo.manyToMany:
                xml_mapper.add_tag(MapperTag.LineNote("多对多查询块"))
                SelectManyToManyBlock.__find_select(xml_mapper, code_config, many_to_many.to, many_to_many.many)
                SelectManyToManyBlock.__query_select(xml_mapper, code_config, many_to_many.to, many_to_many.many)


class SelectInForeignKey:

    @staticmethod
    def create(code_config: CodeConfig, xml_mapper: MapperTag.Mapper):
        if code_config.baseInfo.key is not None:
            create_name = set()
            for one_to_one in code_config.baseInfo.oneToOne:
                field = None
                for attr in code_config.baseInfo.attr:
                    if attr.field == one_to_one.baseInfo.foreignKey:
                        field = attr
                        break
                if field is None or field.field in create_name:
                    continue
                create_name.add(field.field)
                sql_tag = MapperTag.Select(MapperApi.SelectForeignKey.select_in_and_where(code_config, field))
                BlockTag.set_result(sql_tag, code_config)
                sql_tag.add_data(f'SELECT * FROM {MapperUtil.get_table_name(code_config)}')
                where_tag = MapperTag.Where()
                sql_tag.add_tag(where_tag)
                where_tag.add_data(f'{field.field} IN')
                where_tag.add_tag(MapperTag.Foreach(opens="(", close=")").add_data("#{obj}"))
                where_tag.add_tag(BlockTag.if_select_block(code_config))
                BlockTag.fuzzy_search(code_config, where_tag)

                xml_mapper.add_tag(MapperTag.LineNote(MapperApiNote.SelectForeignKey.select_in_and_where(code_config, field)))
                xml_mapper.add_tag(sql_tag).add_blank_line()
