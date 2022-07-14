from src.util import OSUtil


def create_file(root: str):
    """
    构建文件
    :param root:所在的包路径
    """
    path = f'{root}.common.converter'
    template = f'package {path};\n'
    template += """
import java.util.Date;
import org.springframework.core.convert.converter.Converter;
import chiya.core.base.time.DateUtil;

/**
 * 日期转换器，解决前端日期格式问题
 */
public class DateConverter implements Converter<String, Date> {

	@Override
	public Date convert(String source) {
		return DateUtil.stringToDate(source);
	}
}
"""
    OSUtil.save_file_java(path, "DateConverter", template)
