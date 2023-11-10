from src.analsis.AnalysisConfig import AnalysisConfig
from src.analsis.ParserConfig import ParserConfig
from src.code.generateCode import Generate

# 配置，参数建该类
init_config = AnalysisConfig()
init_config.project_name = "chiya.test"
init_config.database_name = "chiya_test"
init_config.database_port = 3307
init_config.use_default_flow()
init_config.create_default_all_file()

# 生成配置
ParserConfig.create(init_config)

# 生成代码
Generate().generate()
