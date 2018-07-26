import os
import sys
import logging
import operator

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client

LOGGER_FORMAT = '%(asctime)s,- %(message)s'
logging.basicConfig(format=LOGGER_FORMAT)
LOGGER = logging.getLogger('recommendation service') #instantiate
LOGGER.setLevel(logging.DEBUG)
PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"

SERVER_HOST = 'localhost'
SERVER_PORT = 5050


# https://www.python.org/dev/peps/pep-0485/#proposed-implementation
def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)



def getPreferenceForUser (userId):
    """ If you call this API, you pass in an userid, the API will return a sorted list according to the preference """
    db =mongodb_client.get_db()
    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId':userId})

    if model is None:
        return []

    """
        dict.items 返回一个tuple(key value pairs), 如:dict_items([('a', 1), ('b', 2), ('c', 4), ('d', 3)])
        然后加上list(), 变成[('a', 1), ('b', 2), ('c', 4), ('d', 3)])
        根据key来排序,这里key为第二个元素(即value), 从高到低
        print(sorted_tuples) => [('c', 4), ('d', 3), ('b', 2), ('a', 1)]
    """
    sorted_tuples = sorted(list(model['preference'].items()), key=operator.itemgetter(1), reverse=True)

    """
       print(sorted_list) => ['c', 'd', 'b', 'a']
    """
    sorted_list = [x[0] for x in sorted_tuples]
    sorted_value_list = [x[1] for x in sorted_tuples]

    #如果所有值都相等, 就等于没有preference, 返回空
    if isclose(float(sorted_value_list[0]), float(sorted_value_list[-1])):
        return []
    return sorted_list


RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(getPreferenceForUser, 'getPreferenceForUser')
LOGGER.info("Starting RPC server for recommendation service on %s:%d", SERVER_HOST, SERVER_PORT)
RPC_SERVER.serve_forever()