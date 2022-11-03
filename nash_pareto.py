import sys
import numpy
from fractions import Fraction

def print_usage():
    print('usage: nash_pareto.py m n')
    print('\tm: number of rows in the payoff matrix, positive integer')
    print('\tn: number of columns in the payoff matrix, positive integer')

def parse_args(args: [str]) -> (bool, int, int):
    failure = (False, -1, -1)
    
    if len(args) != 3:
        return failure

    try:
        m = int(args[1])
        n = int(args[2])

        return failure if (m < 1 or n < 1) else (True, m, n)
    except:
        return failure

def get_payoff(m: int, n: int):
    failure = (False, [])
    payoff = numpy.full((m, n, 2), (0, 0))
    print(payoff)

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

def main():
    (success, m, n) = parse_args(sys.argv)
    if not success:
        print_usage()
        exit()

    (success, payoff) = get_payoff(m, n)


if __name__ == '__main__':
    main()
