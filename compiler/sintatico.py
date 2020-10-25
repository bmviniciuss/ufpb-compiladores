from compiler.utils import get_symbol_table
from compiler.types import TokenType, TokenValueRegex
import logging
import json
import re


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SyntacticAnalyzer():
    def __init__(self):
        self.current_token = ""
        self.stack = []

    def get_next_token(self):
        self.current_token = self.stack.pop()
        logger.debug(self.current_token)

    def compare_token(self, token_type, token_regex):
        return self.compare_token_type(token_type) \
            and self.compare_token_value(token_regex)

    def compare_token_value(self, token_regex):
        return re.match(token_regex, self.current_token['token'])

    def compare_token_type(self, token_type):
        return self.current_token['type'] == token_type

    def process_op_multiplicativo(self):
        if self.compare_token_value(TokenValueRegex.OP_MULTI):
            self.get_next_token()
        else:
            raise Exception()

    def process_op_aditivo(self):
        if self.compare_token_value(TokenValueRegex.OP_ADD):
            self.get_next_token()
        else:
            raise Exception()

    def process_op_relacional(self):
        if self.compare_token_value(TokenValueRegex.OP_RELATIONAL):
            self.get_next_token()
        else:
            raise Exception()

    def process_sinal(self):
        if self.compare_token_value(TokenValueRegex.SINAL):
            self.get_next_token()
        else:
            raise Exception()

    def process_fator(self):
        if self.compare_token_type(TokenType.Identifier):
            self.get_next_token()
            if self.compare_token(TokenType.Delimiter, TokenValueRegex.OPEN_PARENTHESIS):
                self.get_next_token()
                self.process_expression_list()

                if self.compare_token(TokenType.Delimiter, TokenValueRegex.CLOSE_PARENTHESIS):
                    self.get_next_token()
                else:
                    raise Exception()

        elif self.compare_token_type(TokenType.Integer):
            self.get_next_token()

        elif self.compare_token_type(TokenType.Real):
            self.get_next_token()

        elif self.compare_token_value(TokenValueRegex.BOOLEAN):
            self.get_next_token()

        elif self.compare_token(TokenType.Delimiter, TokenValueRegex.OPEN_PARENTHESIS):
            self.get_next_token()

            self.process_expression()
            if self.compare_token(TokenType.Delimiter, TokenValueRegex.CLOSE_PARENTHESIS):
                self.get_next_token()
            else:
                raise Exception()

        elif self.compare_token_value(TokenValueRegex.NOT):
            self.get_next_token()
            self.process_fator()

        else:
            raise Exception()

    def process_expression(self):
        pass

    def process_expression_list(self):
        pass

    def process_variable(self):
        pass

    def process_command(self):
        pass

    def process_params_list(self):
        pass

    def process_arguments(self):
        if self.compare_token(TokenType.Delimiter, TokenValueRegex.OPEN_PARENTHESIS):
            self.get_next_token()
            self.process_params_list()

            if self.compare_token(TokenType.Delimiter, TokenValueRegex.CLOSE_PARENTHESIS):
                self.get_next_token()
            else:
                raise Exception()
        else:
            self.get_next_token()

    def optional_commands(self):
        pass

    def process_compound_command(self):
        if self.compare_token(TokenType.Keyword, TokenValueRegex.TokenValueRegex):
            self.get_next_token()
            self.optional_commands()

            if self.compare_token(TokenType.Keyword, TokenValueRegex.END):
                self.get_next_token()
            else:
                raise Exception()

        else:
            raise Exception()

    def process_sub_programs_declararion(self):
        pass

    def process_variables_declaration(self):
        if self.compare_token(TokenType.Identifier, TokenValueRegex.VAR):
            self.get_next_token()
            self.process_variables_list_declaration()
        else:
            self.get_next_token()

    def internal_process_variables_list(self):
        if self.compare_token(TokenType.Delimiter, TokenValueRegex.COLON):
            self.get_next_token()
            self.process_type()

            if self.compare_token(TokenType.Delimiter, TokenValueRegex.SEMICOLON):
                self.get_next_token()
                self.process_variables_list_declaration_2()
            else:
                # return False
                raise Exception()

        else:
            # return False
            raise Exception()

    def process_variables_list_declaration(self):
        self.process_identifiers_list()
        self.internal_process_variables_list()

    def process_variables_list_declaration_2(self):
        if self.compare_token_type(TokenType.Identifier):
            self.process_identifiers_list()
            self.internal_process_variables_list()
        else:
            self.get_next_token()

    def process_identifiers_list(self):
        if self.compare_token_type(TokenType.Identifier):
            self.get_next_token()
            self.process_identifiers_list()
        elif self.compare_token(TokenType.Delimiter, TokenValueRegex.COMMA):
            self.get_next_token()
            if self.compare_token_type(TokenType.Identifier):
                self.get_next_token()
                self.process_identifiers_list()
            else:
                raise Exception()

        else:
            raise Exception()

    def process_type(self):
        if not self.compare_token(TokenType.Keyword, TokenValueRegex.IDENTIFIER_TYPE):
            raise Exception()
        else:
            self.get_next_token()

    def process(self, token_table):
        self.stack = list(reversed(token_table))
        data = {}

        while len(self.stack) > 0:
            self.get_next_token()
            logger.debug(self.current_token)
            if self.compare_token(TokenType.Keyword, TokenValueRegex.PROGRAM):
                self.get_next_token()

                if self.compare_token_type(TokenType.Identifier):
                    self.get_next_token()

                    if self.compare_token(TokenType.Delimiter, TokenValueRegex.SEMICOLON):
                        self.get_next_token()
                        self.process_variables_declaration()
                        self.process_sub_programs_declararion()
                        self.process_compound_command()

                        if not self.compare_token(TokenType.Delimiter, TokenValueRegex.POINT):
                            raise Exception()

                    else:
                        raise Exception()

                else:
                    raise Exception()

            else:
                raise Exception()


def runSyntacticAnalysis(path, relative_path=False):
    data = get_symbol_table(path, relative_path)
    return SyntacticAnalyzer().process(data['symbol_table'])


if __name__ == '__main__':
    logger.debug(1)

    # Testes rapidos...
    logging.basicConfig(level=logging.DEBUG)
    logger.debug("Sintatico")

    res = runSyntacticAnalysis('lexico_Test4.json')
    logger.debug(json.dumps(res, indent=2))
