

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

    
    def generate_probability_matrix(words = None):
        """ Takes in a list of previous words and returns a dictionary with each
            of the possible following words and their probability of occurrence
        """
        pass


    def generate_inv_probability_matrix(prob_matrix):
        """ Takes in a probability matrix and returns a inverted matrix where
            the probabilities of each word are the key and the words are the
            value
        """
        pass

    
    def generate_tweet(self, count):
        """ Generates tweet based on language model
            length of tweet is determined by the count parameter
        """
        pass


    def calculate_log_likelihood(self, text):
        """ Takes in a string and returns similarity value of the string and the
            language model
        """
        pass
