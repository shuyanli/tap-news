"""backend service, ready to serve node server"""
import os
import sys
import json
import redis
import pickle
from datetime import datetime
from bson.json_util import dumps


#import mongodb_client  因为没有做成package, 所以service.py看不到common底下的这些文件, 所以不能直接这么做
#获得当前路径, (backend_server), 加上utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client
from cloudAMQP_client import CloudAMQPClient
import news_recommendation_service_client

LOG_CLICK_TASK_QUEUE_URL = 'amqp://cbutfrav:ML2tXxDLHj_y3eTX1phhJjJ7Ex1iN13g@otter.rmq.cloudamqp.com/cbutfrav'
LOG_CLICK_TASK_QUEUE_NAME = 'tap-name-log-clicks-task-queue'
cloudAMQP_client = CloudAMQPClient(LOG_CLICK_TASK_QUEUE_URL,LOG_CLICK_TASK_QUEUE_NAME)


REDIS_HOST = "localhost"
REDIS_PORT = 6379
NEWS_TABLE_NAME = "news"
NEWS_LIST_BATCH_SIZE = 10
NEWS_LIMIT = 500
USER_NEWS_TIME_OUT_IN_SECONDS = 60*60
redis_client = redis.StrictRedis()

def getOneNews():

    db = mongodb_client.get_db()
    news = db[NEWS_TABLE_NAME].find_one()
    return json.loads(dumps(news)) #dumps是因为mongoDB存储形式是BSON, 需要用dumps把它变回来,然后再loads反序列化


def getNewsSummariesForUser(user_id, page_num):
    page_num = int(page_num)
    if page_num <= 0:
        return []

    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE #included
    end_index = page_num * NEWS_LIST_BATCH_SIZE         #not included

    sliced_news = []  #返回前端一个没有正文内容但是包括其他一切的news list
    db = mongodb_client.get_db()

    if redis_client.get(user_id) is not None:
        news_digests = pickle.loads(redis_client.get(user_id))
        sliced_news_digests = news_digests[begin_index:end_index]
        #sliced_news = list(db[NEWS_TABLE_NAME].find({'digest': {$in: [sliced_news_digests] } }))#todo 试试这个行不行=>不行
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest':{'$in':sliced_news_digests}}))

    else:
        #total_news = list(db[NEWS_TABLE_NAME].find().sort({'publishedAt': -1}).limit(NEWS_LIMIT)) #todo=>这个可以
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        total_news_digests = [x['digest'] for x in total_news] #之前用到类似用法, 将total_news中每一个'digest'拼成一个list

        #save this list to redis
        redis_client.set(user_id, pickle.dumps(total_news_digests))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)
        sliced_news = total_news[begin_index:end_index]


    # Get preference for the user
    # TODO: use preference to customize returned news list.
    preference = news_recommendation_service_client.getPreferenceForUser(user_id)
    topPreference = None

    if preference is not None and len(preference) > 0:
        topPreference = preference[0]

    for news in sliced_news:
        # Remove text field to save bandwidth.
        del news['text']
        if news['class'] == topPreference:
            news['reason'] = 'Recommend'

    return json.loads(dumps(sliced_news))


def logNewsClickForUser(user_id, news_id):
    message = {'userId':user_id,'newsId':news_id, 'timestemp': str(datetime.utcnow())}
    cloudAMQP_client.sendMessage(message)


