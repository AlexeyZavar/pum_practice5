from .converter import Converter
from .evaluator import Evaluator
from .exceptions import LexerException
from .lexer import Lexer
from .tokenizer import Tokenizer


class EasyWrapper:
    def __init__(self, s):
        self.lexer = Lexer()
        self.tokenizer = Tokenizer()
        self.converter = Converter()
        self.evaluator = Evaluator()

        try:
            self.lexer_result = self.lexer.parse(s)
            self.valid = True
        except LexerException as e:
            self.lexer_result = None
            self.valid = False

            return

        self.tokenizer_result = self.tokenizer.tokenize(self.lexer_result)
        self.converter_result = self.converter.convert(self.tokenizer_result)

    def __call__(self, x: float = 0):
        return self.evaluator.eval(self.converter_result, x)
