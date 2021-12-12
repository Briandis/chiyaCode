class JsonKey:
    # 类名称
    className = "className"
    # 类所在路径
    path = "path"
    # 完整包路径
    package = "package"
    # 表名称
    tableName = "tableName"
    # 备注
    remark = "remark"
    # 工具路径
    utilPath = "utilPath"

    # 主键配置
    class key:
        self = "key"
        # 字段名
        filed = "filed"
        # JAVA数据类型
        type = "type"
        # 属性
        attr = "attr"
        # 备注
        remark = "remark"

    # 属性配置
    class attr:
        self = "attr"
        # 字段名
        filed = "filed"
        # JAVA数据类型
        type = "type"
        # 属性
        attr = "attr"
        # 备注
        remark = "remark"

    # 公共配置
    class config:
        self = "config"

        # 模糊搜索
        class fuzzySearch:
            self = "fuzzySearch"
            name = "name"
            enable = "enable"
            value = "value"
            default = "default"
            data = "data"

        # resultMap替换
        class resultMap:
            self = "resultMap"
            name = "name"
            enable = "enable"

        # restful风格API接口
        class restful:
            self = "restful"
            name = "name"
            enable = "enable"

        # splicingSQL拼接块
        class splicingSQL:
            self = "splicingSQL"
            name = "name"
            enable = "enable"
            value = "value"
            default = "default"

        # extraAPI额外的接口
        class extraAPI:
            self = "extraAPI"
            name = "name"
            enable = "enable"
            value = "value"
            default = "default"

        # 默认的接口
        class defaultAPI:
            self = "defaultAPI"
            name = "name"
            enable = "enable"

        # 假删
        class falseDelete:
            self = "falseDelete"
            name = "name"
            enable = "enable"
            deleteKey = "deleteKey"
            default = "default"
            deleteValue = "deleteValue"
            isUpdate = "isUpdate"
            updateKey = "updateKey"

        # 生成toString方法
        class toJsonString:
            self = "toJsonString"
            name = "name"
            enable = "enable"
            isFastJson = "isFastJson"

        # 链式方法
        class chain:
            self = "chain"
            name = "name"
            enable = "enable"

        # 实体克隆模式
        class entityClone:
            self = "entityClone"
            name = "name"
            enable = "enable"

        # 默认service方法前缀
        class methodName:
            self = "methodName"
            name = "name"
            enable = "enable"
            value = "value"
            default = "default"

        # 创建的文件
        class createFile:
            self = "createFile"
            name = "name"
            enable = "enable"
            value = "value"
            default = "default"

        # 不创建的文件
        class notCreateFile:
            self = "notCreateFile"
            name = "name"
            enable = "enable"
            value = "value"
            default = "default"

        # XML的配置
        class xmlConfig:
            self = "xmlConfig"
            resultMapName = "resultMapName"
            fieldAlias = "fieldAlias"

    # 自动生成的实体类
    class baseEntity:
        self = "baseEntity"
        path = "path"
        className = "className"
        package = "package"

    # 自动生成的XML
    class baseMapperXml:
        self = "baseMapperXml"
        path = "path"
        className = "className"
        package = "package"

    # XML
    class mapperXml:
        self = "mapperXml"
        path = "path"
        className = "className"
        package = "package"

    # 自动生成的mapper接口
    class baseMapperInterface:
        self = "baseMapperInterface"
        path = "path"
        className = "className"
        package = "package"

    # mapper接口
    class mapperInterface:
        self = "mapperInterface"
        path = "path"
        className = "className"
        package = "package"

    # 业务层接口
    class serviceInterface:
        self = "serviceInterface"
        path = "path"
        className = "className"
        package = "package"

    # 业务层实现
    class serviceImplements:
        self = "serviceImplements"
        path = "path"
        className = "className"
        package = "package"

    # 控制层
    class controller:
        self = "controller"
        path = "path"
        className = "className"
        package = "package"

    # 分页信息
    class Page:
        self = "Page"
        path = "path"
        className = "className"
        package = "package"

    # 一对一
    oneToOne = "oneToOne"
    # 一对多
    oneToMany = "oneToMany"
    # 多对多
    manyToMany = "manyToMany"
    # 外键
    foreignKey = "foreignKey"

    # 克隆配置
    class entityClone:
        self = "entityClone"

        # 主键配置
        class key:
            self = "key"
            # 字段名
            filed = "filed"
            # JAVA数据类型
            type = "type"
            # 属性
            attr = "attr"
            # 备注
            remark = "remark"

        # 属性配置
        class attr:
            self = "attr"
            # 字段名
            filed = "filed"
            # JAVA数据类型
            type = "type"
            # 属性
            attr = "attr"
            # 备注
            remark = "remark"
