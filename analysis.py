from src.constant.PublicConstant import Constant
from src.service.analysis.ConditionalAssembly import ConditionalAssembly
from src.service.analysis.CreateConfig import CreateConfig
from src.service.analysis.MySQLAnalysis import MySQLAnalysis, StructureAnalysis, AnalysisConfig

mySQL = MySQLAnalysis("bbs")
l = mySQL.get_all_table()
s = StructureAnalysis(l, AnalysisConfig())
tables = s.parsing_field()

config = {
    Constant.MULTI_TABLE: True,
    Constant.UNDERSCORE_REPLACE: True,
    Constant.PROJECT: "com.test"
}

ConditionalAssembly.assembly(tables, config)
CreateConfig.create(tables, config)

CreateConfig.save_model_json(tables)
