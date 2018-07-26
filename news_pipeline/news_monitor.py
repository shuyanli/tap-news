import os
import sys
import logging
import redis
import hashlib #use md5
import datetime


# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import news_api_client
from cloudAMQP_client import CloudAMQPClient


SLEEP_TIME_IN_SECONDS = 10
NEW_TIME_OUT_IN_SECOND = 3600 * 24 * 3

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://nltivjvc:d2aKEaRE-wNLT20RHngTFNnF1DxTLXzA@otter.rmq.cloudamqp.com/nltivjvc"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"

NEWS_SOURCES = [
    'bbc-news',
    'bbc-sport',
    'bloomberg',
    'cnn',
    'entertainment-weekly',
    'espn',
    'ign',
    'techcrunch',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post'
]

logger_format = '%(asctime)s - %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('news_monitor')
logger.setLevel(logging.DEBUG)

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
cloudAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)


def run ():
    while True:
        news_list = news_api_client.getNewsFromSources(NEWS_SOURCES)

        num_of_new_news = 0

        for news in news_list:
            news_digest = hashlib.md5(news['title'].encode('utf-8')).hexdigest()

            if redis_client.get(news_digest) is None:
                num_of_new_news += 1
                news['digest'] = news_digest

                #加时间是因为后面做去重需要最近的新闻,而有的新闻自己不带这个时间戳
                if news['publishedAt'] is None:
                    news['publishedAt'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

                redis_client.set(news_digest, True) #value是什么无所谓, 确保key在就行了
                redis_client.expire(news_digest, NEW_TIME_OUT_IN_SECOND)

                #send the news in queue
                cloudAMQP_client.sendMessage(news)

        logger.info("Fetched %d news" , num_of_new_news)
        cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)  #这个while循环每10秒循环一次



if __name__ == "__main__":
    run()