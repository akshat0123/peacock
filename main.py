from influencers import Influencers
from peacock import Peacock
import numpy as np
from credentials import *
from tqdm import tqdm


def main():

    influencer = Influencers()

    peacock = Peacock(influencer, credentials)
    peacock.learn_models(5)
    gen_tweet = peacock.complete_model.generate_tweet(10)
    gen_tweet_tokens = peacock.complete_model.generate_tokens(gen_tweet)

    influencers = peacock.influencers.infGroup
    leastPopInfluencer = peacock.rank_influencer_tweets_by_similarity(influencers, 5, 1, gen_tweet_tokens)
    peacock.update_influencers_performance(influencers)


if __name__ == '__main__':
    main()
