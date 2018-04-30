from influencers import Influencers
from peacock import Peacock
from credentials import *
from tqdm import tqdm


def main():

    influencer = Influencers()
    peacock = Peacock(influencer, credentials, 2, 1, 0.5)

    # Episode
    peacock.load_all_tweets(2)

    for i in range(10):
        # Step
        peacock.learn_models()
        gen_tweet = peacock.complete_model.generate_tweet(6)
        gen_tweet_tokens = peacock.complete_model.generate_tokens(gen_tweet)
        peacock.calculate_influencer_similarity(gen_tweet_tokens)

        # Output
        peacock.update_influencers_performance()
        peacock.update_influencers_again()
        print(peacock.influencers.infPerformance, peacock.influencers.infGroup)
      

if __name__ == '__main__':
    main()
