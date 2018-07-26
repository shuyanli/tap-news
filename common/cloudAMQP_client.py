import pika
import logging
import json

logger_format = '%(asctime)s,- %(message)s'
logging.basicConfig(format = logger_format)
logger = logging.getLogger('cloud_amqp_client') #instantiate
logger.setLevel(logging.DEBUG)


#message queue之所以不用单例是因为: 数据库用单例是为了只需要连接上一个数据库, 然后用一个instance管理这个数据库
#而message queue可能有很多个queue, 如果只有一个instance的话会导致不同的queue之间难以管理
#所以就需要定义一个class, 然后每次如果需要不同的queue就用不同的instance就可以了


class CloudAMQPClient:
    cloud_ampq_url = None
    queue_name = None
    params = None



    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_ampq_url = cloud_amqp_url
        self.queue_name = queue_name
        self.params = pika.URLParameters(cloud_amqp_url) #通过URL连接
        self.params.socket_timeout = 3
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    #send one massage, 这样包裹send和get,以后就不需要每一次都去basic_publish然后传一大堆自定义参数了
    def sendMessage(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=json.dumps(message))  #serialize
        logger.debug(" [x] Sent to  %s: %s "%(self.queue_name, message))

    #copied from the api document(basic_get: get one message)
    def getMessage(self):
        method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
        if method_frame:
            logger.debug(" [x] Receive message from  %s: %s "%(self.queue_name, body))
            self.channel.basic_ack(method_frame.delivery_tag) #验证你真正的收到了,而不是别人恶意发的,所以还给我一个证明tag
            return json.loads(body.decode('utf-8'))  #deserialize
        else:
            logger.debug("no message returned")
            return None

    #保持心跳的sleep, 否则如果直接用系统的sleep就断掉连接了
    def sleep(self, seconds):
        self.connection.sleep(seconds)
