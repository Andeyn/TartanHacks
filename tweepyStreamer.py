from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
 
import twitterCredentialsAPI
import numpy as np
import pandas as pd

#prints out junk of data of what type of tweets it is
#returns date, type etc.
### TWITTER AUTHENTIFICATION
class TwitterAuth():
    def __init__(self):
        pass
    def authTwitterApp(self):
        auth = OAuthHandler(twitterCredentialsAPI.CONSUMER_KEY, twitterCredentialsAPI.CONSUMER_SECRET)
        auth.set_access_token(twitterCredentialsAPI.ACCESS_TOKEN, twitterCredentialsAPI.ACCESS_TOKEN_SECRET)
        return auth
        
## Twitter Client(User)
class TwitterClient():
    #clients/user allow you to specify what user you want to look for
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuth().authTwitterApp()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    #allows you to identify which user to extrapalate data from
    def get_twitter_client_api(self):
        return self.twitter_client
    
    #specifies users and number of tweets
    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    #gives you a list of people you can string into your user client funct
    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

### TWITTER STREAMER 
class TwitterStreamer(): #fetches a bunch of data displayed as junk
    def __init__(self):
        self.authenticateTweets = TwitterAuth()

    def streamTweets(self, fetchedTweetFile, hashTagLst):
        #handles Twitter authetification and the connection to Twitter Streaming API
        listener = StdOutListener(fetchedTweetFile)
        auth = self.authenticateTweets.authTwitterApp()
        stream = Stream(auth, listener)
        #calls the hashtaglist u want to parse through and find
        stream.filter(track=hashTagLst)

### TWITTER STREAM LISTENER 
class StdOutListener(StreamListener): #reads the tweets

    def __init__(self, fetchedTweetFile):
        self.fetchedTweetFile = fetchedTweetFile

    def on_data(self, data):#try and except allows you to read files regardless
        try:
            with open(self.fetchedTweetFile, 'a') as f: #'a' opens the file
                f.write(data)
            return True
        except BaseException as e:
            print("Error! %s" % str(e))
        return True
          

    def on_error(self, status):
        print(status)
        pass
        
class hashtagParser():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuth().authTwitterApp()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user
    
    def get_twitter_client_api(self):
        return self.twitter_client
        
    #specifies users and number of tweets
    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline).items(num_tweets):
            tweets.append(tweet)
        return tweets
        
class TweetAnalysis(): #analyzes and categorizes tweets
    def tweetsToDataFrame(self, tweets):
        #panda creates automatically creates a dataframe 
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets']) 
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        return df
def main(): 
    twitterUser = hashtagParser()
    tweetAnalyzer = TweetAnalysis()
    api = hashtagParser().get_twitter_client_api()
    hashTagLst = ["trump"]
    fetchedTweetFile = "tweets.txt"
    username = "KimKardashian"
    twitStreamer = TwitterStreamer()
    # tweets = twitStreamer.streamTweets(fetchedTweetFile, hashTagLst)
    #specifies which user and how many tweets from them
    tweets = api.user_timeline(username, count=10)
    # print(tweets)
    df = tweetAnalyzer.tweetsToDataFrame(tweets)
    print(df)

## used to stream data junk by hashtags in main fucntion
 

main()