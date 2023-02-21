# from src.java.JavaCode import JavaCode, DefaultMate, Attribute, Function
#
# javaCode = JavaCode("chiya.test", "CodeTest")
#
# javaCode.add_mate(DefaultMate.RestController())
# javaCode.add_mate(DefaultMate.RequestMapping("/test"))
#
# attribute = Attribute("TestService", "testService", )
# attribute.add_mate(DefaultMate.Autowired())
# attribute.add_mate(DefaultMate.Qualifier("testServiceImpl"))
# javaCode.add_attr(attribute)
#
# function = Function("private", None, "test", None, Attribute("int", "abs"))
# function.set_is_interface()
#
# javaCode.add_function(function)
#
# attribute = Attribute("int", None, "相应行数")
# function = Function("private", attribute, "getLine", "获取行数", Attribute("Integer", "a"), Attribute("String", "charString", "字符集"))
# function.add_mate(DefaultMate.GetMapping("/getCount"))
#
# javaCode.add_function(function)
#
# print(javaCode.create())


# print(f'{str(None)}1')
"""
controller -> servicer -> domain -> repository -> mapper
controller -> servicer -> mapper
controller -> servicer -> repository -> mapper
controller -> servicer -> domain -> base -> work -> repository -> mapper

"""
code_list = [
    "controller",
    "servicer",
    "mapper",
]
