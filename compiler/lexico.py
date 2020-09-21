import logging
import re
from os import path
from enum import Enum, auto
import json
from compiler.utils import get_src_code, strip_comments

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TokenType(str, Enum):
    Keyword = "Keyword"
    Delimiter = "Delimiter"
    AttributionOperator = "AttributionOperator"
    ComparationOperator = "ComparationOperator"
    ArithmeticOperator = "ArithmeticOperator"
    Identifier = "Identifier"
    Unknown = "Unknown"


Blank = [' ', '\t']
Keyword = ['program', 'var', 'integer', 'real', 'boolean', 'procedure',
           'begin', 'end', 'if', 'then', 'else', 'while', 'do', 'not']
Delimiter = [';', '.', ':', '(', ')', ',']
AttributionOperator = [':=']
ComparationOperator = ['<', '>', '<=', '>=', '<>']
ArithmeticOperator = ['+', '-', '*', '/']
Operators = ArithmeticOperator + ArithmeticOperator + AttributionOperator
Digits = list(range(0, 10))


def get_token_type(token):
    if token in Keyword:
        return TokenType.Keyword
    elif token in Delimiter:
        return TokenType.Delimiter
    elif token in AttributionOperator:
        return TokenType.AttributionOperator
    elif token in ComparationOperator:
        return TokenType.ComparationOperator
    elif re.match(r'^[a-zA-Z][a-zA-Z0-0_]+$', token):
        return TokenType.Identifier
    else:
        return TokenType.Unknown


class TokenReader():
    def __init__(self):
        self.current_line = 1
        self.token_list = []
        self.current_token = ""
        self.current_char = ""
        self.stack = []

    def save_token(self, token):
        self.token_list.append({
            "token": token,
            "type": get_token_type(token)
        })
        self.current_token = ""

    def reset(self):
        self.current_line = 1
        self.token_list = []
        self.current_token = ""
        self.stack = []

    def process_number(self):
        # TODO
        pass

    def process_delimiter(self):
        if self.current_char == ':' and len(self.stack) > 0:
            char2 = self.stack.pop()  # Look ahead, we need to match :=
            pair = self.current_char + char2
            if pair in AttributionOperator:
                self.current_token = pair
                self.save_token(self.current_token)
            else:
                self.current_token += self.current_char
                self.stack.append(char2)
        else:
            self.save_token(self.current_token)
            self.save_token(self.current_char)

    def process_blank(self):
        if self.current_token == "":
            pass
        else:
            self.save_token(self.current_token)

    def process_operator(self):
        if self.current_char in ['<', '>']:
            char2 = self.stack.pop()  # Look ahead: <> <= >=
            pair = self.current_char + char2
            if pair in ComparationOperator:
                self.current_token = pair
                self.save_token(self.current_token)
            else:
                self.current_token += self.current_char
                self.stack.append(char2)

    def process_endline(self):
        self.current_line += 1

    def process_token(self):
        pass

    def process(self, src):
        self.stack = list(reversed(src.strip()))

        while len(self.stack) > 0:
            self.current_char = self.stack.pop()
            if re.search('[a-zA-Z]', self.current_char):
                self.current_token += self.current_char
            elif self.current_char in Blank:
                self.process_blank()
            elif self.current_char in Operators:
                self.process_operator()
            elif self.current_char in Delimiter:
                self.process_delimiter()
            elif self.current_char == '\n':
                self.process_endline()

        return self.token_list


def build_symbol_table(path):
    code = strip_comments(get_src_code(path))
    return TokenReader().process(code)


if __name__ == '__main__':
    # Testes rapidos...
    logging.basicConfig(level=logging.DEBUG)
    res = TokenReader().process(" Area := 3.14 * Raio * Raio;")
    logger.debug(json.dumps(res, indent=2))
