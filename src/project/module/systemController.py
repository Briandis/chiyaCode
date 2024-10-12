from src.util.chiyaUtil import OSUtil


def create_file(root: str):
    """
    构建文件
    :param root:所在的包路径
    """
    path = f'{root}.module.system'
    template = f'package {path};\n\n'
    template += f'import {root}.common.module.security.Security;\n'
    template += f'import {root}.config.ServerInfo;\n'

    template += """
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import chiya.core.base.result.Result;
import chiya.core.base.thread.ThreadUtil;
import chiya.log.ChiyaLog;

/**
 * 服务控制相关
 * 
 * @author chiya
 *
 */
@RestController
@RequestMapping("/system")
public class SystemController {

	@Autowired
	private ServerInfo serverInfo;

	/**
	 * 终止当前服务
	 * 
	 * @return 业务对象
	 */
	@PostMapping("/exit")
	public Result exit() {
		ThreadUtil.createAndStart(() -> {
			// 睡眠5s后退出服务
			ChiyaLog.warn("服务将在5秒后终止");
			ThreadUtil.sleep(5000);
			System.exit(0);
		});
		return Result.success();
	}

	/**
	 * 获取系统信息
	 * 
	 * @return 业务对象
	 */
	@GetMapping("/serverInfo")
	public Result getInfo() {
		return Result.success(serverInfo);
	}

	/**
	 * 获取接口报告信息
	 * 
	 * @return Result业务对象
	 */
	@GetMapping("/interfaceReport")
	public Result getInterfaceReport() {
		return Result.success(Security.INTERFACE_PERFORMANCE.getReport());
	}

}

"""
    OSUtil.save_file_java(path, "SystemController", template)
