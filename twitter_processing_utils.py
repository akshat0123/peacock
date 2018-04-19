import re

def process_tweet(raw):
    """ Takes in raw tweet text and returns cleaned text
    """
    # 1. replace the url with single space
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
    # raw = re.sub("[^a-zA-Z]"," ",raw)

    # 3. removing the RT
    # rm_RT = if this tweet contains RT then remove the whole tweet

    if "RT" in raw:
        return ""
    else:
        return raw 

def getFavoriteCount(tweepyObject):
    return tweepyObject.favorite_count


def getNumFollowers(tweepyObject):
    return tweepyObject.follower_count


def getNumFoward(tweepyObject):
    return tweepyObject.forward_count
