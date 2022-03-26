import logging
from typing import List

from .consts import *
from .exceptions import LexerException

logger = logging.getLogger('Lexer')


class LexerResult:
    def __init__(self, result: List[str], is_function: bool):
        self.result = result
        self.is_function = is_function

    def __str__(self):
        s = ''

        for item in self.result:
            if item in OPERATORS and item != SYMBOL_DEGREE:
                s += ' '
                s += item
                s += ' '
            else:
                s += item

        return s

    def __repr__(self):
        s = '; '.join(self.result)

        return f'LexerResult({s})'


class Lexer:
    def __init__(self):
        self._state = 'S'
        self._buffer = ''
        self._index = 0
        self._current_char = ''
        self._brackets_count = 0
        self._is_function = False
        self._result = []

        self._machine = {
            'S': self._state_s,
            'I': self._state_i,
            'R': self._state_r,
            'B': self._state_b,
            'F': self._state_f,
            'X': self._state_x
        }
        self._expectations = {
            'S': 'number, letter, unary minus or opening bracket',
            'I': 'number, operator, comma or closing bracket',
            'R': 'number, operator or closing bracket',
            'B': 'operator or closing bracket',
            'F': 'letter or opening bracket',
            'X': 'closing bracket or operator',
            'B_ERR': 'right brackets count'
        }

        assert all(item in self._expectations for item in self._machine.keys())

    def _flush_buffer(self):
        if self._buffer:
            logger.debug('Flushing buffer with "{buffer}"'.format(buffer=self._buffer))

            self._result.append(self._buffer)
            self._buffer = ''
        else:
            logger.debug('Nothing to flush')

    def _append_current_char(self):
        logger.debug('Buffering "{char}"'.format(char=self._current_char))
        self._buffer += self._current_char

    def _flush_current_char(self):
        logger.debug('Flushing "{char}"'.format(char=self._current_char))
        self._result.append(self._current_char)

    def _reset(self):
        self._state = 'S'
        self._buffer = ''
        self._index = 0
        self._current_char = ''
        self._brackets_count = 0
        self._is_function = False
        self._result = []

    def _state_s(self):
        if self._current_char.isdigit():
            self._append_current_char()
            return 'I'

        if self._current_char == SYMBOL_BRACKET_OPEN:
            self._brackets_count += 1
            self._flush_current_char()
            return 'S'
        if self._current_char == SYMBOL_MINUS:
            self._append_current_char()
            return 'S'

        if self._current_char in ALPHABET and self._current_char != SYMBOL_VARIABLE:
            self._append_current_char()
            return 'F'

        if self._current_char == SYMBOL_VARIABLE:
            self._append_current_char()
            self._flush_buffer()
            return 'X'

        self._raise_exception()

    def _state_i_r_shared(self):
        if self._current_char.isdigit():
            self._append_current_char()
            return 'I'

        if self._current_char == SYMBOL_BRACKET_CLOSE:
            self._brackets_count -= 1
            self._flush_buffer()
            self._flush_current_char()
            return 'B'

        if self._current_char in OPERATORS:
            self._flush_buffer()
            self._flush_current_char()
            return 'S'

        self._raise_exception()

    def _state_i(self):
        if self._current_char in COMMAS:
            self._append_current_char()
            return 'R'

        return self._state_i_r_shared()

    def _state_r(self):
        return self._state_i_r_shared()

    def _state_b(self):
        if self._current_char == SYMBOL_BRACKET_CLOSE:
            self._brackets_count -= 1
            self._flush_current_char()
            return 'B'

        if self._current_char in OPERATORS:
            self._flush_buffer()
            self._flush_current_char()
            return 'S'

        self._raise_exception()

    def _state_f(self):
        if self._current_char in ALPHABET:
            self._append_current_char()
            return 'F'

        if self._current_char == SYMBOL_BRACKET_OPEN:
            self._brackets_count += 1
            self._flush_buffer()
            self._flush_current_char()
            return 'S'

        self._raise_exception()

    def _state_x(self):
        self._is_function = True

        if self._current_char == SYMBOL_BRACKET_CLOSE:
            self._brackets_count -= 1
            self._flush_current_char()
            return 'B'

        if self._current_char in OPERATORS:
            self._flush_buffer()
            self._flush_current_char()
            return 'S'

        self._raise_exception()

    def _raise_exception(self):
        expected = self._expectations[self._state]

        msg = 'Excepted {expected}, but got "{char}"'.format(expected=expected, char=self._current_char)

        logger.error(msg)
        self._reset()

        raise LexerException(self._index, msg)

    def parse(self, s: str):
        if not s:
            raise LexerException(0, 'Empty input string')

        for i, ch in enumerate(s):
            if ch == ' ':
                continue

            self._index = i
            self._current_char = ch
            self._state = self._machine[self._state]()

        self._flush_buffer()

        if self._brackets_count != 0:
            # todo: wtf
            self._state = 'B_ERR'
            self._current_char = self._brackets_count

            self._raise_exception()

        res = self._result
        is_function = self._is_function
        self._reset()

        return LexerResult(res, is_function)
