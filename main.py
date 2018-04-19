from twitter_processing_utils import process_tweet
from influencers import Influencers
from peacock import Peacock
from credentials import *
from language_model import LanguageModel
import nltk
from stopList import *
from nltk.stem.snowball import EnglishStemmer
from nltk.tokenize import RegexpTokenizer
from tqdm import tqdm
import re



def main():

    influencerMthd = Influencers()

    peacock = Peacock(influencerMthd, credentials)
    peacock.complete_model = LanguageModel()

    for influencer in tqdm(influencerMthd.allInfluencers[:10]):
        tweets = [tweet.full_text for tweet in peacock.get_tweets(influencer, 1)]
        print(tweets)
        tweets = [process_tweet(tweet) for tweet in tweets]
        print(tweets)
        peacock.complete_model.add_document(tweets)

    tweet = peacock.complete_model.generate_tweet(5)
    print(tweet)


if __name__ == '__main__':
    main()
