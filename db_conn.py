# -*- coding:utf-8 -*-
import pymongo
from pymongo.errors import ConnectionFailure

class Mongo_Conner:
    def __init__(self,ip,port,db_name):
        try:
            self.conn = pymongo.MongoClient(ip,port)
            db_auth = self.conn[db_name]
            # db_auth.authenticate(username, pwd)
            self.db = db_auth
        except ConnectionFailure :
            print('mongodb server not available')
            pass

    # 微博登录信息集合
    @property
    def login_info_collection(self):
        return self.db.weibo_login_info

    def get_login_info(self,login_info):
        return self.login_info_collection.find_one(login_info)

    def insert_login_info(self,login_info):
        try:
            self.login_info_collection.insert_one(login_info)
        except Exception as e:
            print('存入数据出错：',str(e))

    def del_login_info(self,login_info):
        self.login_info_collection.remove(login_info)


if __name__ == '__main__':
    mongo_host = '127.0.0.1'
    mongo_port = 27017
    db_name = 'weibo'
    # username = 'test'
    # password = 'test'

    mg = Mongo_Conner(mongo_host,mongo_port,db_name)


    # print(mg.db)
    print( mg.login_info_collection)
    # print(mg.user_video_info_collection)
    mg.insert_login_info({'uid':'12321312123'})


