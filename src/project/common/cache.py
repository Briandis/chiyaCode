from src.util.chiyaUtil import OSUtil


def create_file(root: str):
    """
    构建文件
    :param root:所在的包路径
    """
    path = f'{root}.common.module.cache'
    template = f'package {path};\n'
    template += """
import org.springframework.stereotype.Component;

/**
 * 全局本地缓存
 */
@Component
public class GlobalStore {

}
"""
    OSUtil.save_file_java(path, "GlobalStore", template)
