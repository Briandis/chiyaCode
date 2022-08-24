from src.util import OSUtil


def create_file(root: str):
    """
    构建文件
    :param root:所在的包路径
    """
    path = f'{root}.common.exception'
    template = f'package {path};\n'
    template += """
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;

import chiya.core.base.exception.ChiyaException;
import chiya.core.base.result.Result;
import chiya.log.ChiyaLog;

/**
 * 全局异常处理
 */
@ControllerAdvice
public class GlobalExceptionHandler {

	/**
	 * 通用自定义异常拦截处理
	 * 
	 * @param chiyaException 自定义异常
	 * @return Result 通用返回对象
	 */
	@ResponseBody
	@ExceptionHandler(value = ChiyaException.class)
	public Result handle(ChiyaException chiyaException) {
		// 如果返回值枚举类型有值，则根据枚举值返回错误信息
		if (chiyaException.getResultEnum() != null) { return Result.enums(chiyaException.getResultEnum()); }
		return Result.fail(chiyaException.getMessage());
	}
	
	/**
	 * 通用异常处理
	 * 
	 * @param exception 自定义异常
	 * @return Result 通用返回对象
	 * @throws Exception
	 */
	@ResponseBody
	@ExceptionHandler(value = Exception.class)
	public Result handle(Exception exception) throws Exception {
		StringBuilder stringBuilder = new StringBuilder();
		for (StackTraceElement stackTraceElement : exception.getStackTrace()) {
			stringBuilder.append("\t").append(stackTraceElement).append("\n");
		}
		ChiyaLog.error(exception, "\n", stringBuilder);
		throw exception;
	}
}
"""
    OSUtil.save_file_java(path, "GlobalExceptionHandler", template)
