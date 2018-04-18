from influencers import Influencers
from peacock import Peacock
from credentials import *
from language_model import LanguageModel
import nltk
from stopList import *
from nltk.stem.snowball import EnglishStemmer
from nltk.tokenize import RegexpTokenizer
import re



def main():

    influencerMthd = Influencers()
    peacock = Peacock(influencerMthd, credentials)
    lngMdl = LanguageModel()
    uni,bi,tri = lngMdl.add_document(["Luck is when opportunity meets preparation, truer words were never spoken @RyanSeacrest #americanidol"])
    print(lngMdl.generate_tweet(5))                                

    for influencer in influencerMthd.allInfluencers:
        print('Influencer: %s' % (influencer))
        
        print(lngMdl.generate_tweet(5))
        for tweet in tweets:
            uni,bi,tri = lngMdl.add_document(tweet)
            print('\tTweet: %s' % (tweet.full_text[:300]))
            print('\tTweet: %s' % (tweet.full_text))
    
        


if __name__ == '__main__':
    main()
