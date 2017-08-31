#!/usr/bin/python
#-*- coding:utf-8 -*-
from math import sqrt

def sim_distance(prefs, obj1, obj2):
    # Euclidation Distance Score
    # compute the Eucildation Distance Score between two element the higher the better
    si = dict()
    for item in prefs[obj1]:
        if item in prefs[obj2]:
            si[item] = 1

    if len(si) == 0:
        return 0

    sum_of_squares = sum([
        pow(prefs[obj1][item]-prefs[obj2][item], 2)
        for item in prefs[obj1] if item in prefs[obj2]
        ])
    return 1 / (1 + sqrt(sum_of_squares))

def sim_pearson(prefs, obj1, obj2):
    # Pearson Correlation Score
    # More complex than Euclidation Distance Score, but work better when data set is less normalized
    # ex: when a user's score is always lower than the average value.
    # the higher the better
    si = dict()
    for item in prefs[obj1]:
        if item in prefs[obj2]:
            si[item] = 1

    n = len(si)
    if n == 0:
        return 0

    sum1 = sum([prefs[obj1][item] for item in si])
    sum2 = sum([prefs[obj2][item] for item in si])

    sum1Sq = sum([pow(prefs[obj1][item], 2) for item in si])
    sum2Sq = sum([pow(prefs[obj2][item], 2) for item in si])

    pSum = sum([prefs[obj1][item] * prefs[obj2][item] for item in si])

    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    return num / den

def topMatches(prefs, obj, n = 5, similarity = sim_pearson):
    # find the most similarity obj of the giving one.
    scores = [(similarity(prefs, obj, other), other) 
                for other in prefs if other != obj]

    scores.sort()
    scores.reverse()
    return scores[:n]

def get_recommendations(prefs, obj, similarity = sim_pearson):
    # making recommendations for giving obj

    totals = dict()
    sim_sums = dict()

    for other in prefs:
        if other != obj:
            sim = similarity(prefs, obj, other)
        else:
            continue

        if sim <= 0:
            continue
        for item in prefs[other]:
            if item not in prefs[obj] or prefs[obj][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                sim_sums.setdefault(item, 0)
                sim_sums[item] += sim

    rankings = [(totals / sim_sums[item], item) for item, total in totals.items()]

    rankings.sort()
    rankings.reverse()
    return rankings

def transfrom_prefs(prefs):
    result = dict()
    for obj in result:
        for item in prefs[obj]:
            result.setdefault(item, dict())
            result[item][obj] = prefs[obj][item]
    return result
