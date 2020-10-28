import json
import logging
import re
from compiler.exceptions import ParseError
from compiler.utils import get_src_code, strip_comments
from enum import Enum, auto
from os import path

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TokenType(str, Enum):
    Keyword = "Keyword"
    Delimiter = "Delimiter"
    AttributionOperator = "AttributionOperator"
    ComparisonOperator = "ComparisonOperator"
    AdditiveOperators = "AdditiveOperators"
    MultiplicativeOperators = "MultiplicativeOperators"
    Identifier = "Identifier"
    Integer = "Integer"
    RealNumber = "RealNumber"
    Unknown = "Unknown"


Whitespace = [' ', '\t', '\n', '']
Keyword = ['program', 'var', 'integer', 'real', 'boolean', 'procedure',
           'begin', 'end', 'if', 'then', 'else', 'while', 'do', 'not', 'for', 'to']
Delimiter = [';', '.', ':', '(', ')', ',']
AttributionOperator = [':=']
ComparisonOperator = ['=', '<', '>', '<=', '>=', '<>']
AdditiveOperators = ['+', '-']
MultiplicativeOperators = ['*', '/']
Operator = AdditiveOperators + MultiplicativeOperators + \
    ComparisonOperator + AttributionOperator
Digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
ValidIdentifierPattern = r'^[a-zA-Z]([a-zA-Z0-9_])*$'
ValidNumberPattern = r'^([0-9]+$|^[0-9]+\.[0-9]+$)'
ValidIntegerPattern = r'^[0-9]+$'
ValidRealNumberPattern = r'^[0-9]+\.[0-9]+$'


def get_token_type(token):
    if token in Keyword:
        return TokenType.Keyword
    elif token in Delimiter:
        return TokenType.Delimiter
    elif token in AttributionOperator:
        return TokenType.AttributionOperator
    elif token in AdditiveOperators:
        return TokenType.AdditiveOperators
    elif token in MultiplicativeOperators:
        return TokenType.MultiplicativeOperators
    elif token in ComparisonOperator:
        return TokenType.ComparisonOperator
    elif re.match(ValidIdentifierPattern, token):
        return TokenType.Identifier
    elif re.match(ValidIntegerPattern, token):
        return TokenType.Integer
    elif re.match(ValidRealNumberPattern, token):
        return TokenType.RealNumber
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

    def take_until(self, terminals, whitelist=[]):
        """Takes the next characters until hitting a terminal, updates current_token along the way.
        Puts terminal back on stack after terminating.

        Args:
            terminals ([type]): List of symbols we should stop at
            whitelist (list, optional): Exclusion list for terminals, for convenience. Defaults to [].
        """
        tmp_token = self.current_char
        while len(self.stack) > 0:
            char = self.stack.pop()
            if char in terminals and char not in whitelist:
                self.stack.append(char)
                self.current_token = tmp_token
                break
            else:
                tmp_token += char

        self.current_token = tmp_token

    def take_pair(self, valid_pairs):
        """Takes a pair of chars, if no matching pairs are found after peeking ahead, puts leading char
        back on stack and proceeds as normal

        Args:
            valid_pairs ([type]): List of pairs we're looking for when peeking ahead
        """
        if not len(self.stack) > 0:
            return

        first = self.current_char
        second = self.stack.pop()
        pair = first + second
        if pair in valid_pairs:
            self.current_token = pair
            self.save_token(self.current_token)
        else:
            self.current_token = first
            self.stack.append(second)
            self.save_token(self.current_token)

    def process_number(self):
        self.take_until(Delimiter + Whitespace, ['.'])

        if not re.match(ValidNumberPattern, self.current_token):
            raise ParseError(
                'Invalid token %s in line %s' % (self.current_token, self.current_line))

        self.save_token(self.current_token)

    def process_word(self):
        self.take_until(Delimiter + Whitespace + Operator + ['.'])

        if not re.match(ValidIdentifierPattern, self.current_token):
            raise ParseError(
                'Invalid token %s in line %s' % (self.current_token, self.current_line))

        self.save_token(self.current_token)

    def process_delimiter(self):
        if self.current_char == ':':
            self.take_pair(AttributionOperator)
        else:
            self.current_token = self.current_char
            self.save_token(self.current_token)

    def process_operator(self):
        if self.current_char in ['<', '>']:
            self.take_pair(ComparisonOperator)

        else:
            self.current_token = self.current_char
            self.save_token(self.current_token)

    def process_Whitespace(self):
        if self.current_char == '\n':
            self.current_line += 1

    def process(self, src):
        self.stack = list(reversed(src.strip()))
        data = {}

        while len(self.stack) > 0:
            try:
                self.current_char = self.stack.pop()
                if re.search('[a-zA-Z]', self.current_char):
                    self.process_word()
                elif self.current_char in Whitespace:
                    self.process_Whitespace()
                elif self.current_char in Operator:
                    self.process_operator()
                elif self.current_char in Delimiter:
                    self.process_delimiter()
                elif self.current_char in Digits:
                    self.process_number()
                else:
                    raise ParseError("Couldn't parse token '%s' in line %s" % (
                        self.current_char, self.current_line))
            except ParseError as e:
                data['error'] = str(e)
                break

        data['symbol_table'] = self.token_list
        data['total_symbols'] = len(self.token_list)
        return data


def build_symbol_table(path, relative_path=False):
    code = strip_comments(get_src_code(path, relative_path))
    return TokenReader().process(code)


def get_sym_table(src_code):
    code = strip_comments(src_code)
    return TokenReader().process(code)['symbol_table']


if __name__ == '__main__':
    # Testes rapidos...
    logging.basicConfig(level=logging.DEBUG)
    res = build_symbol_table('Test4.pas')
    # res = TokenReader().process('Area := 3.14 * Raio * Raio;')
    logger.debug(json.dumps(res, indent=2))
