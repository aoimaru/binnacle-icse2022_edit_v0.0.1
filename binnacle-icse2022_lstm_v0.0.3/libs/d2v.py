from abc import *

from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

import numpy as np

class D2V(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def _create_document():
        pass
    
    @staticmethod
    @abstractmethod
    def _create_model():
        pass
    
    @staticmethod
    @abstractmethod
    def _load_model():
        pass
    
    @staticmethod
    def _cos_sim(vector_A, vector_B):
        return np.dot(vector_A, vector_B)/(np.linalg.norm(vector_A)*np.linalg.norm(vector_B))

class D2V_ROOT(D2V):
    @staticmethod
    def _create_document(tags, sequence):
        return TaggedDocument(words = sequence, tags=[tags])
    
    @staticmethod
    def _create_model(documents, model_path):
        model = Doc2Vec(documents=documents, dm = 1, vector_size=100, window=5, min_count=10, workers=4)
        model.save(model_path)

    @staticmethod
    def _load_model(model_path):
        return Doc2Vec.load(model_path)