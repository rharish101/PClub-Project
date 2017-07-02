#!/bin/python2
import os
import codecs
import numpy as np
from gensim.parsing.preprocessing import preprocess_string, strip_punctuation,\
                                         stem_text
from gensim.models.word2vec import Word2Vec
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.layers.recurrent import LSTM

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

def bigrams(tweets=None, labels=None, wv_model=None):
    if not tweets and not labels:
        tweets, labels = export()
    elif tweets and labels:
        pass
    else:
        print "One of tweets or labels given, but not the other"
        return
    if not wv_model:
        wv_model = word2vec(tweets)

    # Shuffle the dataset
    data = zip(tweets, labels)
    np.random.shuffle(data)
    tweets, labels = zip(*data)
    del data

    num_bigrams = 0
    for i in range(len(tweets)):
        for j in range(len(tweets[i]) - 1):
            num_bigrams += 1
    bigram_tweets = np.array([[wv_model.wv['happy'.decode('ISO-8859-1')],
                               wv_model.wv['sad'.decode('ISO-8859-1')]] for i in\
                               range(num_bigrams)])
    bigram_labels = []
    counter = 0
    print "Generating bigrams with word vectors..."
    for i in range(len(tweets)):
        for j in range(len(tweets[i]) - 1):
            bigram_tweets[counter] = np.array([wv_model.wv[tweets[i][j]],
                                               wv_model.wv[tweets[i][j + 1]]])
            bigram_labels.append(labels[i])
            counter += 1
    bigram_labels = np.array(bigram_labels)
    del tweets
    del labels
    del model

    return (bigram_tweets, bigram_labels)

def create_word2vec(tweets):
    wv_model = Word2Vec(size=100, alpha=0.1, window=2, min_count=0, workers=8,
                     min_alpha=0.01)
    print "Created Word2Vec model\nBuilding vocabulary..."
    wv_model.build_vocab(tweets)
    print "Training..."
    wv_model.train(tweets, total_examples=wv_model.corpus_count, epochs=10)
    print "Trained"
    wv_model.save('./model_word2vec')
    print "Model saved"
    return wv_model

def word2vec(tweets=None):
    if 'model_word2vec' in os.listdir('.'):
        response = raw_input('Word2Vec model found. Do you want to load it?'\
                             '(Y/n): ')
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

def create_nn():
    nn_model = Sequential()
    nn_model.add(LSTM(128, input_shape=(2, 100)))
    nn_model.add(Dense(64, activation='relu'))
    nn_model.add(Dense(1, activation='sigmoid'))

    nn_model.compile(loss='categorical_crossentropy', optimizer='rmsprop',
                     metrics=['accuracy'])

    return nn_model

def nn():
    if 'model_nn.h5' in os.listdir('.'):
        response = raw_input('Neural network model found. Do you want to load'\
                             'it? (Y/n): ')
        if response.lower() in ['n', 'no', 'nah', 'nono', 'nahi', 'nein']:
            return create_nn()
        else:
            print "Loading model..."
            nn_model = load_model('model_nn.h5')
            print "Loaded model"
            return nn_model
    else:
        return create_nn()

