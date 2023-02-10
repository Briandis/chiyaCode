from src.util import OSUtil


def create_file(root: str):
    """
    构建文件
    :param root:所在的包路径
    """
    path = f'{root}.common.module.security'
    template = f'package {path};\n'
    template += """
import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.annotation.WebFilter;

import chiya.web.request.RequestFilter;

import java.io.IOException;

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
	    // 如果报错，请更换为JakartaRequestFilter，SpringBoot3.0中已经更换了java的命名空间
        // import chiya.web.request.jakarta.JakartaRequestFilter;
		RequestFilter.doFilter(servletRequest, servletResponse, filterChain);
	}

}
"""
    OSUtil.save_file_java(path, "BodyReaderFilter", template)
