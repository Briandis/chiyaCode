from src.util import OSUtil


def create_file(root: str):
    """
    构建文件
    :param root:所在的包路径
    """
    path = f'{root}.common.bootstrap'
    template = f'package {path};\n'
    template += """
import javax.annotation.PostConstruct;
import org.springframework.stereotype.Component;
import org.springframework.beans.factory.annotation.Autowired;
import chiya.web.security.ChiyaSecurityExtract;
import chiya.web.security.SecurityCertification;

/**
 * 服务初始化启动操作
 */
@Component
public class ServerBootStrap {

    @Autowired
	private ChiyaSecurityExtract chiyaSecurityExtract;
	
    @PostConstruct
    public void init(){
        // TODO:如果项目配置了统一接口路径前缀，则在这里修改，注意开头需要'/'这个斜杠
        ChiyaSecurityExtract.servicePath = "/";
        // 装配所有角色注册的URL
		SecurityCertification.chiyaHashMapValueMap = chiyaSecurityExtract.getURL();
		// TODO:需要手动编写加载用户->角色的关系代码
		
        // TODO:要进行的初始化操作
    }

}
"""
    OSUtil.save_file_java(path, "ServerBootStrap", template)
