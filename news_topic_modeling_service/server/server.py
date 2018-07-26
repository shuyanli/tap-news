import news_classes
import numpy as np
import os
import pandas as pd
import pickle
import sys
import tensorflow as tf
import time

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from tensorflow.contrib.learn.python.learn.estimators import model_fn
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# import packages in trainer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'trainer'))
import news_cnn_model

learn = tf.contrib.learn

SERVER_HOST = 'localhost'
SERVER_PORT = 6060

MODEL_DIR = '../model'
MODEL_UPDATE_LAG_IN_SECONDS = 10

N_CLASSES = 8

VARS_FILE = '../model/vars'
VOCAB_PROCESSOR_SAVE_FILE = '../model/vocab_procesor_save_file'

n_words = 0

MAX_DOCUMENT_LENGTH = 500
vocab_processor = None

classifier = None

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def restoreVars():
    with open(VARS_FILE, 'rb') as f:
        global n_words
        #不写global的话, 即使外面的是global变量, 下面这行里这个n_words就会报错
        n_words = pickle.load(f)

    #从保存的文件中能还原回来
    global vocab_processor #训练时有多少unique word的记录,这个要传承下来
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(
        VOCAB_PROCESSOR_SAVE_FILE)


def loadModel():
    global classifier
    classifier = learn.Estimator(
        model_fn=news_cnn_model.generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_DIR)
    # Prepare training and testing
    df = pd.read_csv('../data/labeled_news.csv', header=None)

    # TODO: fix this until https://github.com/tensorflow/tensorflow/issues/5548 is solved(bug).
    # =>  We have to call evaluate or predict at least once to make the restored Estimator work.
    # 为了绕开上面的bug, 要么换estimator, 要么随意挑一个数据运行一下model,里面的参数就回来了
    train_df = df[0:400]
    x_train = train_df[1]
    x_train = np.array(list(vocab_processor.transform(x_train)))
    y_train = train_df[0]
    classifier.evaluate(x_train, y_train)

    print("Model update.")


restoreVars()
loadModel()

print("Model loaded.")

#用看门狗"盯着"一个目录看, 如果有盯着的地方有任何变化, 重新渲染存的各种值和model
class ReloadModelHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # Reload model
        print("Model update detected. Loading new model.")
        time.sleep(MODEL_UPDATE_LAG_IN_SECONDS)
        restoreVars()
        loadModel()


# Setup watchdog
observer = Observer()
observer.schedule(ReloadModelHandler(), path=MODEL_DIR, recursive=False)
observer.start()


def classify(text):
    #训练阶段如何预处理数据,在新数据来的时候也要先这样预处理, 才能使数据的结构和构成一致, 使得预测模型更精确通用
    text_tokens = word_tokenize(text)
    stemmed_tokens = [stemmer.stem(w.lower()) for w in text_tokens if not w in stop_words]
    norm_sentence = ' '.join(stemmed_tokens)

    text_series = pd.Series([norm_sentence])
    predict_x = np.array(list(vocab_processor.transform(text_series)))
    print(predict_x)

    #得到预测的值
    y_predicted = [
        p['class'] for p in classifier.predict(
            predict_x, as_iterable=True)
    ]
    print(y_predicted[0])
    #查表后得到对应的class
    topic = news_classes.class_map[str(y_predicted[0])]
    return topic


# Threading RPC Server
RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(classify, 'classify')

print(("Starting RPC server on %s:%d" % (SERVER_HOST, SERVER_PORT)))

RPC_SERVER.serve_forever()