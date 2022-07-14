from src.util import OSUtil


def create_file(root: str):
    """
    构建文件
    :param root:所在的包路径
    """
    path = f'{root}.common.util'
    template = f'package {path};\n'
    template += """
import chiya.core.base.thread.ThreadSpace;
import chiya.core.base.object.ObjectUtil;

/**
 * 登录信息工具
 */
public class ThreadSession {

	/** token标识 */
	private static final String TOKEN = "token";
	/** 请求IP */
	private static final String REQUEST_IP = "requestIp";
	/** 请求地址 */
	private static final String REQUEST_URL = "requestURL";
	/** 请求方式 */
	private static final String REQUEST_METHOD = "requestMethod";
	/** 运行时间 */
	private static final String RUN_START_TIME = "runStartTime";
	/** 用户id */
	private static final String USER_ID = "userId";

	/** 清除当前线程的对象 */
	public static void clear() {
		ThreadSpace.clear();
	}

	/**
	 * 设置token
	 * 
	 * @param token 传入的token
	 */
	public static void setToken(String token) {
		if (token != null) { ThreadSpace.put(TOKEN, token); }
	}

	/**
	 * 获取当前用户token
	 * 
	 * @return 字符串
	 */
	public static String getToken() {
		return ObjectUtil.toString(ThreadSpace.get(TOKEN));
	}

	/**
	 * 获取请求的IP
	 * 
	 * @return IP地址
	 */
	public static String getIP() {
		return ObjectUtil.toString(ThreadSpace.get(REQUEST_IP));
	}

	/**
	 * 获取请求的URL
	 * 
	 * @return URL地址
	 */
	public static String getURL() {
		return ObjectUtil.toString(ThreadSpace.get(REQUEST_URL));
	}

	/**
	 * 获取请求方式
	 * 
	 * @return 请求方式
	 */
	public static String getMethod() {
		return ObjectUtil.toString(ThreadSpace.get(REQUEST_METHOD));
	}

	/**
	 * 存储IP
	 * 
	 * @param ip 请求的IP
	 */
	public static void setIP(String ip) {
		ThreadSpace.put(REQUEST_IP, ip);
	}

	/**
	 * 存储请求地址
	 * 
	 * @param url 请求地址
	 */
	public static void setURL(String url) {
		ThreadSpace.put(REQUEST_URL, url);
	}

	/**
	 * 存储请求方式
	 * 
	 * @param method 请求方式
	 */
	public static void setMethod(String method) {
		ThreadSpace.put(REQUEST_METHOD, method);
	}

	/**
	 * 设置运行的起始时间
	 */
	public static void setRunStartTime() {
		ThreadSpace.put(RUN_START_TIME, System.currentTimeMillis());
	}

	/**
	 * 获取运行的起始时间
	 * 
	 * @return long 运行时间
	 */
	public static long getRunStartTime() {
		Object object = ThreadSpace.get(RUN_START_TIME);
		if (object instanceof Long) { return (Long) object; }
		return System.currentTimeMillis();
	}

	/**
	 * 获取用户id
	 * 
	 * @return 用户id
	 */
	public static Integer getUserId() {
		return ObjectUtil.toInteger(ThreadSpace.get(USER_ID));
	}

	/**
	 * 存储用户id
	 * 
	 * @param userId 用户id
	 */
	public static void setUserId(Integer userId) {
		ThreadSpace.put(USER_ID, userId);
	}

}

"""
    OSUtil.save_file_java(path, "ThreadSession", template)
