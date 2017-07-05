#!/bin/python2
import os
import codecs
import sys
import numpy as np
from gensim.parsing.preprocessing import preprocess_string, strip_punctuation,\
                                         stem_text
from gensim.models.word2vec import Word2Vec
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.layers.recurrent import LSTM
from keras.callbacks import TensorBoard, EarlyStopping, ReduceLROnPlateau
import time

def export(type_data='train'):
    print "Extracting data..."
    if type_data.lower() == 'train':
        filename = 'training.1600000.processed.noemoticon.csv'
    elif type_data.lower() == 'test':
        filename = 'testdata.manual.2009.06.14.csv'
    data_file = codecs.open('Sentiment140/' + filename, encoding='ISO-8859-1')
    data = []
    for tweet in data_file.read().split('\n')[:-1]:
        data.append([string for string in tweet.split('"') if string not in [
                    '', ',']])
    data_file.close()
    labels = [(float(tweet[0]) / 4) for tweet in data]
    tweets = [tweet[-1] for tweet in data]

    print "Preprocessing data..."
    for i, tweet in enumerate(tweets):
        new_tweet = ' '.join([word for word in tweet.split(' ') if len(word)\
                            > 0 and word[0] not in ['@', '#'] and 'http' not\
                            in word]).strip()
        pro_tweet = preprocess_string(new_tweet)
        if len(pro_tweet) < 2:
            tweets[i] = strip_punctuation(stem_text(new_tweet.lower())).\
                        strip().split()
        else:
            tweets[i] = pro_tweet

    print "Cleaning data..."
    backup_tweets = np.array(tweets)
    backup_labels = np.array(labels)
    tweets = []
    labels = []
    for i, tweet in enumerate(backup_tweets):
        if len(tweet) >= 2:
            tweets.append(tweet)
            labels.append(backup_labels[i])
    del backup_tweets
    del backup_labels

    return (tweets, labels)

def create_word2vec(tweets):
    wv_model = Word2Vec(size=100, alpha=0.1, window=2, min_count=0, workers=8,
                     min_alpha=0.01)
    print "Created Word2Vec model\nBuilding vocabulary..."
    wv_model.build_vocab(tweets)
    print "Training..."
    wv_model.train(tweets, total_examples=wv_model.corpus_count, epochs=10)
    print "Trained"
    wv_model.save('model_word2vec')
    print "Model saved"
    return wv_model

def get_word2vec(tweets=None):
    if 'model_word2vec' in os.listdir('.'):
        response = raw_input('Word2Vec model found. Do you want to load it?'\
                             ' (Y/n): ')
        if response.lower() in ['n', 'no', 'nah', 'nono', 'nahi', 'nein']:
            if not tweets:
                tweets, labels = export()
                del labels
            return create_word2vec(tweets)
        else:
            print "Loading model..."
            wv_model = Word2Vec.load('./model_word2vec')
            print "Loaded model"
            return wv_model
    else:
        if not tweets:
            tweets, labels = export()
            del labels
        return create_word2vec(tweets)

def init_with_wv(tweets=None, labels=None, wv_model=None, type_data='train'):
    if not tweets and not labels:
        tweets, labels = export(type_data)
    elif tweets and labels:
        pass
    else:
        print "One of tweets or labels given, but not the other"
        return
    if not wv_model:
        wv_model = get_word2vec(tweets)

    print "Replacing words with word vectors..."
    tweets_wv = []
    max_tweet_len = 0
    for tweet in tweets:
        if len(tweet) > max_tweet_len:
            max_tweet_len = len(tweet)
    vocab = wv_model.wv.vocab.keys()
    for tweet_num, tweet in enumerate(tweets):
        sys.stdout.write("\r%d tweet(s) being replaced out of %d\r" % (
                         tweet_num + 1, len(tweets)))
        sys.stdout.flush()
        current_tweet = []
        for word in tweet:
            if word in vocab:
                current_tweet.append(wv_model.wv[word])
        if len(current_tweet) < max_tweet_len:
            current_tweet_len = len(current_tweet)
            for i in range(max_tweet_len - current_tweet_len):
                current_tweet.append(np.zeros(100))
        tweets_wv.append(current_tweet)
    print "\nReplaced words with word vectors"
    tweets_wv = np.array(tweets_wv)
    del tweets
    return (tweets_wv, labels)

def create_nn(max_tweet_len=None):
    if vocab_len == None:
        print "Error: Please specify max tweet length"

    nn_model = Sequential()
    nn_model.add(LSTM(128, input_shape=(max_tweet_len, 100)))
    nn_model.add(Dense(64, activation='relu'))
    nn_model.add(Dense(1, activation='sigmoid'))

    nn_model.compile(loss='binary_crossentropy', optimizer='rmsprop',
                    metrics=['accuracy'])

    print "Created neural network model"
    return nn_model

def get_nn(max_tweet_len=None):
    if 'model_nn.h5' in os.listdir('.'):
        response = raw_input('Neural network model found. Do you want to load'\
                            'it? (Y/n): ')
        if response.lower() in ['n', 'no', 'nah', 'nono', 'nahi', 'nein']:
            return create_nn(max_tweet_len)
        else:
            print "Loading model..."
            nn_model = load_model('model_nn.h5')
            print "Loaded model"
            return nn_model
    else:
        return create_nn(vocab_len)

def train_nn(tweets=None, labels=None, nn_model=None):
    if not tweets and not labels:
        tweets, labels = init_with_wv()
    elif tweets and labels:
        pass
    else:
        print "One of tweets or labels given, but not the other"
        return
    max_tweet_len = max([len(tweet) for tweet in tweets])
    if not nn_model:
        nn_model = get_nn(max_tweet_len)

    # Callbacks (extra features)
    tb_callback = TensorBoard(log_dir='./Tensorboard/' + str(time.time()))
    early_stop = EarlyStopping(monitor='loss', min_delta=0.1, patience=10)
    lr_reducer = ReduceLROnPlateau(monitor='loss', factor=0.5, min_lr=0.00001,
                                patience=3, epsilon=0.2)

    nn_model.fit(tweets, labels, epochs=10, batch_size=100, callbacks=
                [tb_callback, early_stop, lr_reducer], validation_split=0.2)
    nn_model.save('model_nn.h5')

train_nn()

