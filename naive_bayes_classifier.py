import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
import os.path
import pickle
from sklearn import cross_validation

stop_words = set(stopwords.words('english'))

negation_words = ["not", "isn't", "wasn't", "aren't", "weren't"]

def word_feats(words):
    feats = []
    negation = False
    for word in words:
        if word in negation_words:
            negation = True
        else:
            if word not in stop_words:
                if negation == True:
                    feats.append((("not_" + word), True))
                    negation = False
                else:
                    feats.append((word, True))
    return dict(feats)

    # Remove stop words and *try* to account for negation.

def generate_classifier():

    pos_tweets = []
    neg_tweets = []

    with open('labelled_tweets.positive', "r") as f:
        for line in f:
            pos_tweets.append((word_feats(line.split()), 'pos'))

    with open('labelled_tweets.negative', "r") as f:
        for line in f:
            neg_tweets.append((word_feats(line.split()), 'neg'))

    pos_train, pos_test = cross_validation.train_test_split(pos_tweets, test_size=0.2)
    neg_train, neg_test = cross_validation.train_test_split(neg_tweets, test_size=0.2)

    classifier = NaiveBayesClassifier.train(pos_train + neg_train)
    
    # print 'Accuracy:', nltk.classify.util.accuracy(classifier, pos_test + neg_test)

    return classifier

def load_classifier():

    if os.path.isfile("naive_bayes_classifier.pickle"):

        with open("naive_bayes_classifier.pickle", "rb") as f:
            classifier = pickle.load(f)

        return classifier

    else:

        classifier = generate_classifier()

        with open("naive_bayes_classifier.pickle", "wb") as f:
            pickle.dump(classifier, f)

        return classifier
