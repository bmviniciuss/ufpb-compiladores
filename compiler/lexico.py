import logging
import re
from os import path
from enum import Enum, auto
import json
from compiler.utils import get_src_code, strip_comments
from compiler.exceptions import ParseError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TokenType(str, Enum):
    Keyword = "Keyword"
    Delimiter = "Delimiter"
    AttributionOperator = "AttributionOperator"
    ComparationOperator = "ComparationOperator"
    ArithmeticOperator = "ArithmeticOperator"
    Identifier = "Identifier"
    Number = "Number"
    Unknown = "Unknown"


Whitespace = [' ', '\t', '\n']
Keyword = ['program', 'var', 'integer', 'real', 'boolean', 'procedure',
           'begin', 'end', 'if', 'then', 'else', 'while', 'do', 'not']
Delimiter = [';', '.', ':', '(', ')', ',']
AttributionOperator = [':=']
ComparationOperator = ['<', '>', '<=', '>=', '<>']
ArithmeticOperator = ['+', '-', '*', '/']
Operators = ArithmeticOperator + ArithmeticOperator + AttributionOperator
Digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
ValidIdentifierPattern = r'^[a-zA-Z]([a-zA-Z0-9_])+$'
ValidNumberPattern = r'^([0-9]+$|^[0-9]+\.[0-9]+$)'


def get_token_type(token):
    if token in Keyword:
        return TokenType.Keyword
    elif token in Delimiter:
        return TokenType.Delimiter
    elif token in AttributionOperator:
        return TokenType.AttributionOperator
    elif token in ArithmeticOperator:
        return TokenType.ArithmeticOperator
    elif token in ComparationOperator:
        return TokenType.ComparationOperator
    elif re.match(ValidIdentifierPattern, token):
        return TokenType.Identifier
    elif re.match(ValidNumberPattern, token):
        return TokenType.Number
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
        logger.debug(token)
        self.token_list.append({
            "token": token,
            "type": get_token_type(token),
            "line": self.current_line
        })
        self.current_token = ""

    def reset(self):
        self.current_line = 1
        self.token_list = []
        self.current_token = ""
        self.stack = []

    def process_number(self):
        num = self.current_char

        while len(self.stack) > 0:
            char = self.stack.pop()
            if char in Digits + ['.']:
                num += char
            elif char in Delimiter or char in Whitespace:
                self.stack.append(char)
                break

        if not re.match(ValidNumberPattern, num):
            raise ParseError(
                'Invalid token %s in line %s' % (num, self.current_line))

        self.current_token = num
        self.save_token(self.current_token)

    def process_word(self):
        token = self.current_char
        while len(self.stack) > 0:
            char = self.stack.pop()
            if char in Delimiter or char in Whitespace:
                self.stack.append(char)
                break
            else:
                token += char

        if not re.match(ValidIdentifierPattern, token):
            raise ParseError(
                'Invalid token %s in line %s' % (token, self.current_line))

        self.current_token = token
        self.save_token(self.current_token)

    def process_delimiter(self):
        if self.current_char == ':':
            if len(self.stack) > 0:
                char2 = self.stack.pop()  # Look ahead, we need to match :=
                pair = self.current_char + char2
                if pair in AttributionOperator:
                    self.current_token = pair
                    self.save_token(self.current_token)
                else:
                    self.current_token = self.current_char
                    self.save_token(self.current_token)
                    self.stack.append(char2)
            else:
                # TODO: Deal with this possible error in other places
                raise ParseError('Last line must be a ";" token!')
        else:  # Put char back in the stack if we didnt care for it
            self.current_token = self.current_char
            self.save_token(self.current_token)

    def process_operator(self):
        if self.current_char in ['<', '>']:
            char2 = self.stack.pop()  # Look ahead: <> <= >=
            pair = self.current_char + char2
            if pair in ComparationOperator:
                self.current_token = pair
                self.save_token(self.current_token)

        else:  # Put char back in the stack if we didnt care for it
            self.current_token = self.current_char
            self.save_token(self.current_token)

    def process_Whitespace(self):
        if self.current_char == '\n':
            self.current_line += 1

    def process(self, src):
        self.stack = list(reversed(src.strip()))

        while len(self.stack) > 0:
            self.current_char = self.stack.pop()
            if re.search('[a-zA-Z]', self.current_char):
                self.process_word()
            elif self.current_char in Whitespace:
                self.process_Whitespace()
            elif self.current_char in Operators:
                self.process_operator()
            elif self.current_char in Delimiter:
                self.process_delimiter()
            elif self.current_char in Digits:
                self.process_number()
            else:
                raise ParseError("Couldn't parse token %s in line %s",
                                 self.current_char, self.current_line)

        return self.token_list


def build_symbol_table(path):
    code = strip_comments(get_src_code(path))
    return TokenReader().process(code)


if __name__ == '__main__':
    # Testes rapidos...
    logging.basicConfig(level=logging.DEBUG)
    res = build_symbol_table('Test1.pas')
    # res = TokenReader().process('      Raio := 4;')
    logger.debug(json.dumps(res, indent=2))
