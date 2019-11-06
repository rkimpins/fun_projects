"""
This is a program to try out a solution to the unfair flipping coin challenge
posed in "Introductions to Algorithms". The idea is that we are given an unfair
coin that return heads alpha of the time. Given this coin, can we make a new method
that is fair, aka, returns heads 0.5 of the time. My solution follows, with
some nice visualizations
Author: Randal Kimpinski
Date: Nov 5, 2019
"""

import matplotlib.pyplot as plt
import numpy as np
import random
import time

def unfair_flip(alpha):
    """ Flip an unfair coind, which with probability alpha, will return heads """
    if (random.random() > alpha):
        return 1
    else:
        return 0

def unfair_to_fair(alpha):
    """ Uses an unfair coin to generate fair coin flippings

    We accomplish this by fliping the two unfair coins. If exactly 1 is heads,
    we return 1 if it was coin 1, and 0 if it was coin 2. If they are the same,
    we call the function again
    """

    x1 = unfair_flip(alpha)
    x2 = unfair_flip(alpha)
    while(x1 == x2):
        x1 = unfair_flip(alpha)
        x2 = unfair_flip(alpha)
    return x1

def how_many_fails(alpha):
    """ For a given alpha level, how many times do we need to repeat our method """

    x1 = unfair_flip(alpha)
    x2 = unfair_flip(alpha)
    counter = 1
    while(x1 == x2):
        x1 = unfair_flip(alpha)
        x2 = unfair_flip(alpha)
        counter += 1
    return counter

def test_how_many_fails():
    """ Test how_many_fails for vairous alpha levels """

    alphas = np.arange(0.005, 0.50, 0.001)
    results = list()
    reps = 5000
    for alpha in alphas:
        print(f"Running {reps} flips on alpha = {alpha}")
        total = 0
        for _ in range(reps):
            total += how_many_fails(alpha)
        total /= reps
        results.append(total)
    fig1, ax1 = plt.subplots()
    plt.title("Number of collisions from alpha")
    plt.xlabel("Alpha Values")
    plt.ylabel("Number of collisions")
    plt.plot(alphas, results)
    plt.show()

def ratio_for_fair():
    reps = 1000000
    alphas = [0.49, 0.45, 0.4, 0.3, 0.2, 0.1, 0.01, 0.001, 0.0001, 0.00001]
    for alpha in alphas:
        total = 0
        for _ in range(reps):
            total += unfair_to_fair(alpha)
        res = total / reps
        print(f"Over {reps} (one million) repetitions, for alpha = {alpha}, our fair method gives a ratio of {res}")

def main():
    print("""Say we are given an unfair coin, and want to get results that are fair. What can we do?
    We can flip two coins, and if they are different, return the value of the first coin.
    Lets explore more""")
    inp = input("Live Demo [g] or Data analysis [a]:")
    if (inp == "a"):
        ratio_for_fair()
        test_how_many_fails()
        return
    alpha = 0.2
    fflips = list()
    uflips = list()
    reps = 1000
    total = 0
    plt.figure(2)
    graph1 = plt.subplot(1,2,1)
    graph2 = plt.subplot(1,2,2)
    utot = 0
    ftot = 0
    for i in range(reps):
        if (i < 20):
            plt.pause(0.2)
        elif (i < 100):
            plt.pause(0.05)
        else:
            plt.pause(0.00001)
        uflip = unfair_flip(alpha)
        fflip = unfair_to_fair(alpha)
        uflips.append(uflip)
        fflips.append(fflip)
        utot += unfair_flip(alpha)
        ftot += unfair_to_fair(alpha)
        ylim = max(utot, i - utot)
        graph1.clear()
        graph2.clear()

        graph1 = plt.subplot(1,2,1)
        graph1.hist(uflips, bins=3)
        plt.title("Unfair flips")
        plt.xlabel("Flip value")
        plt.ylabel("Frequency")
        plt.ylim(0,ylim)
        plt.xticks([0,1])


        graph2 = plt.subplot(1,2,2)
        graph2.hist(fflips, bins=3)
        plt.title("Fairified")
        plt.xlabel("Flip value")
        plt.ylabel("Frequency")
        plt.ylim(0,ylim)
        plt.xticks([0,1])
        plt.suptitle(f"Alpha = {alpha}, Repetitions = {i}")
main()
