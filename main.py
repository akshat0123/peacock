from peacock import Peacock
from influencers import Influencers
from credentials import *

import nltk
from stopList import *
from nltk.stem.snowball import EnglishStemmer
from nltk.tokenize import RegexpTokenizer
import re


def word_freq(token, nGram):
    """ calculate word frequency in the list
    """
    if token in nGram:
        nGram[token] += 1
    else:
        nGram[token] = 1
    return nGram
    
    

def main():

    peacock = Peacock(Influencers.influencers, credentials)


    for influencer in peacock.influencers:
        print('Influencer: %s' % (influencer))
        tweets = peacock.get_tweets(influencer, 100)
        bigramFrq = {}
        trigram = []
        for tweet in tweets:
            #print('\tTweet: %s' % (tweet.full_text[:300]))
            #print('\tTweet: %s' % (tweet.full_text))
            
            line = tweet.full_text[:300]
            bigramFrq = {}

            tokenizer = nltk.tokenize.treebank.TreebankWordTokenizer()
            stemmer = EnglishStemmer()
            
            tokens = tokenizer.tokenize(line)
            tknsLower = [tkn.lower() for tkn in tokens]
            tknsPunc = [re.sub(r'[^\w\s]','',tkn) for tkn in tknsLower]
            #tknStm = [stemmer.stem(tkn) for tkn in tknsPunc]
            nTkns = [tkn for tkn in tknsPunc if tkn not in stopList and len(tkn) > 2]
            nTkns = list(nTkns)
        
            for i in range(len(nTkns)-2):
                trigram.append(nTkns[i] + ',' + nTkns[i+1] + ',' + nTkns[i+2])
                
            for i in range(len(trigram)):
                biTkn = trigram[i]
                bigramFrq = word_freq(biTkn,bigramFrq) 

    print(bigramFrq)
    
    prob_dict, total_freq = {}, 0

    for word in bigramFrq:
       prob_dict[word] = bigramFrq[word]
       total_freq += bigramFrq[word]

    prob_dict = { word: prob_dict[word]/total_freq for word in prob_dict }

    print(prob_dict)
if __name__ == '__main__':
    main()
