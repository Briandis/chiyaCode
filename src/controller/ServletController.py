import json

from src.constant.PublicConstant import Constant
from src.httpServer.HttpRequest import HttpRequest
from src.httpServer.HttpResponse import HttpResponse
from src.httpServer.Servlet import Servlet
from src.project import createProject
from src.service.analysis.ConditionalAssembly import ConditionalAssembly
from src.service.analysis.CreateConfig import CreateConfig
from src.service.analysis.MySQLAnalysis import MySQLAnalysis, AnalysisConfig, StructureAnalysis
from src.service.generate import dddGenerateAnalysis, generateAnalysis


class LinkMySqlServlet(Servlet):

    def servlet(self, httpRequest: HttpRequest, httpResponse: HttpResponse):
        try:
            host = httpRequest.get_param("host")
            name = httpRequest.get_param("name")
            password = httpRequest.get_param("password")
            port = httpRequest.get_param("port")
            database = httpRequest.get_param("database")
            port = int(port)
            mysql = MySQLAnalysis(database, host=host, name=name, password=password, port=port)
            tables = mysql.get_all_table()
            print(f"查询到表数量：{len(tables)}")
            s = StructureAnalysis(tables, AnalysisConfig())
            # 解析表字段成可以识别字段
            tables = s.parsing_field()

            httpResponse.write_body(json.dumps({"code": 200, "data": tables}))
        except:
            httpResponse.write_body('{"code":"-1"}')


class CreateConfigServlet(Servlet):
    @staticmethod
    def create_config(mySQL, config, create_list, not_create_list):
        """
        生成配置
        :param mySQL : 数据库连接
        :param config: 生成的配置
        :param create_list: 生成的列表
        :param not_create_list: 不生成的列表
        """
        # 创建连接
        # 获取全部的表
        l = mySQL.get_all_table()
        beanConfig = AnalysisConfig()
        beanConfig.assembly_config({
        })

        # 构建解析对象
        s = StructureAnalysis(l, beanConfig)
        # 解析表字段成可以识别字段
        tables = s.parsing_field()
        # 解析
        ConditionalAssembly.assembly(tables, config)
        # 构建配置
        CreateConfig.create(tables, config)
        # 根据配置文件生成
        CreateConfig.save_model_json(tables, create_list, not_create_list)

    def servlet(self, httpRequest: HttpRequest, httpResponse: HttpResponse):
        # 获取创建的文件列表
        create_table = httpRequest.get_param("createTable")
        not_create_table = httpRequest.get_param("notCreateTable")
        create_list = httpRequest.get_param("createList")
        create_model = httpRequest.get_param("createModel")
        project = httpRequest.get_param("project")
        config = {
            Constant.MULTI_TABLE: True,
            Constant.UNDERSCORE_REPLACE: True,
            Constant.PROJECT: project,
            Constant.CREATE_FILE: create_list,
            Constant.CREATE_MODEL: create_model
        }
        host = httpRequest.get_param("host")
        name = httpRequest.get_param("name")
        password = httpRequest.get_param("password")
        port = httpRequest.get_param("port")
        database = httpRequest.get_param("database")
        port = int(port)
        try:
            mysql = MySQLAnalysis(database, host=host, name=name, password=password, port=port)
            CreateConfigServlet.create_config(mysql, config, create_table, not_create_table)
            httpResponse.write_body('{"code":"200"}')
        except:
            httpResponse.write_body('{"code":"-1"}')


class GenerateDDD(Servlet):

    def servlet(self, httpRequest: HttpRequest, httpResponse: HttpResponse):
        try:
            dddGenerateAnalysis.Generate().generate()
            httpResponse.write_body(json.dumps({"code": 200}))
        except:
            httpResponse.write_body('{"code":"-1"}')


class GenerateModel(Servlet):

    def servlet(self, httpRequest: HttpRequest, httpResponse: HttpResponse):
        try:
            generateAnalysis.Generate().generate()
            httpResponse.write_body(json.dumps({"code": 200}))
        except:
            httpResponse.write_body('{"code":"-1"}')


class ProjectInit(Servlet):

    def servlet(self, httpRequest: HttpRequest, httpResponse: HttpResponse):
        try:
            createProject.init(httpRequest.get_param("project"))
            httpResponse.write_body(json.dumps({"code": 200}))
        except:
            httpResponse.write_body('{"code":"-1"}')
