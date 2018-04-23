import numpy as np

class FeatureSpace:


    def __init__(self, language_model):
        """ Takes in a language model object and initializes the feature space
        """
        features = list(language_model.unigram_freqs.keys())
        self.features = {}
        for i in range(len(features)):
            self.features[features[i]] = i


    def tf_vector(self, document):
        """ Takes in a document as a list of tokens and returns the document
            vector representation in the feature space considering term frequency
        """
        vector = np.zeros(len(self.features))
        for token in document:
            if token in self.features:
                vector[self.features[token]] += 1

        return vector


    def cosine_similarity(self, a, b):
        """ Takes in two vectors a and b and returns the cosine similarity value
            between the two vectors
        """
        num = np.dot(a, b)
        den = np.sqrt(np.dot(a, a)) * np.sqrt(np.dot(b, b))

        sim = 0
        if den != 0:
            sim += (num/den)

        return sim
