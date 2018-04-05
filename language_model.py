from random import uniform


class LanguageModel:

    def __init__(self):
        """ Initializes language model
        """
        self.trigram_freqs = {}
        self.bigram_freqs = {}
        self.unigram_freqs = {}

   
    def add_document(self, text):
        """ Takes in a document as a string and adds it to the model
        """
        pass

    
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


    def generate_word(inv_probs, total_prob):
        """ Takes in a dictionary with probability ranges mapped to
            corresponding terms and the total probability in the dictionary and
            returns a token based on its probability of being generated
        """
        random_key_init = uniform(0, total_prob)
        random_key = min(inv_probs.items(), key=lambda x: abs(random_key_init - x[0]))[0]
        token = inv_probs[random_key]
        return token 


    def generate_tweet(self, count):
        """ Generates tweet based on language model
            length of tweet is determined by the count parameter
        """
        tweet = []

        # First word
        prob_dict = self.generate_probability_dict(self.unigram_freqs)
        inv_probs, total_prob = self.generate_inv_probability_dict(prob_dict)
        tweet += generate_word(inv_probs, total_prob)

        # Second word
        prob_dict = self.generate_probability_dict(self.bigram_freqs[tweet[0]])
        inv_probs, total_prob = self.generate_inv_probability_dict(prob_dict)
        tweet += generate_word(inv_probs, total_prob)

        # Remaining words
        for i in range(2, count):
            prob_dict = self.generate_probability_dict(self.trigram_freqs[tweet[i-2]][tweet[i-1]])
            inv_probs, total_prob = self.generate_inv_probability_dict(prob_dict)
            tweet += generate_word(inv_probs, total_prob)

        return ' '.join(tweet)


    def calculate_log_likelihood(self, text):
        """ Takes in a string and returns similarity value of the string and the
            language model
        """
        pass
