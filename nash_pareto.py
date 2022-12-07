"""
Author: Aidan Lynch

Script that finds any pure Pareto optimal states, pure Nash equilibrium, and
mixed Nash equilibrium.
"""

import sys
import numpy
from fractions import Fraction


def print_usage():
    print('usage: nash_pareto.py m n')
    print('\tm: number of rows in the payoff matrix, positive integer')
    print('\tn: number of columns in the payoff matrix, positive integer')


def format_frac(frac):
    if frac.numerator == 0:
        return "0"
    elif frac.denominator == 1:
        return "{}".format(frac.numerator)
    else:
        return "{}/{}".format(frac.numerator, frac.denominator)


def print_payoff(payoff):
    for row in range(0, len(payoff)):
        for col in range(0, len(payoff[0])):
            row_payoff = format_frac(payoff[row][col][0])
            col_payoff = format_frac(payoff[row][col][1])
            print("({:>6}, {:>6})".format(row_payoff, col_payoff), end=" ")
        print()


def parse_args(args: [str]) -> (bool, int, int):
    failure = (False, -1, -1)
    
    if len(args) != 3:
        return failure

    try:
        m = int(args[1])
        n = int(args[2])

        return failure if (m < 1 or n < 1) else (True, m, n)
    except ValueError:
        return failure


def get_payoff(m: int, n: int):
    failure = (False, [])
    payoff = numpy.full((m, n, 2), (0, 0))

    line = 0
    while line < m:
        line_str = input()
        tokens = line_str.split(' ')

        if len(tokens) != n:
            return failure

        for token_index in range(len(tokens)):
            token = tokens[token_index]
            comma_index = token.find(',')
            if comma_index < 0:
                return failure
            
            payoff[line][token_index][0] = Fraction(token[1:comma_index])
            payoff[line][token_index][1] = Fraction(token[comma_index + 1:-1])
        line += 1

    return True, payoff


def is_pareto_optimal(payoff, row_strat, col_strat):
    row_payoff = payoff[row_strat][col_strat][0]
    col_payoff = payoff[row_strat][col_strat][1]

    more_effecient = lambda p, row, col: ((row, col) != (row_strat, col_strat) and p[row][col][0] >= row_payoff and p[row][col][1] >= col_payoff)
    return len(run_pure(payoff, more_effecient)) == 0


def is_pure_nash_equilibrium(payoff, row_strat, col_strat):
    row_payoff = payoff[row_strat][col_strat][0]
    col_payoff = payoff[row_strat][col_strat][1]

    return row_payoff == max(payoff[row][col_strat][0] for row in range(0, len(payoff))) and \
        col_payoff == max(payoff[row_strat][col][1] for col in range(0, len(payoff[0])))


def run_pure(payoff, test):
    pure = []
    for row in range(0, len(payoff)):
        for col in range(0, len(payoff[0])):
            if test(payoff, row, col):
                pure.append((row, col))

    return pure


def main():
    (success, m, n) = parse_args(sys.argv)
    if not success:
        print_usage()
        exit()

    success, payoff = get_payoff(m, n)
    if success:
        print_payoff(payoff)
        pure_nash = run_pure(payoff, is_pure_nash_equilibrium)
        pure_pareto = run_pure(payoff, is_pareto_optimal)
        print("Pure Nash:", pure_nash)
        print("Pure Pareto:", pure_pareto)
    else:
        print("Invalid input!")


if __name__ == '__main__':
    main()
