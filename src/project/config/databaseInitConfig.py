from src.util.chiyaUtil import OSUtil


def create_file(root: str):
    """
    构建文件
    :param root:所在的包路径
    """
    path = f'{root}.config'
    template = f'package {path};\n'
    template += """

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;

import chiya.log.ChiyaLog;
import jakarta.annotation.PostConstruct;

/**
 * 初始化数据库
 * 
 * @author chiya
 *
 */
@Component
public class DatabaseInitConfig {

	/** 链接地址 */
	private String url;
	/** 用户名 */
	private String username;
	/** 密码 */
	private String password;

	@Autowired
	private Environment environment;

	/**
	 * 获取配置的数据库地址
	 * 
	 * @return 数据库URL
	 */
	public String getUrl() {
		if (url == null) { url = environment.getProperty("spring.datasource.url"); }
		return url;
	}

	/**
	 * 获取用户名连接
	 * 
	 * @return 用户名
	 */
	public String getUsername() {
		if (username == null) {
			username = environment.getProperty("spring.sql.init.username");
			if (username == null) { username = environment.getProperty("spring.datasource.username"); }
		}
		return username;
	}

	/**
	 * 获取密码
	 * 
	 * @return
	 */
	public String getPassword() {
		if (password == null) {
			password = environment.getProperty("spring.sql.init.password");
			if (password == null) { password = environment.getProperty("spring.datasource.password"); }
		}
		return password;
	}

	/**
	 * 获取数据库配置的库，并初始化
	 */
	@PostConstruct
	public void initDatabase() {
		ChiyaLog.info("开始数据库初始化流程！");
		try {
			String dbURL = getUrl();
			String all[] = dbURL.split("\\\\?");
			String jbdcULR[] = all[0].split("/");
			String database = jbdcULR[jbdcULR.length - 1];
			ChiyaLog.info("数据库配置解析完成，开始初始化");
			try {
				Connection connection = DriverManager
					.getConnection(
						dbURL.replace(database, ""),
						getUsername(),
						getPassword()
					);
				Statement statement = connection.createStatement();
				String sql = "CREATE DATABASE IF NOT EXISTS `" + database + '`';
				statement.execute(sql);
				statement.close();
				connection.close();
			} catch (Exception e) {
				ChiyaLog.error("初始化数据库失败，如果可以，请手动构建", database, "的数据库");
			}
		} catch (Exception e) {
			ChiyaLog.error("初始化数据库失败，数据库配置解析出错");
		}
		ChiyaLog.info("初始化数据库流程结束");
	}
}

"""
    OSUtil.save_file_java(path, "DatabaseInitConfig", template)
