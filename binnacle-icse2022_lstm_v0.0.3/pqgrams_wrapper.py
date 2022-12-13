from pqgrams.PQGram import *
from pqgrams.tree import *

class PQ_GramWrapper(object):
    @staticmethod
    def _zhang(me):
        if me["children"]:
            node = Node(me["type"])
            for child in me["children"]:
                node.addkid(PQ_GramWrapper._zhang(child))
            return node
        else:
            return Node(me["type"])
    
    @staticmethod
    def _get_pq_edit_distance(contents_A, contents_B, P, Q):
        tree_A = PQ_GramWrapper._zhang(contents_A); tree_B = PQ_GramWrapper._zhang(contents_B)
        profile_A = Profile(tree_A, P, Q); profile_B = Profile(tree_B, P, Q)
        pq_distance = profile_A.edit_distance(profile_B)
        return pq_distance