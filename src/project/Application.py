from src.util.chiyaUtil import OSUtil


def create_file(root: str):
    """
    构建文件
    :param root:所在的包路径
    """
    path = f'{root}'
    template = f'package {path};\n'
    template += """
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.servlet.ServletComponentScan;
import org.springframework.scheduling.annotation.EnableScheduling;

import chiya.log.ChiyaLog;

@SpringBootApplication
@ServletComponentScan
@EnableScheduling
public class Application {

	public static void main(String[] args) {
		// 禁用生成日志文件
		ChiyaLog.getConfig().fileLogDisabled();
		SpringApplication.run(Application.class, args);
		ChiyaLog.info("服务启动完成");
	}

}

"""
    OSUtil.save_file_java(path, "Application", template)
