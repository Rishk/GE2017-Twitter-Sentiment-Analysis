import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Using the following command on Linux will store the output of
# this script to a .txt file:

# python stream_twitter_data.py > twitter-ge#.txt


# Twitter API OAuth Keys and Tokens:

access_token = "-"
access_token_secret = "-"
consumer_key = "-"
consumer_secret = "-"

class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    while True:
        
        time.sleep(5)
	try:
            stream = Stream(auth, l)
            stream.filter(track=['Theresa May', 'theresa_may', 'theresamay', 'UK Prime Minister', 'Number10gov', 'conservatives', 'Tories', 'Tory', 'Corbyn', 'Jeremy Corbyn', 'jeremycorbyn', 'Opposition Leader', 'UKLabour', 'Labour party', 'Labour government', 'Labour', 'Nuttall', 'Paul Nuttall', 'paulnuttall', 'paulnuttallukip', 'ukip', 'Farron', 'Tim Farron', 'timfarron', 'LibDem', 'LibDems', 'Liberal Democrats', 'Lib Dems', 'Brexit', 'NHS', 'Economy', 'National Debt', 'Immigration', 'Education', 'Healthcare', 'Defence', 'Defense', 'Pension', 'Trident'], languages=['en'])
        except:
            continue

        # This loop ensures that the script does not stop collecting tweets
        # if an error occurs.
        
    # Average tweet size is about 5924 bytes.
