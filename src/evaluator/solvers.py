import logging
from typing import Callable

from .wrapper import EasyWrapper

logger = logging.getLogger('Lexer')

EPSILON = 0.001
N = int(100000 / 4)
MAX_STEPS = N


def solve_using_secant(expr: EasyWrapper, a: float, b: float):
    step = 1

    while 1:
        a1 = expr(a)
        b1 = expr(b)

        if a1 == b1:
            logger.error('Division by zero')
            return None

        x = a - (b - a) * a1 / (b1 - a1)
        logger.debug(f'{step = }, {x = }')

        a = b
        b = x

        if abs(expr(x)) <= EPSILON:
            break

        if step >= MAX_STEPS:
            return None

        step += 1

    return x


def integral_using_simpson(expr: EasyWrapper, a: float, b: float, callback: Callable = None):
    # powered by Johny
    # adopted by me <3
    dx = (b - a) / N
    res = 0

    for i in range(N):
        # https://en.wikipedia.org/wiki/Simpson%27s_rule
        res += (dx / 6) * (expr(a + i * dx) + 4 * expr((2 * a + (2 * i + 1) * dx) / 2) + expr(a + (i + 1) * dx))

        # this method can be slow, so give some feedback on operation progress
        if i % 10000 == 0 and callback is not None:
            callback(i, N)

    return res
