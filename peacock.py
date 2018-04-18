import tweepy
import random

class Peacock:

    class Influencers:
    """
    Create class influencers
    Set baseline list of influencers
    """

        def __init__(self):
            self.allInfluencers = ["katyperry","justinbieber","BarackObama","rihanna","taylorswift13","ladygaga","TheEllenShow","Cristiano","YouTube","jtimberlake","Twitter","KimKardashian","britneyspears","ArianaGrande","selenagomez","ddlovato","cnnbrk","shakira","jimmyfallon","realDonaldTrump","BillGates","JLo","Oprah","BrunoMars","narendramodi","nytimes","KingJames","MileyCyrus","CNN","NiallOfficial","instagram","neymarjr","BBCBreaking","Drake","SportsCenter","KevinHart4real","iamsrk","espn","LilTunechi","SrBachchan","wizkhalifa","Louis_Tomlinson","Pink","LiamPayne","BeingSalmanKhan","Harry_Styles","onedirection","aliciakeys","KAKA","realmadrid","NASA","Adele","EmmaWatson","ConanOBrien","FCBarcelona","chrisbrown","ActuallyNPH","NBA","danieltosh","pitbull","zaynmalik","KendallJenner","khloekardashian","akshaykumar","PMOIndia","sachin_rt","KylieJenner","coldplay","NFL","imVkohli","kourtneykardash","deepikapadukone","TheEconomist","aamir_khan","iHrithik","BBCWorld","POTUS","Eminem","andresiniesta8","NatGeo","MesutOzil1088","HillaryClinton","priyankachopra","AvrilLavigne","davidguetta","MohamadAlarefe","NICKIMINAJ","blakeshelton","MariahCarey","elonmusk","ChampionsLeague","ricky_martin","Google","edsheeran","arrahman","Reuters","AlejandroSanz","LeoDiCaprio","aplusk","Dr_alqarn"]
            self.infGroup = random.sample(self.allInfluencers, 10)
            self.discard = self.infGroup
            self.infAvail = list(filter(lambda x: x not in self.infGroup, self.allInfluencers))
            

        def replaceOne(self, discardItem):
            """
            Replace one item in infGroup, append to discard
            Select a new item, append to infGroup and remove from infAvail
            """
            self.infGroup.remove(discardItem)
            self.discard.append(discardItem)
            newItem = random.sample(self.infAvail, 1)[0]
            self.infGroup.append(newItem)
            self.infAvail.remove(newItem)

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
        self.influencers = Influencers()
        self.complete_model = None
        self.influencer_models = None


    def get_tweets(self, user, count):
        """ Takes in a twitter user and a count and returns the number of tweets
            specified by 'count' from the specified user
        """

        return self.api.user_timeline(screen_name=user, count=count, tweet_mode='extended')


    def generate_corpus(self, count):
        """ Generates language model for all influencers as well as language
            model for each individual influencer

            The number of tweets to take from each influencer is determined by
            the count parameter
        """

        self.complete_model = LanguageModel()
        self.influencer_models = {}
       
        for influencer in self.influencers:
            tweets = self.get_tweets(influencer, count)
            self.influencer_models = LanguageModel()

            for tweet in tweets:
                self.complete_model.add_document(tweet)
                self.influencer_models.add_document(tweet)

        pass


    def generate_tweet(self, size):
        """ Generates tweet using complete influencer corpus

            The size of the tweet to be generated is determined by the 'size' parameter
        """
        pass


    def publish_tweet(self, tweet):
        """ Takes in tweet as string and publishes it to the agent's twitter
            feed
        """

        self.api.update_status(tweet)


    def calculate_reward(self):
        """ Calculates reward for the current tweet based upon the amount of
            favorites/retweets recieved on current tweet compared to previous tweet
        """
        pass

    
    def rank_influencers(self):
        """ Calculates similarity of current tweet to each influencer model and
            returns dictionary of each influencer and their rank
        """
        pass


    def update_influencers(self):
        """ Updates influencers based upon their rank
        """
        pass

    
    def run_episode(self, size):
        """ Runs a single reinforcement learning episode

            The size of the tweet to be generated is determined by the 'size'
            parameter
        """
    
        # Generate all language models
        self.generate_corpus()

        # Generate and publish tweet
        tweet = self.generate_tweet(size)
        self.publish_tweet(tweet)

        # Calculate reward of current tweet, rank influencer effectiveness, and
        # update influencers based upon their ranking
        self.calculate_reward()
        self.rank_influencers()
        self.update_influencers()

        pass


    def test(self, user, count):
        """ TEST METHOD: prints latest 'count' tweets from specified user 
        """
        tweets = []
        tweets += [status.text for status in self.get_tweets(user, count)]

        return tweets
