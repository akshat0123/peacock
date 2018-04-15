from random import uniform
import nltk
from stopList import *
from nltk.stem.snowball import EnglishStemmer
from nltk.tokenize import RegexpTokenizer
import re


class LanguageModel:

    def __init__(self):
        """ Initializes language model
        """
        
        self.tokenizer = nltk.tokenize.treebank.TreebankWordTokenizer()
        self.stemmer = EnglishStemmer()
        

        self.trigram_freqs = {}
        self.bigram_freqs = {}
        self.unigram_freqs = {}
        pass

   
    def word_freq(token, nGram):
        """ calculate the tokne frequency
        """
        if token in nGram:
            nGram[token] += 1
        else:
            nGram[token] = 1
            
        return nGram
    
    
    def generate_tokens(self, wordLst):
        """ generate tokens of each tweet
        """
        tokenizer = self.tokenizer
        stemmer = self.stemmer
        tokens = tokenizer.tokenize(wordLst)
        tknsLower = [tkn.lower() for tkn in tokens]
        tknsPunc = [re.sub(r'[^\w\s]','',tkn) for tkn in tknsLower]
        #tknStm = [stemmer.stem(tkn) for tkn in tknsPunc]
        nTkns = [tkn for tkn in tknsPunc if tkn not in stopList and len(tkn) > 2]
        nTkns = list(nTkns)
        
        return nTkns
        
        
    def generate_unigram(self, text):
        """ generate bigram
        """
        unigramFrq = {}
        for tweet in text:
            nTkns = generate_tokens(tweet)
            unigramFrq = word_freq(nTkn,unigramFrq)
        
        return unigramFrq
        

    def generate_bigram(self, text):
        """ generate bigram
        """
        bigramFrq = {}
        bigram = []
        for tweet in text:
            nTkns = generate_tokens(tweet)
            for i in range(len(nTkns)-1):
                bigram.append(nTkns[i] + ',' + nTkns[i+1])
        
        for i in range(len(bigram)):
            biTkn = bigram[i]
            bigramFrq = word_freq(biTkn,bigramFrq)
                 
        return bigramFrq
        
    
    def generate_trigram(self, text):
        """ generate trigram
        """
        trigramFrq = {}
        trigram = []
        for tweet in text:
            nTkns = generate_tokens(tweet)
            for i in range(len(nTkns)-2):
                trigram.append(nTkns[i] + ',' + nTkns[i+1] + ',' + nTkns[i+2])
        
        for i in range(len(trigram)):
            triTkn = trigram[i]
            trigramFrq = word_freq(triTkn,trigramFrq)
            
        return trigramFrq
        

    def add_document(self, text):
        """ Takes in a document as a string and adds it to the model
        """
        self.unigram_freqs = generate_unigram(self,text)        
        self.bigram_freqs = generate_bigram(self,text)
        self.trigram_freqs = generate_trigram(self,text)

    
    def generate_probability_dict(self, freqs):
        """ Takes in a frequency dictionary and returns a dictionary with each
            of the possible words and their probability of occurrence 
        """
        prob_dict, total_freq = {}, 0

        for word in freqs:
           prob_dict[word] = freqs[word]
           total_freq += freqs[word]

        prob_dict = { word: prob_dict[word]/total_freq for word in prob_dict }

        return prob_dict


    def generate_inv_probability_dict(prob_dict):
        """ Takes in a dictionary of terms and their corresponding probabilities and
            returns a dictionary with keys in the interval between 0 and the total
            probability with corresponding terms as values, as well as the total
            probability amount for the term probability dictionary 
        """
        inv_probs, total_prob = {}, 0

        for word in prob_dict:
            total_prob += prob_dict[word]
            inv_probs[prob_sum] = word

        return inv_probs, total_prob


    def produce_word_from_inv_prob_dict(inv_probs, total_prob):
        """ Takes in a dictionary with probability ranges mapped to
            corresponding terms and the total probability in the dictionary and
            returns a token based on its probability of being generated
        """
        random_key_init = uniform(0, total_prob)
        random_key = min(inv_probs.items(), key=lambda x: abs(random_key_init - x[0]))[0]
        token = inv_probs[random_key]

        return token 


    def generate_word(self, freqs):
        """ Takes in a frequency dictionary and returns a word depending on its
            probability of being generated using the given frequency dictionary
        """
        prob_dict = self.generate_probability_dict(freqs)
        inv_probs, total_prob = self.generate_inv_probability_dict(prob_dict)
        word = produce_word_from_inv_prob_dict(inv_probs, total_prob)

        return word


    def generate_tweet(self, count):
        """ Generates tweet based on language model
            length of tweet is determined by the count parameter
        """
        tweet = []

        # First word #
        tweet += generate_word(self.unigram_freqs)

        # Second word #
        # If first word has corresponding bigrams generate word using bigram probability
        if tweet[0] in self.bigram_freqs:
            tweet += generate_word(self.bigram_freqs[tweet[0]])

        # Else use unigram probability
        else:
            tweet += generate_word(self.unigram_freqs)

        # Remaining words #
        for i in range(2, count):

            # If tweets t_i-2 and t_i-2 have corresponding trigrams generate
            # word using trigram probability
            if tweet[i-2] in self.trigram_freqs and tweet[i-1] in self.trigram_freqs[tweet[i-2]]:
                tweet += generate_word(self.trigram_freqs[tweet[i-2]][tweet[i-1]])

            # Else if tweet t_i-1 has corresponding bigrams generate word using
            # bigram probability
            elif tweet[i-1] in self.bigram_freqs:
                tweet += generate_word(self.bigram_freqs[tweet[i-1]])

            # Else use unigram probability
            else:
                tweet += genereate_word(self.unigram_freqs)

        return ' '.join(tweet)


    def calculate_log_likelihood(self, text):
        """ Takes in a string and returns similarity value of the string and the
            language model
        """
        pass
