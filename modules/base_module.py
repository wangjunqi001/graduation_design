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
    
    def init(self):
        return
    
    def create_module(self, table_name, create_sql):
        self.cursor.execute(create_sql % (table_name))
        self.conn.commit()

