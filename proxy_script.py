import json
# from pymongo import MongoClient
from db_conn import Mongo_Conner

# username = 'test'
# password = 'test'
mongo_host = '127.0.0.1'
mongo_port = 27017
db_name = 'weibo'
mg = Mongo_Conner(mongo_host, mongo_port,db_name)

print(mg)
# gsid1 = '1'
# gsid2 = '2'
# uid = 'uid'

# gsid_file=open('gisd.txt',mode='a',encoding='utf-8')

def response(flow):
    global mg
    login_url = 'http://api.weibo.cn/2/account/login'
    repost_url = 'http://api.weibo.cn/2/statuses/repost'
    user_show_url = 'http://api.weibo.cn/2/users/show'

    # if flow.request.url.startswith(login_url):
    #     text=flow.response.text
    #     data=json.loads(text)
    #     if data.get('uid'):
    #         print('采集到gsid数据为',data['uid'])
    #         # data['oauth']=data['oauth2.0']
    #         # data.pop('oauth2.0')
    #         # data['cookie']['cookie']['sina_com_cn']=data['cookie']['cookie']['.sina.com.cn']
    #         # data['cookie']['cookie']['sina_cn'] = data['cookie']['cookie']['.sina.cn']
    #         # data['cookie']['cookie']['weibo_com'] = data['cookie']['cookie']['.weibo.com']
    #         # data['cookie']['cookie']['weibo_cn'] = data['cookie']['cookie']['.weibo.cn']
    #         # del data['cookie']['cookie']['.sina.com.cn']
    #         # del data['cookie']['cookie']['.sina.cn']
    #         # del data['cookie']['cookie']['.weibo.com']
    #         # del data['cookie']['cookie']['.weibo.cn']
    #         uid = data['uid']
    #         gsid1=data['gsid']

    if flow.request.url.startswith(user_show_url):
        # headers = dict(flow.request.headers)
        query = dict(flow.request.query)
        # content = flow.request.get_content()
        # print(headers)
        print(query)
        # print(content)
        # gsid1 = query['gsid']
        param=dict()
        param['_id']=query['uid']
        param['uid'] = query['uid']
        param['gsid']=query['gsid']
        param['s']=query['s']

        # param['ext']=query['ext']
        # param['featurecode']=query['featurecode']

        # param['s']=query['s']


        if mg.get_login_info({'uid':param['uid']}):
           old_param=mg.get_login_info({'uid':param['uid']})
           mg.del_login_info(old_param)
        # mg.insert_login_info(param)
        # gsid_str=json.dumps(param)+"\n"
        # gsid_file = open('F:\mywork\weibo\gisd.txt', mode='a+', encoding='utf-8')
        # gsid_file.write(gsid_str)
        # gsid_file.close()
        mg.insert_login_info(param)
        # mg.close()
        print('存入数据成功')





