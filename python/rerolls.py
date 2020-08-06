"""Simple program to explore probability in regards to rolling dice and being able to reroll failures

I was playing King of Tokyo (tm) with some friends and we stated talking about the probability of achieving all success and the expected number of rolls required before achieving that. For those that aren't aware, in King of Tokyo you start with six six-sided die, with each side having a different effect. Now suppose we wanted to roll all six as claws to maximize our attack. What is the probability of acheiving this? Also, suppose we had certain effects that increased our number of rerolls. What is the expected number of rolls/rerolls we would need to achieve all successes.

This file can also be imported as a module, and contains the following useful function
    * probability_of_all_successes - the probability of achieving all successes
    * average_simulate_rerolling - the expected number of rerolls to achieve all successes
"""

import random
import sys

def probability_of_all_successes(p: float, r: int, n: int) -> float:
    """Calculate the probability of achieving all successes

    Given a certain number of dice, their probability of a success, and the
    allowed number of rolls/rerolls, calculates the probability of achieving
    all successes.

    This implements a recursion I solved when thinking about this problem.
    f(p,1,n) = p^n, the probability of rolling all successes in one roll
    f(p,r,0) = 1, if we need to achieve 0 successful rolls, it is always achieved
    f(p,r,n) = SUM_{x=0}^{n} p^x (1-p)^x f(p,r-1,n-x)
    For the final equation, we add up the probabilities of achieving each number
    of success in the current roll, and then achieving all successes with the
    remaining rolls by applying recursion. We could use dynamic programming
    if we were dealing with larger numbers and wanted to make this program
    more efficient

    Parameters
    ----------
    p : float
        the probability of success for the roll of a single dice
    r : int
        The number of rolls/rerolls allowed
    n : int
        The number of objects being rolled. Can be thought of as dice, but are
        not limited to 1 / int. They can have any success value [0-1]

    Returns
    -------
    float
        the probability of achieving all successes
    """

    if r == 1:
        return pow(p, n)
    elif n == 0:
        return 1
    else:
        result = 0
        for x in range(0, n+1):
            result += pow(p, x) * pow(1-p, n-x) * probability_of_all_successes(p, r-1, n-x)
        return result 

def pretty_print_poas_result(probability: float, rerolls: int, num_objects: int):
    """Pretty print the results of probability_of_all_successes

    Parameters
    ----------
    p : float
        the probability of success for the roll of a single dice
    r : int
        The number of rolls/rerolls allowed
    n : int
        The number of objects being rolled. Can be thought of as dice, but are
        not limited to 1 / int. They can have any success value [0-1]
    """

    result = probability_of_all_successes(probability, rerolls, num_objects)
    print(f"Given {num_objects} dice with a probability of success of {probability} and {rerolls} rolls")
    print(f"The probability of achieving all successes is {result}")

def simulate_rerolling(p: float, n: int) -> int:
    """Simulate rolling a number of dice until they are all successes and
    return the number of rolls/rerolls

    Given n dice and a probability of success of p, simulate rolling and
    rerolling the dice until they are all successes. After the initial roll,
    we increment the counter and reroll any dice that failed. This repeats
    until all dice succeed

    Parameters
    ----------
    p : float
        the probability of success for the roll of a single dice
    n : int
        The number of objects being rolled. Can be thought of as dice, but are
        not limited to 1 / int. They can have any success value [0-1]

    Returns
    -------
    int
        the number of rolls/rerolls necessary to achieve all successes
    """

    counter = 0
    new_n = n
    while new_n > 0:
        for _ in range(new_n):
            ran = random.random()
            if ran < p:
                new_n -= 1
        counter += 1
    return counter

def average_simulate_rerolling(probability: float, num_objects: int, trials: int):
    """Run simulate_rerolling for a given number of trials and print the result

    For a given number of trials, run the simulate_rerolling simulation and
    average all of the results. This gives the expected number of rolls/rerolls
    we must perform before we have all successes

    Parameters
    ----------
    probability : float
        the probability of success for the roll of a single dice
    num_objects : int
        The number of objects being rolled. Can be thought of as dice, but are
        not limited to 1 / int. They can have any success value [0-1]
    """

    results = []
    for _ in range(trials):
        results.append(simulate_rerolling(probability, num_objects))
    print(f"Given {num_objects} dice with a probability of success of {probability}, after {trials} trials")
    print(f"Number of expected rolls to have all successes is {sum(results)/len(results)}")

def print_help_menu():
    """Print the help menu for this command line program
    """

    print("""This program contains two different tools for calculating values
    [--rerolls, -r] p n t
    Find the expected number of rolls/rerolls to achieve all successes
    p is the probability of success on a given die roll
    n is the number of objects we are rolling
    t is the number of trials we are performing to find the average
    [--success, -s] p, r, n
    Directly calculates the probability of achieving all successes
    p is the probability of success on a given die roll
    r is the number of rolls/rerolls we are allowed to perform
    n is the number of objects we are rolling
    """)

def are_close(num1: float, num2: float, error: float) -> bool:
    """Check if two numbers are within a certain error of each other

    Parameters
    ----------
    num1 : float
        first number
    num2 : float
        second number
    error : float
        the level of allowed error between the numbers

    Returns
    -------
    bool
        true if the numbers are within a certain error of each other
    """

    if abs(num1-num2) < error:
        return True
    return False

def test_probability_of_all_successes():
    """Some test cases for probability_of_all_successes
    """

    assert(probability_of_all_successes(1/2,1,2) == 0.25)
    assert(are_close(probability_of_all_successes(1/6,1,2), 1/36, 0.001))
    assert(are_close(probability_of_all_successes(1/2,2,2), 7/16, 0.001))

def main():
    # Help menu
    if len(sys.argv) >= 2 and sys.argv[1] in ["-h", "--help"]:
        print_help_menu()
    # Rerolls
    elif len(sys.argv) == 5 and sys.argv[1] in ["--rerolls", "-r"]:
        probability, num_objects, trials = sys.argv[2:]
        probability = float(probability)
        num_objects = int(num_objects)
        trials = int(trials)
        average_simulate_rerolling(probability, num_objects, trials)
    # All successes
    elif len(sys.argv) == 5 and sys.argv[1] in ["--success", "-s"]:
        probability, rerolls, num_objects = sys.argv[2:]
        probability = float(probability)
        rerolls = int(rerolls)
        num_objects = int(num_objects)
        pretty_print_poas_result(probability, rerolls, num_objects)
    # Demonstration
    else:
        print("Invalid command line arguments, so here is a simple demonstration of the two functionalities")
        average_simulate_rerolling(1/6, 10, 1000)
        pretty_print_poas_result(1/6, 3, 6)

if __name__ == "__main__":
    main()
