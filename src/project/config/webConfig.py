from src.util.chiyaUtil import OSUtil


def create_file(root: str):
    """
    构建文件
    :param root:所在的包路径
    """
    path = f'{root}.config'
    template = f'package {path};\n'
    template += """
import org.springframework.boot.autoconfigure.http.HttpMessageConverters;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.format.FormatterRegistry;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.servlet.config.annotation.InterceptorRegistration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.serializer.SerializerFeature;
import com.alibaba.fastjson.support.spring.FastJsonHttpMessageConverter;
import """+root+""".common.converter.DateConverter;
import """+root+""".common.module.security.Security;

@Configuration
public class WebConfig implements WebMvcConfigurer {

	@Bean
	Security getSecurity() {
		return new Security();
	}

	@Bean
	RestTemplate getRestTemplate() {
		return new RestTemplate();
	}

	@Bean
	DateConverter getDateConverter() {
		return new DateConverter();
	}

	@Override
	public void addFormatters(FormatterRegistry registry) {
		registry.addConverter(getDateConverter());
	}

	@Override
	public void addInterceptors(InterceptorRegistry registry) {
		// 注册拦截器
		InterceptorRegistration registration = registry.addInterceptor(getSecurity());
		// 所有路径都被拦截
		registration.addPathPatterns("/**");
	}

	@Bean
	HttpMessageConverters fastJsonHttpMessageConverters() {
		// 关闭全局循环引用
		JSON.DEFAULT_GENERATE_FEATURE |= SerializerFeature.DisableCircularReferenceDetect.getMask();
		// 默认fast的转换器
		FastJsonHttpMessageConverter fastJsonConverter = new FastJsonHttpMessageConverter();
		return new HttpMessageConverters(fastJsonConverter);
	}

}
"""
    OSUtil.save_file_java(path, "WebConfig", template)
