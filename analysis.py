from src.constant.PublicConstant import Constant
from src.service.analysis.ConditionalAssembly import ConditionalAssembly
from src.service.analysis.CreateConfig import CreateConfig
from src.service.analysis.MySQLAnalysis import MySQLAnalysis, StructureAnalysis, AnalysisConfig
from src.service.generate.generateAnalysis import FileType

mySQL = MySQLAnalysis("chiya_test", port=3307)
l = mySQL.get_all_table()
s = StructureAnalysis(l, AnalysisConfig())
tables = s.parsing_field()

create_file = [
    FileType.controller,
    FileType.service,
    FileType.serviceImpl,
    FileType.javaMapper,
    FileType.javaBaseMapper,
    FileType.xmlMapper,
    FileType.xmlBaseMapper,
    FileType.entity,
    FileType.entityBase
]
config = {
    Constant.MULTI_TABLE: True,
    Constant.UNDERSCORE_REPLACE: True,
    Constant.PROJECT: "chiya.galgame.teahouse.module",
    Constant.CREATE_MODEL: "mvcSuperModel",
    Constant.CREATE_FILE: create_file,
    Constant.TABLE_PREFIX: True,
}
# 装配配置
ConditionalAssembly.assembly(tables, config)
# 解析映射
CreateConfig.create(tables, config)
# 生成
CreateConfig.save_model_json(tables)
