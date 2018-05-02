from language_model import LanguageModel
from twitter_processing_utils import *
import tweepy, random, operator
from operator import itemgetter 
from tqdm import tqdm
import numpy as np


class Peacock:


    def __init__(self, influencers, credentials, similarity_parameter, popularity_parameter, epsilon):
        """ Initializes peacock agent, takes in initial list of influencers and
            twitter credentials dictionary
        """
       
        # Twitter API credentials initialization
        auth = tweepy.OAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])
        auth.set_access_token(credentials['access_token'], credentials['access_token_secret'])
        self.api = tweepy.API(auth)

        # Class fields
        self.username = credentials['username']
        self.influencers = influencers
        self.complete_model = None
        self.influencer_models = None
        self.userTweetsStat = {}
        self.similarities = {}
        self.similarity_parameter = similarity_parameter
        self.popularity_parameter = popularity_parameter
        self.epsilon = epsilon
        self.valueState = {influencer: 0 for influencer in self.influencers.allInfluencers}
        self.reward = 1
        self.rewardParam = 0.1
        self.alpha = 0.1
        self.gamma = 1
        self.curDif = 0


    def load_all_tweets(self, count):
        """ Loads and saves 'count' tweets for all possible influencers
        """

        for influencer in tqdm(self.influencers.allInfluencers, desc='Gathering Tweets'):
            self.get_tweets(influencer, count)

    
    def get_saved_tweets(self, user):
        """ Returns user tweets saved in the 'userTweetsStat' dictionary for the
            given user
        """
        return [list(item.keys()) for item in self.userTweetsStat[user]][0]


    def learn_models(self):
        """ Takes in a count of tweets to learn from for each influencer and
            fills the complete language model and the influencer language models
            with the corresponding tweets
        """

        influencers = self.influencers.infGroup

        self.complete_model = LanguageModel()
        self.influencer_models = { influencer: LanguageModel() for influencer in influencers }

        all_tweets = []
        # for influencer in tqdm(influencers, desc='Learning Models'):
        for influencer in influencers:
            tweets = [tweet for tweet in self.get_saved_tweets(influencer)]
            self.influencer_models[influencer].add_documents(tweets)
            all_tweets += tweets

        self.complete_model.add_documents(all_tweets)


    def get_tweets(self, user, count):
        """ Takes in a twitter user and a count and returns the number of tweets
            specified by 'count' from the specified user
        """
        topTweetsList = self.api.user_timeline(screen_name=user, count=count, tweet_mode='extended')
        clnTweets = {}
        for tweet in topTweetsList:
           clnTweets[processTweet(getNonRetweet(tweet))] = ({'like':getFavoriteCount(tweet),'RT':getNumRetweet(tweet),'follower':getNumFollowers(tweet)}) 

        tweetTxt = [twt for twt in clnTweets.keys()]
        
        if user in self.userTweetsStat:
            self.userTweetsStat[user].append(clnTweets)
        else:
            tmp = []
            tmp.append(clnTweets)
            self.userTweetsStat[user] = tmp
        return tweetTxt, self.userTweetsStat


    def publish_tweet(self, tweet):
        """ Takes in tweet as string and publishes it to the agent's twitter
            feed
        """

        self.api.update_status(tweet)


    def calculate_influencer_similarity(self, gnTweetTkn):
        """ calculate the similarity of each tweets of influencer with generated tweet
        """
        influencers = self.influencers.infGroup
        similarities = { influencer: [] for influencer in influencers}
        for influencer in influencers:
            tweets = [tweet for tweet in self.get_saved_tweets(influencer)]
            for tweet in tweets:
                tweet_tokens = self.complete_model.generate_tokens(tweet)
                sim = self.complete_model.calculate_similarity(gnTweetTkn, tweet_tokens)
                similarities[influencer].append((tweet, sim))

        
        similarities = { influencer: sorted(similarities[influencer], key=lambda x:x[1], reverse=True) for influencer in similarities }
        self.similarities = similarities

        
    def rank_influencer_tweets_by_similarity(self, count, infCnt, gen_tweet_tokens):
        """ For each influencer get the top 'count' similar tweets
            Returns a dictionary with influencer name as key and top 'count'
            similar tweets as values
        """
        self.calculate_influencer_similarity(gen_tweet_tokens)
        similarities = self.similarities
        influencerTopSim = { inf: [] for inf in self.influencers.allInfluencers }
        for influencer in similarities:
            twTopSmlrty = []
            cnt = 0
            for value in similarities[influencer]:
                twTopSmlrty.append((value[0]))
                cnt += 1
                if cnt == count:
                    break
            influencerTopSim[influencer] = twTopSmlrty
        
        leastPopInfluencer = self.least_popular_influencers(influencerTopSim,infCnt)
        
        return leastPopInfluencer
        

    def assign_popularity_to_tweet(self, influencer, tweet):
        """ Takes in a tweet and calculates popularity based on likes/retweets
            of that tweet
        """
        twNoLike = self.userTweetsStat[influencer][0][tweet]['like']
        twNoRt = self.userTweetsStat[influencer][0][tweet]['RT']
        twNoFlwr = self.userTweetsStat[influencer][0][tweet]['follower']
        twPopularity = (twNoLike + 2*twNoRt)/twNoFlwr
        
        return twPopularity


    def least_popular_influencers(self, influencerTopSim, count):
        """ Takes in dictionary from rank_influencer and returns the least
            'count' popular influencers 
        """
        infPopularity = {influencer: 0 for influencer in influencerTopSim}
        for influencer in influencerTopSim:
            infTweetPop = self.userTweetsStat[influencer]
            avgPop = []
            for tweet in influencerTopSim[influencer]:
                infTweet = infTweetPop[len(infTweetPop)-1]
                avgPop.append(self.assign_popularity_to_tweet(infTweet,tweet))
            infPopularity[influencer] = np.mean(avgPop)
                
        tmp = {key: rank for rank, key in enumerate(sorted(set(infPopularity.values()), reverse=True), 1)}
        rankInfluencer = {k: tmp[v] for k,v in infPopularity.items()}
        leastPopInfluencer = [a for a in dict(sorted(rankInfluencer.items(), key=operator.itemgetter(1), reverse=True)[:count]).keys()]
        
        return leastPopInfluencer


    def update_influencers_performance(self):
        """ Updates influencer performance
        """
        
        currentScore = np.sum([a for a in self.influencers.infPerformance.values()])
        # the value of current states
        for influencer in self.influencers.infGroup:
            self.valueState[influencer] = self.influencers.infPerformance[influencer]
        
        for influencer in self.influencers.infGroup:
            popularities = [self.assign_popularity_to_tweet(influencer, pair[0]) for pair in self.similarities[influencer]]
            similarities = [pair[1] for pair in self.similarities[influencer]]
            self.influencers.infPerformance[influencer] += (self.similarity_parameter*np.mean(similarities) + self.popularity_parameter*np.mean(popularities))
        
        newScore = np.sum([a for a in self.influencers.infPerformance.values()])
        difScore = newScore - currentScore
        
        # if difScore > self.rewardParam:
        #     self.reward = 1
        # else:
        #     self.reward = -1

        if difScore > self.curDif:
            self.reward = 0
        else:
            self.reward = -1

        self.curDif = difScore
        
        # v(s) += alpha * (R + gamma*v(s') - v(s))
        for influencer in self.influencers.infGroup:
            self.valueState[influencer] += self.alpha * (self.reward + self.gamma*self.influencers.infPerformance[influencer] - self.valueState[influencer]) 
        
    
    def update_influencers(self):
        sorted_influencers = [(influencer, self.influencers.infPerformance[influencer]) for influencer in self.influencers.infGroup]
        sorted_influencers = sorted(sorted_influencers, key=lambda x: x[1], reverse=True)
        worst_influencer = sorted_influencers[len(sorted_influencers)-1][0]

        sorted_influencer_pool = [(influencer, self.influencers.infPerformance[influencer]) for influencer in self.influencers.infPerformance]
        sorted_influencer_pool = sorted(sorted_influencer_pool, key=lambda x:x[1], reverse=True)
        best_possible_influencer = sorted_influencer_pool[0][0]
        best_index = 0

        # Remove worst influencer
        worst_index = self.influencers.infGroup.index(worst_influencer)
        self.influencers.infGroup.pop(worst_index)

        if random.random() < self.epsilon:
            new_influencer = self.influencers.allInfluencers[random.sample(range(0, len(self.influencers.allInfluencers)-1), 1)[0]]
            if new_influencer in self.influencers.infGroup:
                while new_influencer in self.influencers.infGroup:
                    new_influencer = self.influencers.allInfluencers[random.sample(range(0, len(self.influencers.allInfluencers)-1), 1)[0]]

        else:
            new_influencer = best_possible_influencer
            if new_influencer in self.influencers.infGroup:
                while new_influencer in self.influencers.infGroup:

                    sorted_influencer_pool = [(influencer, self.influencers.infPerformance[influencer]) for influencer in self.influencers.infPerformance]
                    sorted_influencer_pool = sorted(sorted_influencer_pool, key=lambda x:x[1], reverse=True)
                    best_possible_influencer = sorted_influencer_pool[best_index][0]
                    new_influencer = best_possible_influencer
                    best_index += 1


        self.influencers.infGroup.append(new_influencer)


    def update_influencers_again(self):

        # Replace influencer at random
        if random.random() > self.epsilon:

            # Remove influencer at random
            random_influencer = self.influencers.infGroup[random.sample(range(0, len(self.influencers.infGroup)-1), 1)[0]]
            random_index = self.influencers.infGroup.index(random_influencer)
            self.influencers.infGroup.pop(random_index)

            # Replace influencer at random
            new_influencer = self.influencers.allInfluencers[random.sample(range(0, len(self.influencers.allInfluencers)-1), 1)[0]]
            if new_influencer in self.influencers.infGroup:
                while new_influencer in self.influencers.infGroup:
                    new_influencer = self.influencers.allInfluencers[random.sample(range(0, len(self.influencers.allInfluencers)-1), 1)[0]]

        # Replace worst influencer with best possible influencer
        else:
            # Remove worst influencer
            sorted_influencers = [(influencer, self.influencers.infPerformance[influencer]) for influencer in self.influencers.infGroup]
            sorted_influencers = sorted(sorted_influencers, key=lambda x: x[1], reverse=True)
            worst_influencer = sorted_influencers[len(sorted_influencers)-1][0]
            worst_index = self.influencers.infGroup.index(worst_influencer)
            self.influencers.infGroup.pop(worst_index)

            # Find best possible influencer
            sorted_influencer_pool = [(influencer, self.influencers.infPerformance[influencer]) for influencer in self.influencers.infPerformance]
            sorted_influencer_pool = sorted(sorted_influencer_pool, key=lambda x:x[1], reverse=True)
            best_possible_influencer = sorted_influencer_pool[0][0]
            best_index = 0

            new_influencer = best_possible_influencer
            if new_influencer in self.influencers.infGroup:
                while new_influencer in self.influencers.infGroup:

                    sorted_influencer_pool = [(influencer, self.influencers.infPerformance[influencer]) for influencer in self.influencers.infPerformance]
                    sorted_influencer_pool = sorted(sorted_influencer_pool, key=lambda x:x[1], reverse=True)
                    best_possible_influencer = sorted_influencer_pool[best_index][0]
                    new_influencer = best_possible_influencer
                    best_index += 1


        self.influencers.infGroup.append(new_influencer)
