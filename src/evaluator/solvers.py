import logging

from .wrapper import EasyWrapper

logger = logging.getLogger('Lexer')

EPSILON = 0.00001
N = 100000


def solve_using_secant(expr: EasyWrapper, a: float, b: float):
    step = 1

    while 1:
        a1 = expr(a)
        b1 = expr(b)

        if a1 == b1:
            logger.debug('Division by zero')
            return None

        x = a - (b - a) * a1 / (b1 - a1)
        logger.debug(f'{step = }, {x = }')

        a = b
        b = x

        if abs(expr(x)) <= EPSILON:
            break

    return x


def integral_using_simpson(expr: EasyWrapper, a: float, b: float):
    # powered by Johny
    # adopted by me <3
    dx = (b - a) / N
    res = 0

    for i in range(N):
        # https://en.wikipedia.org/wiki/Simpson%27s_rule
        res += (dx / 6) * (expr(a + i * dx) + 4 * expr((2 * a + (2 * i + 1) * dx) / 2) + expr(a + (i + 1) * dx))

    return res
