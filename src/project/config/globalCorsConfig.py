from src.util import OSUtil


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
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * 全局跨域配置
 */
@Configuration
public class GlobalCorsConfig implements WebMvcConfigurer {

	/**
	 * 允许跨域调用的过滤器
	 */
	@Bean
	public CorsFilter corsFilter() {
		CorsConfiguration config = new CorsConfiguration();
		// 允许所有域名进行跨域调用
		config.addAllowedOriginPattern("*");
		// 允许跨越发送cookie
		config.setAllowCredentials(true);
		// 放行全部原始头信息
		config.addAllowedHeader("*");
		// 允许所有请求方法跨域调用
		config.addAllowedMethod("*");
		UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
		source.registerCorsConfiguration("/**", config);
		return new CorsFilter(source);
	}
}
"""
    OSUtil.save_file_java(path, "GlobalCorsConfig", template)
