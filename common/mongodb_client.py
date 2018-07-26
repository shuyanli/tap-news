from pymongo import MongoClient

MONGO_DB_HOST = 'localhost'
MONGO_DB_PORT = 27017
DB_NAME = 'tap-news'

#use singleton:数据库有链接限制, 如,同时支持十个连接, 所以有一个thread pool(connection pool)来维护连入.
#pymongo实现了这个pool的支持, 使用统一的mongoclient 就能自动实现线程池的管理, 所以这里需要一个单例
client = MongoClient(MONGO_DB_HOST, MONGO_DB_PORT)

#对于这个方程,如果你调用的时候不传入参数,就是用默认的dbname, 否则使用你传入的dbname
#这是python方便的地方, 不需要根据不同的传入参数来overload多个接口
def get_db(db = DB_NAME):
    db = client[db]  #都是调用client这一个singleton
    return db