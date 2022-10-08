from src.util import OSUtil


def create_file(root: str):
    """
    构建文件
    :param root:所在的包路径
    """
    path = f'{root}.common.module.security'
    template = f'package {path};\n'
    template += """
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.web.servlet.HandlerInterceptor;

import com.alibaba.fastjson.JSONObject;

import chiya.core.base.count.InterfaceCount;
import chiya.core.base.count.InterfacePerformance;
import chiya.core.base.string.StringUtil;
import chiya.core.base.number.NumberUtil;
import chiya.security.Method;
import chiya.web.security.SecurityCertification;
import chiya.web.token.TokenUtil;
import chiya.log.ChiyaLog;

import """ + root + """.common.util.ThreadSession;

/**
 * 拦截器，用于权限控制，token基础数据处理
 */
public class Security implements HandlerInterceptor {

	/** 计数工具 */
	public static final InterfaceCount interfaceCount = new InterfaceCount();
	/** 性能统计工具 */
	public static final InterfacePerformance INTERFACE_PERFORMANCE = new InterfacePerformance();

	/**
	 * 全局接口拦截，进入控制层前
	 */
	@Override
	public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
		ThreadSession.setRunStartTime();
		// 是否放行
		boolean isRelease = true;

		String method = request.getMethod();
		String url = request.getRequestURI();
		String ip = request.getRemoteAddr();
		ThreadSession.setIP(ip);
		ThreadSession.setMethod(method);
		ThreadSession.setURL(url);
		// 获取token
		String token = request.getHeader("token");
		// 用户标识
		String user = null;
		if (token != null) {
			if (token.startsWith("user")) {
				token = token.substring("user".length());
				user = TokenUtil.getData(token);
				if (user != null) {
					ThreadSession.setToken(token);
					ThreadSession.setUserId(NumberUtil.parseIntOrNull(user));
				}
			}
		}
		// 先检查游客模式
		isRelease = SecurityCertification.checkTourists(url, Method.getByte(method));
		if (!isRelease && user != null) {
			// 用户模式
			isRelease = SecurityCertification.check(url, Method.getByte(method), null);
		}
		// 计数统计
		interfaceCount.increment(isRelease);
        ChiyaLog.info(StringUtil.spliceStringJoiner("\t", "用户", user, "请求方式", method, "请求地址", url, "IP", ip, interfaceCount.getCountMsg(), "业务执行状态", isRelease));
		logParameter(request);
		if (!isRelease) { response.setStatus(403); }
		return isRelease;
	}

	/**
	 * 从Controller返回之后处理
	 */
	@Override
	public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
		int time = (int) (System.currentTimeMillis() - ThreadSession.getRunStartTime());
		ChiyaLog.info("业务结束，清空线程临时数据,运行花费时间：", time);
		INTERFACE_PERFORMANCE.put(ThreadSession.getMethod() + ThreadSession.getURL(), time);
		// 清除该线程所使用的数据
		ThreadSession.clear();
	}

	/**
	 * 接口日志参数
	 * 
	 * @param request 请求信息
	 */
	public static void logParameter(HttpServletRequest request) {
		JSONObject jsonObject = new JSONObject();
		// 遍历参数并获取
		request.getParameterMap().forEach((key, value) -> jsonObject.put(key, value[0]));
		String contentType = request.getContentType();
		// 如果是上传文件的情况
		String info = "";
		if (contentType != null) {
			if (StringUtil.eqString("image/jpeg", contentType)) { info = "上传了图片"; }
			if (contentType.indexOf("multipart/form-data;") != -1) { info = "请求体长度：" + request.getContentLength(); }
		}
		ChiyaLog.info("携带参数", info, jsonObject.toJSONString());
	}

}
"""
    OSUtil.save_file_java(path, "Security", template)
