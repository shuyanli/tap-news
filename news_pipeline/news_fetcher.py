import os
import sys
import logging
from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from cloudAMQP_client import CloudAMQPClient

#comes from this queue
SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://nltivjvc:d2aKEaRE-wNLT20RHngTFNnF1DxTLXzA@otter.rmq.cloudamqp.com/nltivjvc"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"


#send out from this queue
DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://nltivjvc:d2aKEaRE-wNLT20RHngTFNnF1DxTLXzA@otter.rmq.cloudamqp.com/nltivjvc"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap-news-dedupe-news-task-queue"

SLEEP_TIME_IN_SECONDS = 5


logger_format = '%(asctime)s - %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('news_fetcher')
logger.setLevel(logging.DEBUG)

scrape_news_queue_client  = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
dedupe_news_queue_client  = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)


def handle_message (msg):
    if not isinstance(msg, dict):  #如果msg不属于dict或者json类
        logger.warning('message is broken')
        return


    article = Article(msg['url'])
    article.download()
    article.parse()


    msg['text'] = article.text
    dedupe_news_queue_client.sendMessage(msg)






def run():
    while True:
        if scrape_news_queue_client is not None:
            msg = scrape_news_queue_client.getMessage()
            if msg is not None:
                try:
                    handle_message(msg)
                except Exception as e:
                    logger.warning(e)
                    pass

            scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)  #这里为什么不往回空格对齐第一句if?



if __name__ == "__main__":
    run()
