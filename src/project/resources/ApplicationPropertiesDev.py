from src.util.chiyaUtil import OSUtil


def create_file(root: str):
    """
    构建文件
    :param root:所在的包路径
    """
    path_t1=root.replace(".","-")
    path_t2=root.replace(".","/")
    template = f"""# 自动生成配置
    
# 数据库配置
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.datasource.url=jdbc:mysql://127.0.0.1:3306/{path_t1}?useUnicode=true&characterEncoding=utf-8&serverTimezone=Asia/Shanghai
spring.datasource.username=root
spring.datasource.password=123456

# 日志配置
logging.level.{root}.common.module=debug
logging.level.{root}.module=debug

"""
    OSUtil.save_file("resources", "application-dev", "properties", template)
