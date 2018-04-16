from peacock import Peacock
from influencers import Influencers
from credentials import *

import nltk
from stopList import *
from nltk.stem.snowball import EnglishStemmer
from nltk.tokenize import RegexpTokenizer
import re


def word_freq(token, nGram):
    """ calculate word frequency in the list
    """
    if token in nGram:
        nGram[token] += 1
    else:
        nGram[token] = 1
    return nGram
    
    

def main():

    peacock = Peacock(Influencers.influencers, credentials)


    for influencer in peacock.influencers:
        print('Influencer: %s' % (influencer))
        tweets = peacock.get_tweets(influencer, 100)
        for tweet in tweets:
            print('\tTweet: %s' % (tweet.full_text[:300]))
            print('\tTweet: %s' % (tweet.full_text))
            
            

    print(prob_dict)
if __name__ == '__main__':
    main()
