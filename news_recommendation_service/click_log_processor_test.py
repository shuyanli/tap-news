import click_log_processor
import os
import sys

from datetime import datetime

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client

PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"
NEWS_TABLE_NAME = "news"

NUM_OF_CLASSES = 8

TEST_NEWS_DIGEST = "nmuYSK3LFDb7SY727Ibonw==\n"


def test_basic():
    db = mongodb_client.get_db()

    db[PREFERENCE_MODEL_TABLE_NAME].delete_many({'userId':'test_user'})

    msg = {'userId':'test_user', 'newsId':TEST_NEWS_DIGEST, 'timestamp':str(datetime.utcnow())}

    click_log_processor.handle_message(msg)

    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId':'test_user'})

    print(model)

    assert model is not None
    assert len(model['preference']) == NUM_OF_CLASSES


if __name__ == "__main__":
    test_basic()