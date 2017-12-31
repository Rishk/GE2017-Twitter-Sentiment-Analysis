# GE2017 Twitter Sentiment Analysis
> Sentiment analysis of many millions of tweets throughout the 2017 UK General Election using a naive Bayes classifier.

## Introduction
As a part of an independent research project looking into how social media can be used to understand political sentiment, I conducted sentiment analysis of many millions of tweets throughout the 2017 UK General Election.

In my analysis, I used the volumes of positive and negative tweets about various parties and topics over time. I settled with the naive Bayes classifier for its processing speed, effectiveness in sentiment analysis (the independence of attributes, in this case words, is mostly true) and overall accuracy, which was 77% after optimisation.

The scripts I used to handle the data and carry out this sentiment analysis can be found here, however, I have not supplied the raw tweets, training data or processed data. To find out more about the project as a whole, the visualisations of sentiment analysis and what I concluded, please get in touch with me.

## Files
|File Name|Function|Input|Output|
|---|---|---|---|
|stream_twitter_data.py|Collect tweets about the 2017 General Election from Twitter using the Twitter Streaming API.|Streaming filters.|[Raw tweets](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object)* in files of the form _twitter-ge#.txt_.|
|naive_bayes_classifier.py|Train, test and store the naive Bayes classifier so it can be used when processing the tweets. This script is imported by _process_raw_twitter_data.py_.|Training and testing data.|Trained naive Bayes classifier (_naive_bayes_classifier.pickle_) and its accuracy.|
|process_raw_twitter_data.py|Process the raw data from Twitter: label each tweet based on its content, classify the sentiment of each tweet and add it to the appropriate file based on its date.|Raw tweets in files of the form _twitter-ge#.txt_.|Labelled and classified tweets in files of the form _dd-mm-yyyy.txt_. Each file contains all tweets for the given date.|
|generate_dataframes.py|Load all the processed data into a pandas DataFrame so it can be analysed. Parameters for filtering include: political parties, daily or weekly, topic (e.g. Brexit, healthcare).|Labelled and classified tweets in files of the form _dd-mm-yyyy.txt_.|A pandas DataFrame containing the volumes of positive and negative tweets for each specific party over time, filtered based on the given parameters.|

*Note: the content of tweet objects changes over time and hence may not contain the same information as it did for this project.

## Dependencies
* **Python Version**: 2.7.12
* **Python Libraries**: nltk, numpy, pandas, sklearn, tweepy
* **Hardware**: This project has been programmed such that processing the many millions of tweets does not require specialist hardware. Having said this, the raw Twitter data was in excess of 100GB, which may be an issue in some cases. The data could be processed on a rolling basis if space is limited.
    * **Note**: when streaming the Twitter data, I used a Raspberry Pi as the script runs 24/7 - I highly recommend a setup like this if you are going to stream your own data.

## Further Improvements
 * Improve the sentiment analysis classifier through better handling of negation, identification of non-genuine tweets and classification of sarcasm and humour.
    * This could involve moving away from a naive Bayes classifier.
 * Profile users anonymously to better understand the demographic of users tweeting.