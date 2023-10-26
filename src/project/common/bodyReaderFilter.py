from src.util.chiyaUtil import OSUtil


def create_file(root: str):
    """
    构建文件
    :param root:所在的包路径
    """
    path = f'{root}.common.module.security'
    template = f'package {path};\n'
    template += """
import jakarta.servlet.Filter;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.ServletRequest;
import jakarta.servlet.ServletResponse;
import jakarta.servlet.annotation.WebFilter;

import java.io.IOException;

import chiya.web.request.jakarta.JakartaRequestFilter;

// 启用Filter需要在Springboot的启动类加@ServletComponentScan
/**
 * 针对JSON的备份ServletRequest
 * 
 * @author chiya
 */
@WebFilter(filterName = "bodyReaderFilter", urlPatterns = "/*")
public class BodyReaderFilter implements Filter {

	@Override
	public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
		JakartaRequestFilter.doFilter(servletRequest, servletResponse, filterChain);
	}

}
"""
    OSUtil.save_file_java(path, "BodyReaderFilter", template)
