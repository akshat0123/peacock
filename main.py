from peacock import Peacock
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
<<<<<<< HEAD
            print('\tTweet: %s' % (tweet.full_text[:300]))
            print('\tTweet: %s' % (tweet.full_text))
=======
<<<<<<< HEAD
            print('\tTweet: %s' % (tweet))
=======
            #print('\tTweet: %s' % (tweet.full_text[:300]))
            #print('\tTweet: %s' % (tweet.full_text))
>>>>>>> origin/master
            
            

    print(prob_dict)
>>>>>>> 5e662f16ec0b2546270027fd495d0f83c3814f6a
if __name__ == '__main__':
    main()
