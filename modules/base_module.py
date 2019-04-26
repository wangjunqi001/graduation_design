import sys

import MySQLdb
import DBUtils.PersistentDB as PersistentDB

sys.path.append("../")
import db_config as DbConfig

class BaseModule(object):
    def __init__(self):
        self.conn_pool = PersistentDB(creator=MySQLdb, maxusage=100, **DbConfig.db_config)
        self.conn = self.conn_pool.get_connect()       
        self.cursor = self.conn.cursor()
    
    def init(self):
        return
    
    def create_module(self, table_name, create_sql):
        ret = self.cursor.execute("SHOW TABLES LIKE %s" % (table_name))
        if ret == 0 :
            self.cursor.execute(create_sql % (table_name))
            self.conn.commit()

