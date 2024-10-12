from src.util.chiyaUtil import OSUtil


def create_file(root: str):
    """
    构建文件
    :param root:所在的包路径
    """
    path_t1=root.replace(".","-")
    path_t2=root.replace(".","/")
    template = f"""# 自动生成配置
    
# 服务端口 
server.port=32123

# 服务同意地址前缀
server.servlet.context-path=/{path_t1}

# 文件上传大小限制
spring.servlet.multipart.max-file-size=5MB
spring.servlet.multipart.max-request-size=5MB

# 使用的配置前缀
spring.profiles.active=dev

# redis配置
spring.redis.host=127.0.0.1
spring.redis.database=2
spring.redis.port=6379
spring.redis.timeout=3000ms

# mybatis配置
mybatis.mapper-locations=classpath:{path_t2}/**/*Mapper.xml
mybatis.type-aliases-package={root}

"""
    OSUtil.save_file("resources", "application", "properties", template)
