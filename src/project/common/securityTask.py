from src.util import OSUtil


def create_file(root: str):
    """
    构建文件
    :param root:所在的包路径
    """
    path = f'{root}.common.module.security'
    template = f'package {path};\n'
    template += """
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import lombok.extern.slf4j.Slf4j;

/**
 * 接口的每日任务
 */
@Component
@Slf4j
public class SecurityTask {

	/**
	 * 每日 0 : 00 的时候执行的任务
	 */
	@Scheduled(cron = "0 0 0 * * ?")
	public void task() {
		log.debug("-------->昨日请求数量：" + Security.interfaceCount.getCountMsg());
		Security.INTERFACE_PERFORMANCE.getReport().forEach(obj -> log.debug("性能报告" + obj));;
		Security.interfaceCount.reset();
		Security.INTERFACE_PERFORMANCE.reset();
	}

}

"""
    OSUtil.save_file_java(path, "SecurityTask", template)
