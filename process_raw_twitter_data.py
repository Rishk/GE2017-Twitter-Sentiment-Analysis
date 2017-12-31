import datetime
import json

import naive_bayes_classifier as nbc
# This imports the "naive_bayes_classifier.py" script that will either load
# the saved classifier or generate it if the file doesn't exist.

# ---------------------------- Functions ----------------------------

def check_contents(tweet_string, terms):

    if any(word in tweet_string.lower() for word in terms):
        return 1
    else:
        return 0

def month_string_to_number(month_string):

    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    
    return months.index(month_string.lower()) + 1

def classify_tweet_sentiment(tweet_string, classifier):

    tweet_feats = nbc.word_feats(tweet_string)

    probabilities = classifier.prob_classify(tweet_feats)
    positive_p = probabilities.prob("pos")
    negative_p = probabilities.prob("neg")
                            
    compound_score = positive_p - negative_p

    classification = classifier.classify(tweet_feats)

    sentiment_score = 0

    if (compound_score <= 0.05) and (compound_score >= -0.05):
        
        return 0

        # Neutral tweets.

    else:

        if classification == "pos":
            return 1
        else:
            return -1

# ------------------------- End of Functions -------------------------

file_open = "N/A"

classifier = nbc.load_classifier()

# The program loops through through the specified Twitter files containing
# raw data and processes them as required. The raw data is in files of the
# form 'twitter-ge{number}.txt'.

# Once processed, each tweet is added to a file of the form 'dd-mm-yyyy.txt'
# depending on the day it was tweeted.

start_file = 1
end_file = 20

# This example loops through all files between twitter-ge1.txt and
# twitter-ge20.txt inclusive.

for i in range (start_file, end_file + 1):
    with open('twitter-ge' + str(i) + '.txt', "r") as infile:
        for line in infile:
            try:
                tweet = json.loads(line)

                tweet_id = tweet.get('id_str', None)
                tweet_string = tweet.get('text', None)
                
                if tweet_string[:2] != "RT":

                    # Try to catch retweets.

                    tory = check_contents(tweet_string, ['theresa may', 'theresa_may', 'theresamay', 'uk prime minister', 'number10gov', 'conservatives', 'tories', 'tory'])
                    labour = check_contents(tweet_string, ['corbyn', 'jeremy corbyn', 'jeremycorbyn', 'opposition leader', 'uklabour', 'labour party', 'labour government', 'labour'])
                    libdems = check_contents(tweet_string, ['farron', 'tim farron', 'timfarron', 'libdem', 'libdems', 'liberal democrats', 'lib dems'])
                    ukip = check_contents(tweet_string, ['nuttall', 'paul nuttall', 'paulnuttall', 'paulnuttallukip', 'ukip'])
                    
                    party_total = tory + labour + libdems + ukip

                    if party_total == 1:

                        # Remove any tweets that mention more than one party
                        # as we cannot differentiate the sentiment based on
                        # each political party in the tweet.

                        # Example: "The Conservatives are doing a great job,
                        # unlike Labour!"

                        # The sentiment analysis algorithm would not be able to
                        # tag Conservatives as positive and Labour as negative.

                        # We also want to remove any tweets that do not have
                        # any political parties associated with them.
                        
                        healthcare = check_contents(tweet_string, ['healthcare', 'hospital', 'nhs'])
                        economy = check_contents(tweet_string, ['economy', 'industry', 'inflation', 'jobs', 'national debt'])
                        immigration = check_contents(tweet_string, ['borders', 'immigration', 'terrorism'])
                        education = check_contents(tweet_string, ['education', 'school'])
                        defence = check_contents(tweet_string, ['defence', 'defense', 'nuclear', 'trident'])
                        brexit = check_contents(tweet_string, ['brexit', 'european union', 'eu'])
                        pension = check_contents(tweet_string, ['pension'])
                    
                        sentiment_score = classify_tweet_sentiment(tweet_string, classifier)
                        
                        followers = tweet['user']['followers_count']
                        
                        verified = 0
                        
                        if tweet['user']['verified'] == True:
                            verified = 1
                        
                        # Strip relevant date and time info from the tweet.
                        
                        month_number = month_string_to_number(tweet.get('created_at', None)[4:7])
                        day_number = int(tweet.get('created_at', None)[8:10])
                        
                        hour = int(tweet.get('created_at', None)[11:13])
                        minute = int(tweet.get('created_at', None)[14:16])
                        
                        tweet_date = datetime.datetime(2017, month_number, day_number, hour, minute)
                        
                        date_created = tweet_date.strftime('%d-%m-%Y')
                        time = tweet_date.strftime('%H:%M')
                
                        country = ""
                        
                        if tweet['place'] is not None:
                            country = tweet['place']['country']                    
                        
                        tweet_data = [tweet_id, sentiment_score, tory, labour, libdems, ukip, healthcare, economy, immigration, education, defence, brexit, pension, followers, verified, time, country]

                        if file_open == "N/A":

                            # If no file is open, open the correct file.
                            
                            date_file = open(date_created + ".txt", "a+")
                            file_open = date_created
                            
                        elif file_open != date_created:

                            # If the wrong file is open, close it and
                            # open the correct file.
                            
                            file_open = date_created
                            date_file.close()
                            date_file = open(date_created + ".txt", "a+")

                        date_file.write(json.dumps(tweet_data) + "\n")
                        
            except:
                
                continue
    
date_file.close()
