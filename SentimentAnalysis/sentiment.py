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
    labels = np.array([tweet[0] for tweet in data])
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
    backup = np.array(tweets)
    tweets = []
    for tweet in backup:
        if len(tweet) >= 2:
            tweets.append(tweet)
    tweets = np.array(tweets)
    del backup

    return (tweets, labels)

