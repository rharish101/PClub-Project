#!/bin/python2
import codecs
import numpy as np
from gensim.parsing.preprocessing import preprocess_string, strip_punctuation,\
                                         stem_text

def export():

    print "Extracting data..."
    data_file = codecs.open('Sentiment140/training.1600000.processed.'
                            'noemoticon.csv', encoding='ISO-8859-1')
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
        pro_tweet = np.array(preprocess_string(new_tweet))
        if len(pro_tweet) < 2:
            tweets[i] = np.array(strip_punctuation(stem_text(new_tweet.lower()
                                 )).strip().split())
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
    tweets = np.array(tweets)
    labels = np.array(labels)
    del backup_tweets
    del backup_labels

    num_bigrams = 0
    for i in range(len(tweets)):
        for j in range(len(tweets[i]) - 1):
            num_bigrams += 1
    bigram_tweets = np.array([['qwertyuiop'.decode('ISO-8859-1'),
                               'qwertyuiop'.decode('ISO-8859-1')] for i in\
                               range(num_bigrams)])
    bigram_labels = []
    counter = 0
    print "Generating bigrams..."
    for i in range(len(tweets)):
        for j in range(len(tweets[i]) - 1):
            bigram_tweets[counter] = np.array([tweets[i][j], tweets[i][j + 1]])
            bigram_labels.append(labels[i])
            counter += 1
    bigram_labels = np.array(bigram_labels)
    del tweets
    del labels

    return (bigram_tweets, bigram_labels)

