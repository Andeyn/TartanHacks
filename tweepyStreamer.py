from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
 
import twitterCredentialsAPI


#prints out junk of data of what type of tweets it is
#returns date, type etc.
##TWITTER AUTHENTIFICATION

class TwitterAuth():
    def __init__(self):
        pass
    def authTwitterApp(self):
        auth = OAuthHandler(twitterCredentialsAPI.CONSUMER_KEY, twitterCredentialsAPI.CONSUMER_SECRET)
        auth.set_access_token(twitterCredentialsAPI.ACCESS_TOKEN, twitterCredentialsAPI.ACCESS_TOKEN_SECRET)
        return auth

### TWITTER STREAMER 
class TwitterStreamer():
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
class StdOutListener(StreamListener):

    def __init__(self, fetchedTweetFile):
        self.fetchedTweetFile = fetchedTweetFile

    def on_data(self, data):#try and except allows you to read files regardless
        try:
            print(data)
            with open(self.fetchedTweetFile, 'a') as f: #'a' opens the file
                f.write(data)
            return True
        except BaseException as e:
            print("Error! %s" % str(e))
        return True
          

    def on_error(self, status):
        print(status)

 
def main(): 
    hashTagLst = ["kardashian", "jenner"]
    fetchedTweetFile = "tweets.txt"

    twitStreamer = TwitterStreamer()
    twitStreamer.streamTweets(fetchedTweetFile, hashTagLst)
main()