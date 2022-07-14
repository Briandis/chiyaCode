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

/**
 * 服务初始化启动操作
 */
@Component
public class ServerBootStrap {
    
    @PostConstruct
    public void init(){
        // TODO:要进行的初始化操作
    }

}
"""
    OSUtil.save_file_java(path, "ServerBootStrap", template)
