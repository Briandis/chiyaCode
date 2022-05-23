import os
import shutil
import traceback
import json

from src.httpServer.HttpRequest import HttpRequest
from src.httpServer.HttpResponse import HttpResponse
from src.httpServer.Servlet import Servlet
from src.service.analysis.MySQLAnalysis import MySQLAnalysis, AnalysisConfig, StructureAnalysis


class LinkMySqlServlet(Servlet):

    def servlet(self, httpRequest: HttpRequest, httpResponse: HttpResponse):

        host = httpRequest.get_param("host")
        name = httpRequest.get_param("name")
        password = httpRequest.get_param("password")
        port = httpRequest.get_param("port")
        database = httpRequest.get_param("database")
        port = int(port)
        try:
            mysql = MySQLAnalysis(database, host=host, name=name, password=password, port=port)
            tables = mysql.get_all_table()
            print(f"查询到表数量：{len(tables)}")
            s = StructureAnalysis(tables, AnalysisConfig())
            # 解析表字段成可以识别字段
            tables = s.parsing_field()

            httpResponse.write_body(json.dumps({"code": 200, "data": tables}))
        except:
            # traceback.print_exc()
            httpResponse.write_body('{"code":"-1"}')

#
# class CreateConfigServlet(Servlet):
#     def servlet(self, httpRequest: HttpRequest, httpResponse: HttpResponse):
#         data = httpRequest.get_param("data")
#         try:
#             with open("config.json", "w", encoding="utf-8") as file:
#                 file.write(data)
#             httpResponse.write_body(json.dumps({"code": 200}))
#         except:
#             httpResponse.write_body(json.dumps({"code": -1, "msg": "配置文件错误"}))
#
#
# class CreateOneServlet(Servlet):
#     def servlet(self, httpRequest: HttpRequest, httpResponse: HttpResponse):
#         if os.path.exists(os.path.join(os.getcwd(), "config.json")):
#             try:
#                 data = json.load(open("config.json", encoding="utf-8"))
#                 analysis = SQLLinkUtil(data)
#                 analysis.get_all_table()
#                 analysis.mapping_relations()
#                 analysis.save_model_json()
#             except:
#                 httpResponse.write_body(json.dumps({"code": -1, "msg": "配置文件生成错误"}))
#                 return
#             try:
#                 g = Generate()
#                 g.generate()
#                 httpResponse.write_body(json.dumps({"code": 200}))
#             except Exception:
#                 traceback.print_exc()
#                 httpResponse.write_body(json.dumps({"code": -1, "msg": "代码生成错误"}))
#         else:
#             httpResponse.write_body(json.dumps({"code": -1, "msg": "配置文件不存在"}))
#
#
# class CreateTowServlet(Servlet):
#     def servlet(self, httpRequest: HttpRequest, httpResponse: HttpResponse):
#         try:
#             data = json.load(open("config.json", encoding="utf-8"))
#             analysis = SQLLinkUtil(data)
#             analysis.get_all_table()
#             analysis.mapping_relations()
#             analysis.save_model_json()
#             httpResponse.write_body(json.dumps({"code": 200}))
#         except:
#             httpResponse.write_body(json.dumps({"code": -1, "msg": "配置文件生成错误"}))
#
#
# class CreateThreeServlet(Servlet):
#     def servlet(self, httpRequest: HttpRequest, httpResponse: HttpResponse):
#         try:
#             g = Generate()
#             g.generate()
#             httpResponse.write_body(json.dumps({"code": 200}))
#         except:
#             traceback.print_exc()
#             httpResponse.write_body(json.dumps({"code": -1, "msg": "代码生成依赖的config目录错误"}))
#
#
# class GetInfoServlet(Servlet):
#     def servlet(self, httpRequest: HttpRequest, httpResponse: HttpResponse):
#         path = os.path.join(os.getcwd(), "config.json")
#         a = os.path.exists(path)
#         path = os.path.join(os.getcwd(), "config")
#         b = os.path.exists(path)
#         path = os.path.join(os.getcwd(), "data")
#         c = os.path.exists(path)
#         path = os.path.join(os.getcwd(), "exConfig")
#         d = os.path.exists(path)
#         httpResponse.write_body(json.dumps({
#             "code": 200,
#             "data": {"a": a, "b": b, "c": c, "d": d}
#         }))
#
#
# def del_file(filepath):
#     del_list = os.listdir(filepath)
#     for f in del_list:
#         file_path = os.path.join(filepath, f)
#         if os.path.isfile(file_path):
#             os.remove(file_path)
#         elif os.path.isdir(file_path):
#             shutil.rmtree(file_path)
#
#
# class RemoveConfigServlet(Servlet):
#     def servlet(self, httpRequest: HttpRequest, httpResponse: HttpResponse):
#         path = os.path.join(os.getcwd(), "config")
#         del_file(path)
#         os.removedirs(path)
#         httpResponse.write_body(json.dumps({"code": 200}))
#
#
# class RemoveDataServlet(Servlet):
#     def servlet(self, httpRequest: HttpRequest, httpResponse: HttpResponse):
#         path = os.path.join(os.getcwd(), "data")
#         del_file(path)
#         os.removedirs(path)
#         httpResponse.write_body(json.dumps({"code": 200}))
#
#
# class RemoveExConfigServlet(Servlet):
#     def servlet(self, httpRequest: HttpRequest, httpResponse: HttpResponse):
#         path = os.path.join(os.getcwd(), "exConfig")
#         del_file(path)
#         os.removedirs(path)
#         httpResponse.write_body(json.dumps({"code": 200}))
#
#
# class GetConfigList(Servlet):
#     def servlet(self, httpRequest: HttpRequest, httpResponse: HttpResponse):
#         path = os.path.join(os.getcwd(), "config")
#         if os.path.exists(path):
#             list_file = os.listdir(path)
#             data = []
#             for file in list_file:
#                 if ".json" in file:
#                     data.append(file)
#             httpResponse.write_body(json.dumps({"code": 200, "data": data}))
#         else:
#             httpResponse.write_body(json.dumps({"code": -1, "msg": "目录不存在"}))
#
#
# class GetOneJson(Servlet):
#     def servlet(self, httpRequest: HttpRequest, httpResponse: HttpResponse):
#         file = httpRequest.get_param("file")
#         path = os.path.join(os.getcwd(), "config")
#         if os.path.exists(path) and file is not None:
#             file_path = os.path.join(path, file)
#             if os.path.exists(file_path):
#                 httpResponse.write_body(json.dumps({"code": 200, "data": json.load(open(os.path.join(file_path)))}))
#                 return
#         httpResponse.write_body(json.dumps({"code": -1, "msg": "目录不存在"}))
#
#
# class CreateExConfigServlet(Servlet):
#     def servlet(self, httpRequest: HttpRequest, httpResponse: HttpResponse):
#         data = httpRequest.get_param("data")
#         class_name = httpRequest.get_param("className")
#         if class_name is None or data is None:
#             httpResponse.write_body(json.dumps({"code": -1, "msg": "缺少必要参数"}))
#             return
#
#         path = os.path.join(os.getcwd(), "exConfig")
#         if not os.path.exists(path):
#             os.mkdir(path)
#         try:
#             with open(os.path.join(path, class_name) + ".json", "w", encoding="utf-8") as file:
#                 file.write(data)
#             httpResponse.write_body(json.dumps({"code": 200}))
#         except:
#             httpResponse.write_body(json.dumps({"code": -1, "msg": "写入文件出错"}))
#
#
# class CreateExCodeServlet(Servlet):
#     def servlet(self, httpRequest: HttpRequest, httpResponse: HttpResponse):
#         try:
#             g = ExGenerate()
#             g.generate()
#             httpResponse.write_body(json.dumps({"code": 200}))
#         except:
#             traceback.print_exc()
#             httpResponse.write_body(json.dumps({"code": -1, "msg": "代码生成依赖的exConfig目录错误"}))
