import logging

from .wrapper import EasyWrapper

logger = logging.getLogger('Lexer')

EPSILON = 0.00001


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
