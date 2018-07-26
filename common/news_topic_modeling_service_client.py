#用来调用news_topic_modelinng_service里面对应的service
#如. 写一个classify来调用那边的classify函数, 实现了对那一大堆service file的封装



import jsonrpclib

URL = "http://localhost:6060"

client = jsonrpclib.ServerProxy(URL)

def classify(text):
    topic = client.classify(text)
    print("Topic: %s" % str(topic))
    return topic