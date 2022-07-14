from src.util import OSUtil


def create_file(root: str):
    """
    构建文件
    :param root:所在的包路径
    """
    path = f'{root}.common.exception'
    template = f'package {path};\n'
    template += """
import org.springframework.validation.BindException;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;

import chiya.core.base.exception.ChiyaException;
import chiya.core.base.result.Result;
import chiya.core.base.result.ResultEnum;

/**
 * 全局异常处理
 */
@ControllerAdvice
public class GlobalExceptionHandler {

	/**
	 * 通用自定义异常拦截处理
	 * 
	 * @param chiyaException 自定义异常
	 * @return CommonResult 通用返回对象
	 */
	@ResponseBody
	@ExceptionHandler(value = ChiyaException.class)
	public Result handle(ChiyaException chiyaException) {
		// 如果返回值枚举类型有值，则根据枚举值返回错误信息
		if (chiyaException.getResultEnum() != null) { return Result.enums(chiyaException.getResultEnum()); }
		return Result.fail(chiyaException.getMessage());
	}

	/**
	 * 抽象出来的重复的代码块
	 * 
	 * @param bindingResult
	 * @return CommonResult 通用返回对象
	 */
	private Result bindingResultCommon(BindingResult bindingResult) {
		String message = null;
		if (bindingResult.hasErrors()) {
			FieldError fieldError = bindingResult.getFieldError();
			// 获取错误字段和定义的错误信息，大概是这样吧
			if (fieldError != null) { message = fieldError.getField() + fieldError.getDefaultMessage(); }
		}
		return Result.fail(message);
	}

	/**
	 * 参数校验异常拦截处理
	 * 
	 * @param methodArgumentNotValidException 参数校验异常，啥异常我也不知道，大概
	 * @return CommonResult 通用返回对象
	 */
	@ResponseBody
	@ExceptionHandler(value = MethodArgumentNotValidException.class)
	public Result handleValidException(MethodArgumentNotValidException methodArgumentNotValidException) {
		BindingResult bindingResult = methodArgumentNotValidException.getBindingResult();
		return bindingResultCommon(bindingResult);
	}

	/**
	 * 参数校验异常拦截处理
	 * 
	 * @param bindException
	 * @return CommonResult 通用返回对象
	 */
	@ResponseBody
	@ExceptionHandler(value = BindException.class)
	public Result handleValidException(BindException bindException) {
		BindingResult bindingResult = bindException.getBindingResult();
		return bindingResultCommon(bindingResult);
	}

	/**
	 * 请求头字段缺失异常处理
	 * 
	 * @param servletRequestParameterException
	 * @return CommonResult 通用返回对象
	 */
	@ResponseBody
	@ExceptionHandler(MissingServletRequestParameterException.class)
	public Result handleMissingServletRequestParameterException(MissingServletRequestParameterException servletRequestParameterException) {
		ResultEnum resultCodeEnum = ResultEnum.PARAMENTER_ERROR;
		String msg = String.format("请求字段缺失, 类型为 %s，名称为 %s", servletRequestParameterException.getParameterType(),
				servletRequestParameterException.getParameterName());
		return Result.enums(resultCodeEnum, msg);
	}
}
"""
    OSUtil.save_file_java(path, "GlobalExceptionHandler", template)
