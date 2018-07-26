import datetime
import logging
import os
import sys
import news_topic_modeling_service_client

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient

DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://nltivjvc:d2aKEaRE-wNLT20RHngTFNnF1DxTLXzA@otter.rmq.cloudamqp.com/nltivjvc"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap-news-dedupe-news-task-queue"

SLEEP_TIME_IN_SECONDS = 1

NEWS_TABLE_NAME = "news-test"

SAME_NEWS_SIMILARITY_THRESHOLD = 0.9

logger_format = '%(asctime)s - %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('news_deduper')
logger.setLevel(logging.DEBUG)

cloudAMQP_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if not isinstance(msg, dict):  #如果msg不属于dict或者json类
        logger.warning('message is broken')
        return

    text = msg['text']
    if text is None:
        return
    #得到新闻事件当天0点的年月日时分秒, 并且规定范围为此时到一天后
    published_at = parser.parse(msg['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

    #得到范围, 然后再mongoDB中查找在这个范围里的所有新闻,然后变成一个list
    #注意:mongoDB存的时间不是string二十时间戳, 如果是string则gte和lt就不明白这个string怎么比较了
    db = mongodb_client.get_db()
    same_day_news_list = list(db[NEWS_TABLE_NAME].find(
        {'publishedAt': {'$gte':published_at_day_begin,
                         '$lt':published_at_day_end}}))

    if same_day_news_list is not None and len(same_day_news_list) > 0:

        #这个写法学一下, 对same_day_news_list里每一个news, 将他的text拿出来组成一个新的list
        documents = [news['text'] for news in same_day_news_list]

        #比较的母本放到第一个位置
        documents.insert(0, text)

        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T #得到N*N矩阵

        logger.debug("Pairwise Sim:%s", str(pairwise_sim))

        rows, _ = pairwise_sim.shape
        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                logger.info("Duplicated news. Ignore.")
                return

    #如果新的消息不和这一天内的所有消息重复,则视为新消息,存入mongodb
    msg['publishedAt'] = parser.parse(msg['publishedAt'])#存入时间戳

    description = msg['discription']
    if description is None:
        description = msg['title']

    topic = news_topic_modeling_service_client.classify(description)
    msg['class'] = topic

    #upsert为true, 如果没有,则插入,如果有, 则覆盖,upsert = update + insert
    print('saving to mongoDB')
    try:
        db[NEWS_TABLE_NAME].replace_one({'digest':msg['digest']}, msg, upsert=True)
    except Exception as e:
        logger.warning(e)




def run():
    while True:
        if cloudAMQP_client is not None:
            msg = cloudAMQP_client.getMessage()
            if msg is not None:
                # Parse and process the message
                try:
                    handle_message(msg)
                except Exception as e:
                    logger.warning(e)
                    pass

            cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == "__main__":
    run()
