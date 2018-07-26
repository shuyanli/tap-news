from cloudAMQP_client import CloudAMQPClient

TEST_AMPQ_URL = 'amqp://jcaunwhv:WLJyL7lp7Hhu8ry62yyub6vNoNb1BRaw@otter.rmq.cloudamqp.com/jcaunwhv'
TEST_QUEUE_NAME = 'test'

def test_basic():
    client = CloudAMQPClient(TEST_AMPQ_URL, TEST_QUEUE_NAME)
    message = {'test': 'test'}
    client.sendMessage(message)
    client.sleep(5)
    receivedMessage = client.getMessage()

    assert message == receivedMessage
    print ('test passed')


if __name__ == "__main__":
    test_basic()