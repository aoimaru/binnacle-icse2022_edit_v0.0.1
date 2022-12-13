#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson and Tyler Goeringer
#Email: tim.tadh@gmail.com and tyler.goeringer@gmail.com
#For licensing see the LICENSE file in the top level directory.

"""
    This file provides unit testing for the different parts of the PQ-Gram algorithm.
"""

from pqgrams.PQGram import *
from pqgrams.tree import *
import unittest, random, itertools
from pstats import Stats
import cProfile
random.seed(1)

class ProfileCheck(unittest.TestCase):
    """
        This class verifies that PQGram.Profile is executing properly.
    """

    def checkProfileEquality(self, profile1, profile2):
        """
            Ensure that two different PQ-Gram Profile are actually the same. Used in later tests to
            compare dynamically created Profiles against preset Profiles.
        """
        if len(profile1) != len(profile2) or len(profile1[0]) != len(profile2[0]):
            return False
        for gram1 in profile1:
            contains = False
            for gram2 in profile2:
                if gram1 == gram2:
                    contains = True
                    break
            if contains == False:
                return False
        return True

    def setUp(self):
        self.p = 2
        self.q = 3
        num_random = 10
        self.trees = list()
        self.profiles = list()

        # Construct one-node trees
        self.small_tree1 = tree.Node("a")
        self.small_tree2 = tree.Node("b")
        self.trees.append(self.small_tree1)
        self.trees.append(self.small_tree2)

        self.small_profile1 = [('*','a','*','*','*')]
        self.small_profile2 = [('*','b','*','*','*')]

        # Construct a few more known trees
        self.known_tree1 =  (tree.Node("a")
                                .addkid(tree.Node("a")
                                    .addkid(tree.Node("e"))
                                    .addkid(tree.Node("b")))
                                .addkid(tree.Node("b"))
                                .addkid(tree.Node("c")))

        self.known_tree2 =  (tree.Node("a")
                                .addkid(tree.Node("a")
                                    .addkid(tree.Node("e"))
                                    .addkid(tree.Node("b")))
                                .addkid(tree.Node("b"))
                                .addkid(tree.Node("x")))

        self.trees.append(self.known_tree1)
        self.trees.append(self.known_tree2)

        self.known_profile1 = [('*','a','*','*','a'),('a','a','*','*','e'),('a','e','*','*','*'),('a','a','*','e','b'),
                               ('a','b','*','*','*'),('a','a','e','b','*'),('a','a','b','*','*'),('*','a','*','a','b'),
                               ('a','b','*','*','*'),('*','a','a','b','c'),('a','c','*','*','*'),('*','a','b','c','*'),
                               ('*','a','c','*','*')]
        self.known_profile2 = [('*','a','*','*','a'),('a','a','*','*','e'),('a','e','*','*','*'),('a','a','*','e','b'),
                               ('a','b','*','*','*'),('a','a','e','b','*'),('a','a','b','*','*'),('*','a','*','a','b'),
                               ('a','b','*','*','*'),('*','a','a','b','x'),('a','x','*','*','*'),('*','a','b','x','*'),
                               ('*','a','x','*','*')]

        self.known_edit_distance = 0.31

        # Construct a few randomly generated trees
        for i in range(0, num_random):
            depth = random.randint(1, 10)
            width = random.randint(1, 5)
            self.trees.append(randtree(depth=depth, width=width, repeat=4))

        # Generate Profiles
        for tree1 in self.trees:
            self.profiles.append(PQGram.Profile(tree1, self.p, self.q))

        #self.prof = cProfile.Profile()
        if hasattr(self, "prof"):
            self.prof.enable()

    def tearDown(self):
        """finish any test"""
        if hasattr(self, "prof"):
            p = Stats(self.prof)
            p.strip_dirs()
            p.sort_stats('cumtime')
            p.print_stats()
            print("\n--->>>")


    def testProfileCreation(self):
        """Tests the creation of profiles against known profiles."""
        small_tree1_equality = self.checkProfileEquality(self.profiles[0], self.small_profile1)
        small_tree2_equality = self.checkProfileEquality(self.profiles[1], self.small_profile2)
        known_tree1_equality = self.checkProfileEquality(self.profiles[2], self.known_profile1)
        known_tree2_equality = self.checkProfileEquality(self.profiles[3], self.known_profile2)

        self.assertEqual(small_tree1_equality, True)
        self.assertEqual(small_tree2_equality, True)
        self.assertEqual(known_tree1_equality, True)
        self.assertEqual(known_tree2_equality, True)

#    def testSymmetry(self):
#        """x.edit_distance(y) should be the same as y.edit_distance(x)"""
#        for profile1 in self.profiles:
#            for profile2 in self.profiles:
#                self.assertEqual(profile1.edit_distance(profile2), profile2.edit_distance(profile1))

    def testEditDistanceBoundaries(self):
        """x.edit_distance(y) should always return a value between 0 and 1"""
        for profile1 in self.profiles:
            for profile2 in self.profiles:
                self.assertTrue(profile1.edit_distance(profile2) <= 1.0 and profile1.edit_distance(profile2) >= 0)

#    def testTriangleInequality(self):
#        """The triangle inequality should hold true for any three trees"""
#        for profile1 in self.profiles:
#            for profile2 in self.profiles:
#                for profile3 in self.profiles:
#                    self.assertTrue(profile1.edit_distance(profile3) <= profile1.edit_distance(profile2) + profile2.edit_distance(profile3))

    def testIdentity(self):
        """x.edit_distance(x) should always be 0"""
        for profile in self.profiles:
            self.assertEqual(profile.edit_distance(profile), 0)

    def testKnownValues(self):
        """The edit distance of known_tree1 and known_tree2 should be approximately 0.31"""
        edit_distance = self.profiles[2].edit_distance(self.profiles[3])
        self.assertEqual(round(edit_distance, 2), self.known_edit_distance)


# Builds a random tree for testing purposes
def randtree(depth=2, alpha='abcdefghijklmnopqrstuvwxyz', repeat=2, width=2):
    labels = [''.join(x) for x in itertools.product(alpha, repeat=repeat)]
    random.shuffle(labels)
    labels = (x for x in labels)
    root = tree.Node("root")
    p = [root]
    c = list()
    for x in range(depth-1):
        for y in p:
            for z in range(random.randint(1,1+width)):
                n = tree.Node(next(labels))
                y.addkid(n)
                c.append(n)
        p = c
        c = list()
    return root


unittest.main()
