import re

def processTweet(tweepyStatusObject):
    """ Takes in raw tweet text and returns cleaned text
    """
    # 1. replace the url with single space
    raw = tweepyStatusObject._json['text']
    raw = re.sub('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'," ",raw)
    # 2. emoji
    emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    raw = emoji_pattern.sub(r'',raw)
    # 3. remove the @ # ??
    raw = re.sub("[^a-zA-Z]","",raw)
    return raw 

# Removing the RT
# rm_RT = if this tweet contains RT then remove the whole tweet

def getNonRetweet(tweepyStatusObject):
    raw = tweepyStatusObject._json['text']

    if "RT" in raw:
        return ""
    else:
        return raw 

def getFavoriteCount(tweepyStatusObject):
    return tweepyStatusObject._json['favorite_count']

def getNumFollowers(tweepyStatusObject):
    return tweepyStatusObject._json['user']['followers_count']

def getNumRetweet(tweepyStatusObject):
    return tweepyStatusObject._json['retweet_count']
