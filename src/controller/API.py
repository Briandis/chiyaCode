from src.httpServer.HttpRequest import HttpRequest
from src.httpServer.HttpResponse import HttpResponse
from src.httpServer.RequestApi import Servlet


class HelloWorld(Servlet):
    def servlet(self, request: HttpRequest, response: HttpResponse):
        response.write("hello world")
