from influencers import Influencers
from peacock import Peacock
from credentials import *
from tqdm import tqdm


def main():

    influencer = Influencers()

    peacock = Peacock(influencer, credentials)
    peacock.learn_models(2)
    print(peacock.complete_model.generate_tweet(6))


if __name__ == '__main__':
    main()
