from src.util.chiyaUtil import OSUtil


def create_file(root: str):
    """
    构建文件
    :param root:所在的包路径
    """
    path = f'{root}.config'
    template = f'package {path};\n'
    template += """
import java.net.InetAddress;
import java.net.UnknownHostException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;

import chiya.core.base.number.NumberUtil;

/**
 * 当前服务运行信息
 * 
 * @author chiya
 *
 */
@Component
public class ServerInfo {

	/** 服务所运行的端口 */
	private Integer port;

	/** 当前IP */
	private String ip;

	/** 版本 */
	private String version;

	/** 全局路径 */
	private String path;

	@Autowired
	private Environment environment;

	/**
	 * 获取端口
	 * 
	 * @return 服务所运行的端口
	 */
	public Integer getPort() {
		if (port == null) {
			String serverPort = environment.getProperty("local.server.port");
			port = NumberUtil.parseIntOrNull(serverPort);
		}
		return port;
	}

	/**
	 * 获取IP
	 * 
	 * @return 服务所运行的IP
	 */
	public String getIp() {
		if (ip == null) {
			try {
				ip = InetAddress.getLocalHost().getHostAddress();
			} catch (UnknownHostException e) {
				ip = null;
			}
		}
		return ip;
	}

	/**
	 * 获取当前版本
	 * 
	 * @return 版本
	 */
	public String getVersion() {
		if (version == null) { version = environment.getProperty("server.version"); }
		return version;
	}

	/**
	 * 获取全局URL路径
	 * 
	 * @return 统一的路径
	 */
	public String getPath() {
		if (path == null) { path = environment.getProperty("server.servlet.context-path"); }
		return path;
	}

}

"""
    OSUtil.save_file_java(path, "ServerInfo", template)
