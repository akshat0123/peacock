from peacock import Peacock
from influencers import *
from credentials import *

def main():

    peacock = Peacock(influencers, credentials)

    for influencer in peacock.influencers:
        print('Influencer: %s' % (influencer))
        tweets = peacock.get_tweets(influencer, 10)
        for tweet in tweets:
            print('\tTweet: %s' % (tweet.full_text[:20]))

if __name__ == '__main__':
    main()
