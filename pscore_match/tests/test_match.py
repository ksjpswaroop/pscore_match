from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from nose.plugins.attrib import attr
from nose.tools import assert_raises, raises
import numpy as np
import pandas as pd

from ..match import Match
from ..data import gerber_green_imai

@raises(AssertionError)
def test_match_errors():
    match=Match(groups=[1,2,1,2], propensity=[0.1, 0.2, 0.15, 0.22, 0.11])
    
@raises(AssertionError)
def test_match_errors():
    match=Match(groups=[1,2,1,3], propensity=[0.1, 0.2, 0.15, 0.22])
    
@raises(AssertionError)
def test_match_errors():
    match=Match(groups=[1,2,1,2], propensity=[-0.1, 0.2, 0.15, 0.11])
    
@raises(ValueError)
def test_match_errors():
    match=Match(groups=[1,2,1,2], propensity=[0.1, 0.2, 0.15, 0.11])
    match.create(method='something made up') 

@raises(AssertionError)
def test_match_errors():
    match=Match(groups=[1,2,1,2], propensity=[-0.1, 0.2, 0.15, 0.11])
    match.create(method='many-to-one', caliper_method=None, many_method='caliper')

def test_match_onetoone():
    np.random.seed(23456)
    match=Match(groups=[1,2,1,2], propensity=[0.1, 0.2, 0.15, 0.11])
    match.create()
    expected_matches = {'match_pairs' : {0:3, 2:1},
                        'treated' : np.array([0, 2]),
                        'control' : np.array([1, 3]),
                        'dropped' : np.array([])}
    np.testing.assert_equal(match.matches, expected_matches)
    np.testing.assert_equal(match.weights, np.ones(4))
    
    match.create(caliper_scale='propensity', caliper=0.01)
    expected_matches = {'match_pairs' : {0:3},
                        'treated' : np.array([0]),
                        'control' : np.array([3]),
                        'dropped' : np.array([1, 2])}
    np.testing.assert_equal(match.matches, expected_matches)
    np.testing.assert_equal(match.weights, np.array([1,0,0,1]))
    
    match.create(replace=True)    
    expected_matches = {'match_pairs' : {0:3, 2:3},
                        'treated' : np.array([0, 2]),
                        'control' : np.array([3]),
                        'dropped' : np.array([1])}
    np.testing.assert_equal(match.matches, expected_matches)
    np.testing.assert_equal(match.weights, np.array([1,0,1,2]))
    
def test_match_manytoone():
    np.random.seed(23456)
    match=Match(groups=[1,2,1,2], propensity=[0.1, 0.2, 0.15, 0.11])
    match.create(method='many-to-one')
    expected_matches = {'match_pairs' : {0:np.array([3]), 2: np.array([3])},
                        'treated' : np.array([0,2]),
                        'control' : np.array([3]),
                        'dropped' : np.array([1])}
    np.testing.assert_equal(match.matches, expected_matches)
    np.testing.assert_equal(match.weights, np.array([1,0,1,2]))
    
    match.create(method='many-to-one', caliper_scale='logit', replace=False)
    expected_matches = {'match_pairs' : {0:np.array([1]), 2: np.array([3])},
                        'treated' : np.array([0,2]),
                        'control' : np.array([1,3]),
                        'dropped' : np.array([])}
    np.testing.assert_equal(match.matches, expected_matches)    
    np.testing.assert_equal(match.weights, np.ones(4))
    
    match.create(method='many-to-one', many_method='knn', k=2, replace=True)
    expected_matches = {'match_pairs' : {0:np.array([3,1]), 2: np.array([3,1])},
                        'treated' : np.array([0,2]),
                        'control' : np.array([1,3]),
                        'dropped' : np.array([])}
    np.testing.assert_equal(match.matches, expected_matches)    
    np.testing.assert_equal(match.weights, np.ones(4))