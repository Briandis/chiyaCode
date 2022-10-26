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
            pg_class.relname AS 表名,
            CAST ( obj_description ( relfilenode, 'pg_class' ) AS VARCHAR ) AS 名称,
            pg_attribute.attname AS 字段,
            pg_description.description AS 字段备注,
            pg_type.typname AS 列类型,
            EXISTS ( SELECT * FROM pg_constraint WHERE pg_constraint.conrelid = pg_class.oid AND pg_constraint.contype = 'p' 	AND pg_attribute.attnum = pg_constraint.conkey [ 1 ]) AS 主键 
        FROM
            pg_class,
            pg_attribute,
            pg_type,
            pg_description 
        WHERE
            pg_attribute.attnum > 0 
            AND pg_attribute.attrelid = pg_class.oid 
            AND pg_attribute.atttypid = pg_type.oid 
            AND pg_description.objoid = pg_attribute.attrelid 
            AND pg_description.objsubid = pg_attribute.attnum 
            AND pg_class.relname IN ( SELECT tablename FROM pg_tables WHERE schemaname = '{self.database}' AND POSITION ( '_2' IN tablename ) = 0 ) 
        ORDER BY
            pg_class.relname,
            pg_attribute.attnum
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
