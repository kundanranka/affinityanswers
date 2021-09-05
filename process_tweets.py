#install tweet-preprocessor to clean tweets
#pip install tweet-preprocessor

import re
#set up punctuations we want to be replaced
REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\|)|(\()|(\))|(\[)|(\])|(\%)|(\$)|(\>)|(\<)|(\{)|(\})")
REPLACE_WITH_SPACE = re.compile("(<br\s/><br\s/?)|(-)|(/)|(:).")
#file name to be used
SLURS_FILE = "racialSlurs.json" #assuming all slurs are in lowercase and have no punctuation
TWEETS_FILE = "tweets.json" #tweets can contain any hashtags, links or mentions, and can be in upper or lower case

import preprocessor as p
import json

# data cleaning
def preprocess_tweets(df):
  tempArr = []
  for line in df:
    #send to tweet_processor
    tmpL = p.clean(line)
    #remove puctuation
    tmpL = REPLACE_NO_SPACE.sub("", tmpL.lower()) # convert all tweets to lower cases
    tmpL = REPLACE_WITH_SPACE.sub(" ", tmpL)
    tempArr.append(tmpL)
  return tempArr

# calculate the degree of profanity
def profanity_degree(tweet,slurs):
    slur_count = 0
    for slur in slurs:
        if slur in tweet:
            slur_count += tweet.count(slur)
    return slur_count

ractial_slurs = json.load(open(SLURS_FILE))["slurs"]
data = json.load(open(TWEETS_FILE))["tweets"]
tweets = preprocess_tweets(data)
for tweet in tweets:
    if any(slur in tweet for slur in ractial_slurs):
        slur_count = profanity_degree(tweet,ractial_slurs)
        print(tweet+" -> "+str(slur_count))