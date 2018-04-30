from influencers import Influencers
from peacock import Peacock
from credentials import *
from tqdm import tqdm


def main():

    influencer = Influencers()
    peacock = Peacock(influencer, credentials)

    # Episode
    peacock.load_all_tweets(2)

    # Step
    peacock.learn_models()
    gen_tweet = peacock.complete_model.generate_tweet(6)
    gen_tweet_tokens = peacock.complete_model.generate_tokens(gen_tweet)
    similarities = peacock.calculate_influencer_similarity(gen_tweet_tokens)

    # Output
    print('\nPeacock Generated Tweet: %s\n' % (gen_tweet))

    for influencer in similarities:
        print('\nInfluencer: %s\n' % (influencer))
        for sim in similarities[influencer]:
            tweet, val = sim[0], sim[1]
            print('Tweet: %s\tValue: %s' % (tweet, val))
      

if __name__ == '__main__':
    main()
