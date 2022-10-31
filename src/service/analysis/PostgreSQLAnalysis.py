import psycopg2
from psycopg2 import extras


class PostgreSQLAnalysis:

    def __init__(self, dbname, database, user="postgres", password="123456", host="127.0.0.1", port=5432):
        self.conn = psycopg2.connect(dbname=database, user=user, password=password, host=host, port=port)
        self.curses = self.conn.cursor(cursor_factory=extras.DictCursor)
        self.database = dbname

    def get_all_table(self):
        """
        获取全部的表
        :return:
        """
        self.curses.execute(f"""
SELECT
	relname AS 表名,
	CAST ( obj_description ( relfilenode, 'pg_class' ) AS VARCHAR ) AS 名称,
	attr.* 
FROM
	pg_class,
	(
	SELECT
		attrelid,
		attname AS 字段,
		description AS 字段备注,
		typname AS 列类型,
		EXISTS (
		SELECT
			* 
		FROM
			pg_constraint 
		WHERE
			pg_constraint.conrelid = attrelid 
			AND pg_constraint.contype = 'p' 
			AND pg_attribute.attnum = pg_constraint.conkey [ 1 ] 
		) AS 主键 
	FROM
		pg_attribute
		LEFT JOIN pg_description ON attrelid = objoid 
		AND attnum = objsubid
		LEFT JOIN pg_type ON atttypid = pg_type.oid 
	) AS attr 
WHERE
	relname IN ( SELECT tablename FROM pg_tables WHERE schemaname = '{self.database}') 
	AND attrelid = oid 
ORDER BY
	relname
        """)

        self.conn.commit()

        rows = self.curses.fetchall()
        row_dict = [{k: v for k, v in record.items()} for record in rows]
        self.curses.close()
        self.conn.close()
        return row_dict

    def to_mysql_list_table(self):
        """
        转化成mysql的表信息
        :return:
        """
        tables = {}
        for row in self.get_all_table():
            table_name = row["表名"]
            if table_name not in tables:
                tables[table_name] = {
                    "TABLE_NAME": row["表名"],
                    "TABLE_COMMENT": row["名称"],
                    "COLUMN": []
                }
            table = tables[table_name]
            column = {
                "COLUMN_NAME": row["字段"],
                "DATA_TYPE": row["列类型"],
                "COLUMN_KEY": row["主键"],
                "COLUMN_COMMENT": row["字段备注"]
            }
            if column["COLUMN_KEY"]:
                column["COLUMN_KEY"] = "PRI"
            else:
                column["COLUMN_KEY"] = None
            table["COLUMN"].append(column)
        lists = []
        for key in tables:
            lists.append(tables[key])
        return lists
