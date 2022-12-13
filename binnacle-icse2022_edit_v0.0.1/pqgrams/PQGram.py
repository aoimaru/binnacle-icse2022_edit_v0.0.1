#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson and Tyler Goeringer
#Email: tim.tadh@gmail.com and tyler.goeringer@gmail.com
#For licensing see the LICENSE file in the top level directory.

"""
    Allows for the computation of the PQ-Gram edit distance of two trees. To calculate the distance,
    a Profile object must first be created for each tree, then the edit_distance function can be called.

    For more information on the PQ-Gram algorithm, please see the README.
"""

import pqgrams.tree, copy
import functools
import collections
import itertools


class Profile(object):
    """
        Represents a PQ-Gram Profile, which is a list of PQ-Grams. Each PQ-Gram is represented by a
        deque. This class relies on the tree.Node classe.
    """

    def __init__(self, root, p=2, q=3):
        """
            Builds the PQ-Gram Profile of the given tree, using the p and q parameters specified.
            The p and q parameters do not need to be specified, however, different values will have
            an effect on the distribution of the calculated edit distance. In general, smaller values
            of p and q are better, though a value of (1, 1) is not recommended, and anything lower is
            invalid.
        """
        super(Profile, self).__init__()
        ancestors = collections.deque('*'*p, maxlen=p)
        self.list = list()

        self.profile(root, p, q, ancestors)
        self.sort()

    def profile(self, root, p, q, ancestors):
        """
            Recursively builds the PQ-Gram profile of the given subtree. This method should not be called
            directly and is called from __init__.
        """
        ancestors.append(root.label)
        siblings = collections.deque('*'*q, maxlen=q)

        if(len(root.children) == 0):
            self.append(itertools.chain(ancestors, siblings))
        else:
            for child in root.children:
                siblings.append(child.label)
                self.append(itertools.chain(ancestors, siblings))
                self.profile(child, p, q, copy.copy(ancestors))
            for i in range(q-1):
                siblings.append("*")
                self.append(itertools.chain(ancestors, siblings))

    def edit_distance(self, other):
        """
            Computes the edit distance between two PQ-Gram Profiles. This value should always
            be between 0.0 and 1.0. This calculation is reliant on the intersection method.
        """
        union = len(self) + len(other)
        return 1.0 - 2.0*(self.intersection(other)/union)

    def intersection(self, other):
        """
            Computes the set intersection of two PQ-Gram Profiles and returns the number of
            elements in the intersection.
        """
        intersect = 0.0
        i = j = 0
        maxi = len(self)
        maxj = len(other)
        while i < maxi and j < maxj:
            intersect += self.gram_edit_distance(self[i], other[j])
            if self[i] == other[j]:
                i += 1
                j += 1
            elif self[i] < other[j]:
                i += 1
            else:
                j += 1
        return intersect

    @functools.lru_cache()
    def gram_edit_distance(self, gram1, gram2):
        """
            Computes the edit distance between two different PQ-Grams. If the two PQ-Grams are the same
            then the distance is 1.0, otherwise the distance is 0.0. Changing this will break the
            metrics of the algorithm.
        """
        distance = 0.0
        if gram1 == gram2:
            distance = 1.0
        return distance

    def sort(self):
        """
            Sorts the PQ-Grams by the concatenation of their labels. This step is automatically performed
            when a PQ-Gram Profile is created to ensure the intersection algorithm functions properly and
            efficiently.
        """
        self.list.sort(key=lambda x: ''.join(x))

    def append(self, value):
        self.list.append(tuple(value))

    @functools.lru_cache(maxsize=2)
    def __len__(self):
        return len(self.list)

    def __repr__(self):
        return str(self.list)

    def __str__(self):
        return str(self.list)

    @functools.lru_cache(maxsize=32)
    def __getitem__(self, key):
        return self.list[key]

    def __iter__(self):
        return iter(self.list)
