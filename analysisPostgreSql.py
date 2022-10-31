from src.constant.PublicConstant import Constant
from src.service.analysis.ConditionalAssembly import ConditionalAssembly
from src.service.analysis.CreateConfig import CreateConfig
from src.service.analysis.MySQLAnalysis import StructureAnalysis, AnalysisConfig
from src.service.analysis.PostgreSQLAnalysis import PostgreSQLAnalysis
from src.structure.CreateConfig import FileType

postgreSQL = PostgreSQLAnalysis("test", "TEST", password="P@ssw0rd", host="127.0.0.1", port=5432)
l = postgreSQL.to_mysql_list_table()
s = StructureAnalysis(l, AnalysisConfig())
tables = s.parsing_field()

# for name in tables:
#     print(tables[name])

create_file = [
    FileType.controller,
    FileType.service,
    FileType.serviceImpl,
    FileType.javaMapper,
    FileType.javaBaseMapper,
    FileType.xmlMapper,
    FileType.xmlBaseMapper,
    FileType.entity,
    FileType.entityBase,

    FileType.domain,
    FileType.domainImpl,
    FileType.repository,
    FileType.repositoryImpl,
    # FileType.cache,
]
config = {
    Constant.MULTI_TABLE: True,
    Constant.UNDERSCORE_REPLACE: True,
    Constant.PROJECT: "com.example.demo.module",
    Constant.CREATE_MODEL: "ddd",
    Constant.CREATE_FILE: create_file,
    Constant.TABLE_PREFIX: True,
    Constant.RESTFUL: False,
    "repositoryUseCache": False,
    Constant.EXTRA_API: False,
    "databaseName": "test"
}
# 装配配置
ConditionalAssembly.assembly(tables, config)
# 解析映射
CreateConfig.create(tables, config)
# 生成
CreateConfig.save_model_json(tables)
