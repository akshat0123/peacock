from influencers import Influencers
from peacock import Peacock
from credentials import *
from tqdm import tqdm


def main():

    influencer = Influencers()

    peacock = Peacock(influencer, credentials)
    peacock.learn_models(2)
    # gen_tweet = peacock.complete_model.generate_tweet(6)
    # gen_tweet_tokens = peacock.complete_model.generate_tokens(gen_tweet)

    # influencers = peacock.influencers.infGroup
    # similarities = { influencer: [] for influencer in influencers }
    # for influencer in tqdm(influencers, desc='Calculating Similarities:'):
    #     tweets = [tweet.full_text for tweet in peacock.get_tweets(influencer, 10)]
    #     for tweet in tweets:
    #         tweet_tokens = peacock.complete_model.generate_tokens(tweet)
    #         sim = peacock.complete_model.calculate_similarity(gen_tweet_tokens, tweet_tokens)
    #         similarities[influencer].append((tweet, sim))

    # print('\nPeacock Generated Tweet: %s\n' % (gen_tweet))

    # similarities = { influencer: sorted(similarities[influencer], key=lambda x:x[1], reverse=True) for influencer in similarities }
    # for influencer in similarities:
    #     print('\nInfluencer: %s\n' % (influencer))
    #     for sim in similarities[influencer]:
    #         tweet, val = sim[0], sim[1]
    #         print('Tweet: %s\tValue: %s' % (tweet, val))
        

if __name__ == '__main__':
    main()
