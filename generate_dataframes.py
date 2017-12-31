from datetime import timedelta, date
import json
import numpy as np
import pandas as pd

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2017, 5, 3)
end_date = date(2017, 6, 17)

# Days after Manchester bombing and London attacks.
excluded_dates = ["23-05-2017", "24-05-2017", "04-06-2017"]

topics = ["healthcare", "economy", "immigration", "education", "defence", "brexit"]

def generate_data(followers=-1, weekly=False, topic="All", parties=["tory", "labour"]):

    final_data = []

    # As the data is so large and there is insufficient memory, the program
    # loops through the files containing the data and processes them
    # one by one.

    # The files are of the form 'dd-mm-yyyy.txt', and are thus separated by day.

    for single_date in daterange(start_date, end_date):
        
        tweets_data = []

        date_string = single_date.strftime("%d-%m-%Y")
        
        if date_string not in excluded_dates:
            
            tweets_data_path = date_string + '.txt'
            
            tweets_file = open(tweets_data_path, "r")
            for line in tweets_file:
                try:
                    tweet = json.loads(line)
                    tweet.insert(0, date_string)
                    tweets_data.append(tweet)
                except:
                    continue
            
            tweets = pd.DataFrame(tweets_data)
            tweets.columns = ["date", "tweet_id", "sentiment", "tory", "labour", "libdems", "ukip", "healthcare", "economy", "immigration", "education", "defence", "brexit", "pension", "followers", "verified", "time", "country"]

            tweets = tweets[tweets.followers > followers]

            if topic.lower() in topics:

                tweets = tweets[tweets[topic.lower()] == 1]

            # Bring all the data together and append it to the main list.

            to_append = []

            to_append.append(date_string)

            for party in parties:

                # Add the volume of positive and negative tweets for each party.
                
                to_append.append(len(tweets[(tweets[party] == 1) & (tweets.sentiment == 1)].index))
                to_append.append(len(tweets[(tweets[party] == 1) & (tweets.sentiment == -1)].index))

            final_data.append(to_append)

    dataframe_column_headings = ["date"]

    for party in parties:

        dataframe_column_headings.append(party + "_positive")
        dataframe_column_headings.append(party + "_negative")

    output = pd.DataFrame(final_data)
    output.columns = dataframe_column_headings

    if weekly is True:

        # Group the data into weekly data.

        output_dates = pd.DataFrame(output.groupby(by=lambda x: x/7, axis=0)['date'].apply(list))
        output_volumes = output.groupby(by=lambda x: x/7, axis=0).sum()

        output = output_dates.join(output_volumes, how='outer')

    else:

        # Give the data day by day.

        output.set_index('date', inplace=True)

    return output
