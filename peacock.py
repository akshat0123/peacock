from language_model import LanguageModel
from twitter_processing_utils import *
from tqdm import tqdm
import tweepy, random, operator
import numpy as np

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
        self.userTweetsStat = {}
        self.similarities = {}



    def learn_models(self, count):
        """ Takes in a count of tweets to learn from for each influencer and
            fills the complete language model and the influencer language models
            with the corresponding tweets
        """

        influencers = self.influencers.infGroup

        self.complete_model = LanguageModel()
        self.influencer_models = { influencer: LanguageModel() for influencer in influencers }

        all_tweets = []
        for influencer in tqdm(influencers, desc='Learning Models'):
            tweets = [tweet for tweet in self.get_tweets(influencer, count)[0]]
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

    def calculate_influencer_similarity(self,influencers, gnTweetTkn):
        """ calculate the similarity of each tweets of influencer with generated tweet
        """
        similarities = { influencer: [] for influencer in influencers}
        for influencer in tqdm(influencers, desc='Calculating Similarities:'):
            tweets = [tweet for tweet in self.get_tweets(influencer, 10)[0]]
            for tweet in tweets:
                tweet_tokens = self.complete_model.generate_tokens(tweet)
                sim = self.complete_model.calculate_similarity(gnTweetTkn, tweet_tokens)
                similarities[influencer].append((tweet, sim))

        
        similarities = { influencer: sorted(similarities[influencer], key=lambda x:x[1], reverse=True) for influencer in similarities }
        
        self.similarities = similarities

        
    def rank_influencer_tweets_by_similarity(self, influencers, count, infCnt, gen_tweet_tokens):
        """ For each influencer get the top 'count' similar tweets
            Returns a dictionary with influencer name as key and top 'count'
            similar tweets as values
        """
        self.calculate_influencer_similarity(influencers, gen_tweet_tokens)
        similarities = self.similarities
        influencerTopSim = {inf: [] for inf in influencers}
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
        

    def assign_popularity_to_tweet(self, tweetStat, tweet):
        """ Takes in a tweet and calculates popularity based on likes/retweets
            of that tweet
        """
#        likes = []
#        RTs = []
#        for influencer in similarities:
#            likes.append(self.get_tweets(influencer, 10)[1][similarities[influencer][0][0]]['like'])
#            RTs.append(self.get_tweets(influencer, 10)[1][similarities[influencer][0][0]]['RT'])
#        
#        lngMdl = self.complete_model
#        lngMdl.assign_like_RT_to_generatedTweet(likes,RTs)
        
        twNoLike = tweetStat[tweet]['like']
        twNoRt = tweetStat[tweet]['RT']
        twNoFlwr = tweetStat[tweet]['follower']
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

    def update_influencers_performance(self, influencers):
        """ Updates influencer performance
        """
        simParam = 2
        popParam = 1
        for influencer in influencers:
            similarity = []
            popularity = []
            infTweetPop = self.userTweetsStat[influencer]
            infTweet = infTweetPop[len(infTweetPop)-1]
            for value in self.similarities[influencer]:
                similarity.append(value[1])  
                popularity.append(self.assign_popularity_to_tweet(infTweet,value[0]))
                
            self.influencers.infPerformance[influencer] = (simParam*np.mean(similarity) + popParam*np.mean(popularity))
        print("\n===============================================================\n")
        print("The performance of influencer is updated based on the generated tweet\n")
        print(self.influencers.infPerformance)
        
    
    def update_influencers(self, influencers, noInfluencer, epsilon):
        self.influencers.allInfluencers
        infPerformance = self.influencers.infPerformance
        tmp = {key: rank for rank, key in enumerate(sorted(set(infPerformance.values()), reverse=True), 1)}
        rankInfluencer = {k: tmp[v] for k,v in infPerformance.items()}
        
        noInf = len(rankInfluencer)
        slcInfluencer = []
        if random.random() < epsilon:
            slcInfluencer = random.sample(range(1, noInf-1),noInfluencer)
            
        else: 
            slcInfluencer = [a for a in dict(sorted(rankInfluencer.items(), key=operator.itemgetter(1))[:noInfluencer]).keys()]
        
        print('test')
               
           