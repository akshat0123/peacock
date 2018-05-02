from influencers import Influencers
from peacock import Peacock
from copy import deepcopy
from credentials import *
from tqdm import trange
from tqdm import tqdm


RESULTS_PATH = './results/'


def write_output(extension, text) :
    with open(RESULTS_PATH + extension + '.csv', 'a+') as f:
        f.write(text)


def main():

    influencer = Influencers()
    peacock = Peacock(influencer, credentials, 2, 1, 0.8)
    peacock.load_all_tweets(10)

    # Episodes
    for j in trange(1000, desc='Running Episodes'):

        starting_influencers = deepcopy(peacock.influencers.infGroup)
        prev_group = set(deepcopy(peacock.influencers.infGroup))
        converge_count, iteration_count = 0, 0

        # Steps
        for i in range(100000):

            peacock.learn_models()
            gen_tweet = peacock.complete_model.generate_tweet(6)
            gen_tweet_tokens = peacock.complete_model.generate_tokens(gen_tweet)
            peacock.calculate_influencer_similarity(gen_tweet_tokens)

            peacock.update_influencers_performance()
            peacock.update_influencers_again()

            # Step output
            output_text = '%s|%s|%s\n' % (i, peacock.influencers.infGroup, gen_tweet)
            output_file = 'episode_%s' % j
            write_output(output_file, output_text)

            # Check for convergence
            cur_group = set(deepcopy(peacock.influencers.infGroup))
            if cur_group == prev_group: converge_count += 1
            else: converge_count = 0
            if converge_count == 20: break
            prev_group = cur_group

            iteration_count += 1
          
        # Episode output
        episode_output = '%s|%s|%s|%s\n' % (j, starting_influencers, cur_group, iteration_count)
        episode_path = 'episode_data'
        write_output(episode_path, episode_output)

        # Reset influencer performance
        peacock.influencers.reset()


if __name__ == '__main__':
    main()
