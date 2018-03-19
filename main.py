from peacock import Peacock
from influencers import *
from credentials import *

def main():

    peacock = Peacock(influencers, credentials)

    tweets = peacock.test('akshat0123', 1)
    for tweet in tweets: print(tweet)

if __name__ == '__main__':
    main()
