import sys

import MySQLdb
from DBUtils.PersistentDB import PersistentDB as PersistentDB

sys.path.append("../")
import db_config as DbConfig

class BaseModule(object):
    def __init__(self):
        self.conn_pool = PersistentDB(creator=MySQLdb, maxusage=100, **DbConfig.db_config)
        self.conn = self.conn_pool.connection()       
        self.cursor = self.conn.cursor()
        self.module_name = ""
    
    def init(self):
        return
    
    def create_module(self, table_name, create_sql):
        self.cursor.execute(create_sql % (table_name))
        self.conn.commit()

    def select(self, table_name="", field_content="*", condition=""):
        if table_name == "":
            return None
        select_sql = "SELECT " + field_content + " FROM " + table_name
        if condition != "":
            select_sql += (" WHERE " + condition)
        self.cursor.execute(select_sql)

        return self.cursor.fetchall()

    def update(self, table_name="", update_expr="", condition=""):
        if table_name == "" or condition == "":
            return
        update_sql = "UPDATE " + table_name + " SET " + update_expr
        if condition != "":
            update_sql += " WHERE " + condition 
        self.cursor.execute(update_sql)
        self.conn.commit()















