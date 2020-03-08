# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the tweepy library
import tweepy

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '1215724218412871681-ABM3iZN8E5LRzqCDOPJU3M0wOPoSWK'
ACCESS_SECRET = 'QW6j7hnIV2VUN3P9cmaBcEsDh31ZCLwAKIi41X8z2SLxB'
CONSUMER_KEY = 'RVMLQCP9QnvdYR8GsTzpNglji'
CONSUMER_SECRET = 'jGqGTdTQePhjVkNnDPmI24cfuYycdBQitdeUWmwt64amwiyfJ1'

# Setup tweepy to authenticate with Twitter credentials:

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

#---------------------------------------------------------------------------------------------------------------------
# The following loop will print most recent statuses, including retweets, posted by the authenticating user and that user’s friends. 
# This is the equivalent of /timeline/home on the Web.
#---------------------------------------------------------------------------------------------------------------------
'''
for status in tweepy.Cursor(api.home_timeline).items(200):
    #print(json.dumps(status._json))
    print(json.dumps(status._json))
    time.sleep(0.5)
'''
class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(json.dumps(status._json))
    
    def on_error(self, status_code):
        if status_code == 420:
            return False

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
#filter by bounding boxes of the USA
stream.filter(locations=[-123.52,32.41,-103.74,48.76,-103.74,29.78,-88.27,48,-88.27,25.02,-70,42.4])


#no filter for the world tweets
#stream.sample()

