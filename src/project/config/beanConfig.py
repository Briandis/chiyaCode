from src.util.chiyaUtil import OSUtil


def create_file(root: str):
    """
    构建文件
    :param root:所在的包路径
    """
    path = f'{root}.config'
    template = f'package {path};\n'
    template += """
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import chiya.web.redis.BaseRedisService;
import chiya.web.security.ChiyaSecurityExtract;

@Configuration
public class BeanConfig {

	// Redis通用模板
	@Bean
	BaseRedisService BaseRedisService() {
		return new BaseRedisService();
	}

    // 权限控制器
	@Bean
	ChiyaSecurityExtract ChiyaSecurityExtract() {
	    // 服务器配置的全局路径
		ChiyaSecurityExtract.servicePath = "/chiya";
		return new ChiyaSecurityExtract();
	}

}
"""
    OSUtil.save_file_java(path, "BeanConfig", template)
