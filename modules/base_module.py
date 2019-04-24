import MySQLdb
import DBUtils.PersistentDB as PersistentDB

sys.append("../")
import db_config.db_config as DbConfig

class base_module(Object):
    def __init__(self):
        self.conn_pool = PersistentDB(creator=MySQLdb, maxusage=100, **DbConfig)
    
    # 不允许连接
    def get_connect(self):
        return self.conn_pool.connection()


