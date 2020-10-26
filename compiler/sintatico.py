from logging import error
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
        if len(self.stack) > 0:
            self.current_token = self.stack.pop()
            logger.debug(self.current_token)
        else:
            raise Exception("EOF")

    def compare_token(self, token_type, token_regex):
        return self.compare_token_type(token_type) \
            and self.compare_token_value(token_regex)

    def compare_token_value(self, token_regex):
        return re.match(token_regex, self.current_token['token'])

    def compare_token_type(self, token_type):
        return self.current_token['type'] == token_type

    def process_variables_declaration(self):
        if self.compare_token_value(TokenValueRegex.VAR):
            self.get_next_token()
            self.process_variables_list_declaration()
        else:
            self.get_next_token()

    def process_variables_list_declaration(self):
        self.process_identifiers_list()

        if self.compare_token_value(TokenValueRegex.COLON):
            self.get_next_token()
            self.process_type()

            if self.compare_token_value(TokenValueRegex.SEMICOLON):
                self.get_next_token()
                self.process_variables_list_declaration_2()
            else:
                raise Exception(
                    self.format_error_message(
                        "Error: delimiter ';' was expected."
                    ))
        else:
            raise Exception(
                self.format_error_message(
                    "Error: delimiter ':' was expected."
                ))

    def process_variables_list_declaration_2(self):
        if self.compare_token_type(TokenType.Identifier):
            self.process_identifiers_list()

            if self.compare_token_value(TokenValueRegex.COLON):
                self.get_next_token()
                self.process_type()

                if self.compare_token_value(TokenValueRegex.SEMICOLON):
                    self.get_next_token()
                    self.process_variables_list_declaration_2()
                else:
                    raise Exception(
                        self.format_error_message(
                            "Error: delimiter ';' was expected."
                        ))

            else:
                raise Exception(
                    self.format_error_message(
                        "Error: delimiter ':' was expected."
                    ))

        else:
            self.get_next_token()

    def process_identifiers_list(self):
        if self.compare_token_type(TokenType.Identifier):
            self.get_next_token()
            self.process_identifiers_list_2()
        else:
            raise Exception(self.format_error_message(
                'Erro: o programa espera um identificador válido.'))

    def process_identifiers_list_2(self):
        if self.compare_token_value(TokenValueRegex.COMMA):
            self.get_next_token()
            if self.compare_token_type(TokenType.Identifier):
                self.get_next_token()
                self.process_identifiers_list_2()
            else:
                raise Exception(self.format_error_message(
                    'Erro: o programa espera um identificador válido.'))

        else:
            self.get_next_token()

    def process_sub_programs_declararion(self):
        if self.compare_token(TokenType.Keyword, TokenValueRegex.PROCEDURE):
            self.process_sub_program_declaration()

            if self.compare_token(TokenType.Delimiter, TokenValueRegex.SEMICOLON):
                self.get_next_token()
                self.process_sub_programs_declararion_2()

            else:
                raise Exception('Delimitador ; esperado')
        else:
            self.get_next_token()

    def process_sub_programs_declararion_2(self):
        if self.compare_token(TokenType.Keyword, TokenValueRegex.PROCEDURE):
            self.process_sub_program_declaration()

            if self.compare_token(TokenType.Delimiter, TokenValueRegex.SEMICOLON):
                self.get_next_token()
                self.process_sub_programs_declararion_2()

            else:
                raise Exception('Delimitador ; esperado')
        else:
            self.get_next_token()

    def process_sub_program_declaration(self):
        if self.compare_token_value(TokenValueRegex.PROCEDURE):
            self.get_next_token()
            if self.compare_token_type(TokenType.Identifier):
                self.get_next_token()
                self.process_arguments()

                if self.compare_token(TokenType.Delimiter, TokenValueRegex.SEMICOLON):
                    self.get_next_token()
                    self.process_variables_declaration()
                    self.process_sub_programs_declararion()
                    self.process_compound_command()
                else:
                    raise Exception(
                        '";"  esperado antes de declaracao de variaveis de um subprograma')
            else:
                raise Exception(
                    'Um subprograma requer um identificador valido')
        else:
            raise Exception('Subprograma deve iniciar com "procedure"')

    def process_arguments(self):
        if self.compare_token_value(TokenValueRegex.OPEN_PARENTHESIS):
            self.get_next_token()
            self.process_params_list()

            if self.compare_token_value(TokenValueRegex.CLOSE_PARENTHESIS):
                self.get_next_token()
            else:
                raise Exception(
                    self.format_error_message(
                        '")" esperado apos list da parametros.')
                )
        else:
            self.get_next_token()

    def process_params_list(self):
        self.process_identifiers_list()
        if self.compare_token(TokenType.Delimiter, TokenValueRegex.COLON):
            self.get_next_token()
            self.process_type()
            self.process_params_list_2()
        else:
            raise Exception('Esperado ":" apos lista de identificadoers')

    def process_params_list_2(self):
        if self.compare_token(TokenType.Delimiter, TokenValueRegex.SEMICOLON):
            self.get_next_token()
            self.process_identifiers_list()

            if self.compare_token(TokenType.Delimiter, TokenValueRegex.COLON):
                self.get_next_token()
                self.process_type()
                self.process_params_list_2()
            else:
                raise Exception('Esperado  ":" apos lista de identificadoers')

    def process_compound_command(self):
        if self.compare_token(TokenType.Keyword, TokenValueRegex.BEGIN):
            self.get_next_token()
            self.optional_commands()

            if self.compare_token(TokenType.Keyword, TokenValueRegex.END):
                self.get_next_token()
            else:
                raise Exception('Comando composto deve acabar com end')

        else:
            raise Exception('Comando composto deve iniciar com begin')

    def optional_commands(self):
        pass

    def process_command(self):
        pass

    def process_variable(self):
        pass

    def process_expression_list(self):
        pass

    def process_expression(self):
        pass

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

        elif self.compare_token_type(TokenType.RealNumber):
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

    def process_sinal(self):
        if self.compare_token_value(TokenValueRegex.SINAL):
            self.get_next_token()
        else:
            raise Exception()

    def process_op_relacional(self):
        if self.compare_token_value(TokenValueRegex.OP_RELATIONAL):
            self.get_next_token()
        else:
            raise Exception()

    def process_op_aditivo(self):
        if self.compare_token_value(TokenValueRegex.OP_ADD):
            self.get_next_token()
        else:
            raise Exception()

    def process_op_multiplicativo(self):
        if self.compare_token_value(TokenValueRegex.OP_MULTI):
            self.get_next_token()
        else:
            raise Exception()

    def process_type(self):
        if not self.compare_token(TokenType.Keyword, TokenValueRegex.IDENTIFIER_TYPE):
            raise Exception()
        else:
            self.get_next_token()

    def process(self, token_table):
        self.stack = list(reversed(token_table))

        while len(self.stack) > 0:
            self.get_next_token()
            if self.compare_token(TokenType.Keyword, TokenValueRegex.PROGRAM):
                self.get_next_token()

                if self.compare_token_type(TokenType.Identifier):
                    self.get_next_token()

                    if self.compare_token(TokenType.Delimiter, TokenValueRegex.SEMICOLON):
                        self.get_next_token()
                        self.process_variables_declaration()
                        self.process_sub_programs_declararion()
                        # self.process_compound_command()

                        if not self.compare_token_value(TokenValueRegex.POINT):
                            raise Exception(
                                self.format_error_message(
                                    "Error: final delimiter '.' was expected."
                                )
                            )

                    else:
                        raise Exception(
                            self.format_error_message(
                                "Error: delimiter ';' was expected."
                            )
                        )

                else:
                    raise Exception(
                        self.format_error_message(
                            "Error: An valid identifier was expected."
                        )
                    )

            else:
                raise Exception(self.format_error_message(
                    "Error: 'program' identifier was not found."
                ))

    def format_error_message(self, message):
        if self.current_token:
            return message + " On line: " + str(self.current_token['line'])
        else:
            return message


def runSyntacticAnalysis(path, relative_path=False):
    data = get_symbol_table(path, relative_path)
    return SyntacticAnalyzer().process(data['symbol_table'])


if __name__ == '__main__':
    logger.debug(1)

    # Testes rapidos...
    logging.basicConfig(level=logging.DEBUG)
    logger.debug("Sintatico")

    res = runSyntacticAnalysis('lexico_Test3.json')
    logger.debug(json.dumps(res, indent=2))
