"""backend service, ready to serve node server"""

import logging

import operations

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer




SERVER_HOST = 'localhost'
SERVER_PORT = 4040

LOGGER_FORMAT = '%(asctime)s,- %(message)s'
logging.basicConfig(format=LOGGER_FORMAT)
LOGGER = logging.getLogger('backend_service') #instantiate
LOGGER.setLevel(logging.DEBUG)


def add(num1, num2):
    """testing method"""
    LOGGER.debug('add is called with %s and %s', num1, num2)
    return num1+num2


def get_one_news():
    """ Test method to get one news """
    LOGGER.debug("getOneNews is called")
    return operations.getOneNews()


def get_news_summaries_for_user(user_id, page_num):
    """get news summaries, not the whole news, for a use"""
    LOGGER.debug("get_news_summaries_for_user is called for user %s, with page number %s", user_id, page_num) #rpc传入的参数都认为是string
    return operations.getNewsSummariesForUser(user_id, page_num)


def log_news_click_for_user(user_id, news_id):
    """log_news_click_for_user called"""
    LOGGER.debug("log_news_click_for_user is called for user %s, and news %s", user_id, news_id) #rpc传入的参数都认为是string
    return operations.logNewsClickForUser(user_id, news_id)


RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))

#第二个参数是暴露给外部提供调用的借口,使用post的时候要和第二个参数的名字一致
RPC_SERVER.register_function(add, 'add')
RPC_SERVER.register_function(get_one_news, 'get_one_news')
RPC_SERVER.register_function(get_news_summaries_for_user, 'getNewsSummariesForUser')
RPC_SERVER.register_function(log_news_click_for_user, 'logNewsClickForUser')

LOGGER.info("Starting RPC server on %s:%d", SERVER_HOST, SERVER_PORT)
RPC_SERVER.serve_forever()
