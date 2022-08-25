# chiyaCode

千夜代码生成器，快速构建开发JAVA-WEB项目，彻底解决烦恼。

---

### 下载地址：右侧，发行版内下载最新版的chiyaCode.zip，解压运行start.ext即可用。

> 只支持windows


---

## 特征优势

1.MyBatis的多表语句生成。

1. 多表生成基于表名+主键名的命名形式进行扫描，

> 如user和user_info表\
> user中存在主键字段名为id的字段\
> user_info表中存在字段名为user_id的字段即构成自动扫描的多表关系\
> 多表关系自动识别一对一、一对多、多对多

2. 多表查询中自动解决字段名重复问题，无需解决多表字段别名问题
3. 自动根据多表关系，提供本表的外键查询，完全可以做到单表查全部
4. 强大的单表操作

2.从controller层一路生成到mapper，只需要根据项目业务，删除接口即可，接口属于restful风格的api

3.前台后台接口一起生成

4.多种生成模式，支持MVC传统模式，支持模块化分包模式，支持领域驱动设计模式

5.轻度的依赖，如果你不需要chiya-util和chiya-web这两个jar包做依赖，完全可以舍去，对于Page这样的分页对象\
您可以自行构建Page对象，只需要其中拥有start和count字段即可无缝兼容生成的mapper
> 如果你要修改，就要做好要改多个mapper中的import的Page路径的准备

6.生成的代码全面的文档类型的注释，你只需阅读方法注释的文档，即可知道要做什么

### 7.如果数据库底层变动，支持重复生成，你可以放心的替换自动生成的文件

> 前提是你没有把代码写在自动生成的文件中\
> baseEntity、baseMapper、baseMapper.xml这三种文件就是用于自动生成的，请不要把新增的代码写在其中\
> entity、mapper、mapper.xml这几个文件是给你提供新增，他们都继承了上面的文件。\
> 如果带有base的文件，请勿修改其中的内容，因为这是被设计出可以随时替换的。\
> 其他类型的文件不支持重复生成，所以生成需谨慎，请检查生成的文件是否会覆盖你的代码。

8.提供新项目快速初始化项目的操作，快速统一风格

---

# 使用说明

1.编译后的文件直接运行start.exe，等等游览器打开

2.输入工程名称，作为JAVA的开发人员，你应该知道这个是什么意思

3.新项目推荐初始化工程，快速获得项目中常规的各种疑难问题处理
> 包括不限于json和FormData的统一处理 - 你可以不用思考这个接口是json还是传统表单了，和@requestBody说再见\
> 接口统一拦截器 - 鉴权、性能统计、用户信息处理、接口参数日志处理，都在这里\
> 全局异常处理 - 统一的异常捕获，进阶则断言检查\
> ThreadSession工具 - ThreadLocal你应该听说过吧，这个工具和这个差不多，但是实现不一样\
> 跨域配置 - 你不需要配置跨域了\
> 每天0点的定时任务 - 别忘了在app类上加上@ServletComponentScan @EnableScheduling注解，不然不会生效\
> 日期处理 - 你不需要考虑前端前的日期格式是各种乱七八糟的了，反正常见格式全都被转换了\
> 默认FastJson - emmm....如果你对这个有严重意见，可能你需要改好多地方，用这个东西就图API方便

4.输入数据库信息，进行连接

5.选择要生成的文件，如果生成模式不是领域驱动设计，则有些文件选中也不会生成
> 抽象实体、抽象Mapper接口、抽象Mapper.xml这些是可以被替换的，其他的则慎重考虑

6.生成配置文件
> 如果你有什么要深度自定义的，可以在根目录下config种进行定制修改\
> 生成配置文件前，请检查config目录种有无多余的json配置，如果有请删除

7.解析配置文件并生成
> 生成需谨慎，注意config文件夹种有那些配置文件，切记！\
> data文件夹就是输出的代码，生成前也记得检查是否有多余的文件\
> 如果没有检查直接剪切走，代码被覆盖不要怪我没说！！！

---

## 项目依赖

生成的代码默认依赖 chiya-util、chiya-web、fastJson、spring-redis、spring全家桶\
chiya-util、chiya-web两者都需自行拉取源码，然后手动打jar包，\
两者打包不需要maven进行打包，普通打包即可\
参考
```xml
<!-- chiyaUtil工具库 -->
<dependency>
    <groupId>chiya</groupId>
    <artifactId>chiya</artifactId>
    <version>0.0.1</version>
    <scope>system</scope>
    <systemPath>chiyaUtil.jar的路径</systemPath>
</dependency>
<!-- chiya-web 工具库 -->
<dependency>
    <groupId>chiya-web</groupId>
    <artifactId>chiya-web</artifactId>
    <version>0.0.1</version>
    <scope>system</scope>
    <systemPath>chiya-web.jar的路径</systemPath>
</dependency>
```