from twitter import Twitter, OAuth                                                                                                                                                                                                         
import random
import os, ssl

#catches verification errors
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context
    
def butt(hashtags):
    ACCESS_TOKEN = "1094105071346954240-cq8p86mVwoNW5D4hVgCpgetlNXhhEq"
    ACCESS_SECRET = "yF8wWyLqEX16RvmHqWxQnh1jBN619lRKlrn6LK42FxZM9"
    CONSUMER_KEY = "PW3luCZ75v2Pi7d11w7z9yIbm"
    CONSUMER_SECRET = "tueL9DcKQUZjAhntoXZDQXhcmqnR2KyrTchLttprZIolVIt8ZP"
    
    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    t = Twitter(auth=oauth)

    query = t.search.tweets(q='%23' + hashtags)
    detects = []
    for s in query['statuses']:
        print(s['text'], '\n')
        detects.append(s['text'])
    
    randCapt = random.choice(detects)
    randCapt = "#" + randCapt
    return randCapt
butt('lmfao')
print(butt('lmfao'))