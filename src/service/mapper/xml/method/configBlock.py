from src.util.chiyaUtil import StringUtil


class DatabaseNameConfig:

    @staticmethod
    def get_database_name(config):
        if "databaseName" in config["config"] and config["config"]["databaseName"]["enable"]:
            if "value" in config["config"]["databaseName"]:
                data = config["config"]["databaseName"]["value"]
                if StringUtil.is_not_null(data):
                    return data + "."
        return ""
