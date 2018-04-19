from language_model import LanguageModel
import tweepy
import random

class Peacock:


    def __init__(self, influencers, credentials):
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


    def get_tweets(self, user, count):
        """ Takes in a twitter user and a count and returns the number of tweets
            specified by 'count' from the specified user
        """

        return self.api.user_timeline(screen_name=user, count=count, tweet_mode='extended')


    def publish_tweet(self, tweet):
        """ Takes in tweet as string and publishes it to the agent's twitter
            feed
        """

        self.api.update_status(tweet)


    def rank_influencer_tweets_by_similarity(self, count):
        """ For each influencer get the top 'count' similar tweets
            Returns a dictionary with influencer name as key and top 'count'
            similar tweets as values
        """
        pass


    def assign_popularity_to_tweet(self, tweet):
        """ Takes in a tweet and calculates popularity based on likes/retweets
            of that tweet
        """
        pass


    def least_popular_influencers(self, inf_dict, count):
        """ Takes in dictionary from rank_influencer and returns the least
            'count' popular influencers 
        """
        pass


    def update_influencers(self, count):
        """ Updates influencer list at random with 'count' influencers
        """
        pass
    
