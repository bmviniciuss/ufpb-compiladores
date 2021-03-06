from logging import error
from os import path
from compiler.utils import get_symbol_table
from compiler.types import TokenType, TokenValueRegex
from compiler import lexico
from compiler.identifiers_stack import IdentifiersStack
from compiler.typed_identifiers_stack import TypedIdentifiersStack
from compiler.pct import PCT

import pathlib
import logging
import json
import re
import sys


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SyntacticAnalyzer():
    def __init__(self):
        self.current_token = ""
        self.stack = []
        self.identifiers_stack = IdentifiersStack()
        self.typed_identifiers = TypedIdentifiersStack()
        self.pct = PCT()

    def search_identifier_and_add_to_pct(self, identifier_name):
        identifier = self.typed_identifiers.search(identifier_name)
        if identifier:
            self.pct.push(identifier['type'])

    def check_identifier_declaration(self, identifier):
        if not self.identifiers_stack.search(identifier):
            raise Exception(self.format_error_message(
                "Idendificador " + identifier + " não foi declarado."
            ))

    def add_typed_identifiers(self, type, identifiers):
        for token in identifiers:
            item = {"token": token, "type": type}
            self.typed_identifiers.push(item)

    def add_current_token_to_identifier_stack(self):
        if not self.identifiers_stack.search(self.current_token['token']):
            self.identifiers_stack.push(self.current_token)
        else:
            raise Exception(self.format_error_message(
                "SemanticoError: variável " +
                self.current_token['token'] + " já foi declarada."
            ))

    def add_scope_mark(self):
        self.identifiers_stack.push({"token": "$", "type": "MARK"})
        self.typed_identifiers.push({"token": "$", "type": "MARK"})

    def get_next_token(self):
        if len(self.stack) > 0:
            self.current_token = self.stack.pop()
            logger.debug(self.current_token)
        else:
            raise Exception("EOF")

    def peek_next(self):
        if len(self.stack) > 0:
            token = self.stack.pop()
            self.stack.append(token)
            return token
        else:
            raise Exception("EOF")

    def compare_token(self, token_type, token_regex):
        return self.compare_token_type(token_type) \
            and self.compare_token_value(token_regex)

    def compare_token_value(self, token_regex):
        return re.match(token_regex, self.current_token['token'])

    def compare_token_type(self, token_type, token=None):
        token = self.current_token['type'] if token == None else token['type']
        return token == token_type

    def process_variables_declaration(self):
        if self.compare_token_value(TokenValueRegex.VAR):
            self.get_next_token()
            self.process_variables_list_declaration()

    def process_variables_list_declaration(self):
        identifiers = self.process_identifiers_list()
        if self.compare_token_value(TokenValueRegex.COLON):
            self.get_next_token()
            type = self.process_type()
            self.add_typed_identifiers(type, identifiers)
            self.typed_identifiers.print()

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
            identifiers = self.process_identifiers_list()
            if self.compare_token_value(TokenValueRegex.COLON):
                self.get_next_token()
                type = self.process_type()
                self.add_typed_identifiers(type, identifiers)
                self.typed_identifiers.print()

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

    def process_identifiers_list(self):
        identifiers_buffer = []
        if self.compare_token_type(TokenType.Identifier):
            self.add_current_token_to_identifier_stack()
            identifiers_buffer.append(self.current_token['token'])

            self.get_next_token()
            identifiers_buffer += self.process_identifiers_list_2()
            return identifiers_buffer
        else:
            raise Exception(self.format_error_message(
                'Erro: o programa espera um identificador válido.'))

    def process_identifiers_list_2(self):
        identifiers_buffer = []

        if self.compare_token_value(TokenValueRegex.COMMA):
            self.get_next_token()
            if self.compare_token_type(TokenType.Identifier):
                self.add_current_token_to_identifier_stack()
                identifiers_buffer.append(self.current_token['token'])

                self.get_next_token()
                identifiers_buffer += self.process_identifiers_list_2()
            else:
                raise Exception(self.format_error_message(
                    'Erro: o programa espera um identificador válido.'))
        return identifiers_buffer

    def process_sub_programs_declararion(self):
        if self.compare_token_value(TokenValueRegex.PROCEDURE):
            self.process_sub_program_declaration()

            if self.compare_token_value(TokenValueRegex.SEMICOLON):
                self.identifiers_stack.close_scope()
                self.typed_identifiers.close_scope()

                self.get_next_token()
                self.process_sub_programs_declararion_2()

            else:
                raise Exception('Delimitador ; esperado')

    def process_sub_programs_declararion_2(self):
        if self.compare_token(TokenType.Keyword, TokenValueRegex.PROCEDURE):
            self.process_sub_program_declaration()

            if self.compare_token(TokenType.Delimiter, TokenValueRegex.SEMICOLON):
                self.identifiers_stack.close_scope()
                self.typed_identifiers.close_scope()

                self.get_next_token()
                self.process_sub_programs_declararion_2()

            else:
                raise Exception('Delimitador ; esperado')

    def process_sub_program_declaration(self):
        if self.compare_token_value(TokenValueRegex.PROCEDURE):
            self.get_next_token()
            if self.compare_token_type(TokenType.Identifier):
                self.add_current_token_to_identifier_stack()
                self.typed_identifiers.push(
                    {"token": self.current_token['token'], "type": "PROCEDURE"})
                self.add_scope_mark()

                self.get_next_token()
                self.process_arguments()

                if self.compare_token_value(TokenValueRegex.SEMICOLON):
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

    def process_params_list(self):
        identifiers = self.process_identifiers_list()
        if self.compare_token_value(TokenValueRegex.COLON):
            self.get_next_token()
            type = self.process_type()
            self.add_typed_identifiers(type, identifiers)
            self.process_params_list_2()

        else:
            raise Exception(self.format_error_message(
                'Esperado ":" apos lista de identificadoers'))

    def process_params_list_2(self):
        if self.compare_token_value(TokenValueRegex.SEMICOLON):
            self.get_next_token()
            identifiers = self.process_identifiers_list()

            if self.compare_token_value(TokenValueRegex.COLON):
                self.get_next_token()
                type = self.process_type()
                self.add_typed_identifiers(type, identifiers)

                self.process_params_list_2()
            else:
                raise Exception(self.format_error_message(
                    'Esperado  ":" apos lista de identificadoers'))

    def process_compound_command(self):
        if self.compare_token_value(TokenValueRegex.BEGIN):
            self.get_next_token()
            self.optional_commands()

            if self.compare_token_value(TokenValueRegex.END):
                self.get_next_token()
            else:
                raise Exception(self.format_error_message(
                    'Comando composto deve acabar com end'))

        else:
            raise Exception(self.format_error_message(
                'Comando composto deve iniciar com begin'))

    def optional_commands(self):
        if self.compare_token_type(TokenType.Identifier) \
                or self.compare_token_value(TokenValueRegex.IF) \
                or self.compare_token_value(TokenValueRegex.WHILE) \
                or self.compare_token_value(TokenValueRegex.BEGIN):
            self.process_list_of_commands()

    def process_list_of_commands(self):
        self.process_command()
        self.process_list_of_commands_2()

    def process_list_of_commands_2(self):
        if self.compare_token_value(TokenValueRegex.SEMICOLON):
            self.get_next_token()
            self.process_command()
            self.process_list_of_commands_2()

    def process_command(self):
        if self.compare_token_type(TokenType.Identifier) and self.compare_token_type(TokenType.AttributionOperator, self.peek_next()):
            self.process_variable()

            if self.compare_token_type(TokenType.AttributionOperator):
                self.get_next_token()
                self.process_expression()

            self.verify_attribution()

        elif self.compare_token_type(TokenType.Identifier):
            self.process_procedure_activation()
        elif self.compare_token_value(TokenValueRegex.BEGIN):
            self.process_compound_command()
        elif self.compare_token_value(TokenValueRegex.IF):
            self.get_next_token()
            self.process_expression()

            if self.compare_token_value(TokenValueRegex.THEN):
                self.get_next_token()
                self.process_command()
                self.process_else()
            else:
                raise Exception(self.format_error_message(
                    '"then" esperado para o comando if.'))
        elif self.compare_token_value(TokenValueRegex.WHILE):
            self.get_next_token()
            self.process_expression()

            if self.compare_token_value(TokenValueRegex.DO):
                self.get_next_token()
                self.process_command()
            else:
                raise Exception(self.format_error_message(
                    '"do" esperado para o comando while.'))
        else:
            raise Exception(self.format_error_message(
                'comando esperado.'))

    def process_else(self):
        if self.compare_token_value(TokenValueRegex.ELSE):
            self.get_next_token()
            self.process_command()

    def process_variable(self):
        if self.compare_token_type(TokenType.Identifier):
            self.check_identifier_declaration(self.current_token['token'])

            self.search_identifier_and_add_to_pct(self.current_token['token'])

            self.get_next_token()
        else:
            raise Exception(self.format_error_message(
                'Variável esperado.'))

    def process_procedure_activation(self):
        if self.compare_token_type(TokenType.Identifier):
            self.check_identifier_declaration(self.current_token['token'])
            self.search_identifier_and_add_to_pct(self.current_token['token'])

            self.get_next_token()

            if self.compare_token_value(TokenValueRegex.OPEN_PARENTHESIS):
                self.get_next_token()
                self.process_list_of_expressions()

                if self.compare_token_value(TokenValueRegex.CLOSE_PARENTHESIS):
                    self.get_next_token()
                else:
                    raise Exception(self.format_error_message(
                        ') esperado.'))
        else:
            raise Exception(self.format_error_message(
                'Identificador esperado.'))

    def process_list_of_expressions(self):
        self.process_expression()
        self.process_list_of_expressions_2()

    def process_list_of_expressions_2(self):
        if self.compare_token_value(TokenValueRegex.COMMA):
            self.get_next_token()
            self.process_expression()
            self.process_list_of_expressions_2()

    def process_expression(self):
        self.process_simple_expression()

        if self.compare_token_value(TokenValueRegex.OP_RELATIONAL):
            self.process_op_relacional()
            self.process_simple_expression()

            self.verify_relational_expression()

    def process_simple_expression(self):
        if self.compare_token_value(TokenValueRegex.SINAL):
            self.process_sinal()

            self.process_term()
            self.process_simple_expression_2()
        else:
            self.process_term()
            self.process_simple_expression_2()

    def process_simple_expression_2(self):
        if self.compare_token_value(TokenValueRegex.OP_ADD):
            if self.compare_token_value(TokenValueRegex.SINAL):
                self.process_op_aditivo()
                self.process_term()
                self.process_simple_expression_2()
                self.verify_arithmetic_expression()
            elif self.compare_token_value(TokenValueRegex.OR):
                self.process_op_aditivo()
                self.process_term()
                self.process_simple_expression_2()
                self.verify_logic_expression()

    def process_term(self):
        self.process_fator()
        self.process_term_2()

    def process_term_2(self):
        if self.compare_token_value(TokenValueRegex.OP_MULTI):
            if self.compare_token_value(TokenValueRegex.OP_MULTI_SIGNAL):
                self.process_op_multiplicativo()
                self.process_fator()
                self.process_term_2()
                self.verify_arithmetic_expression()
            elif self.compare_token_value(TokenValueRegex.OP_MULTI_AND):
                self.process_op_multiplicativo()
                self.process_fator()
                self.process_term_2()
                self.verify_logic_expression()

    def process_fator(self):
        if self.compare_token_type(TokenType.Identifier):
            self.process_procedure_activation()

        elif self.compare_token_type(TokenType.Integer):
            self.get_next_token()
            self.pct.push("integer")

        elif self.compare_token_type(TokenType.RealNumber):
            self.get_next_token()
            self.pct.push("real")

        elif self.compare_token_value(TokenValueRegex.BOOLEAN):
            self.get_next_token()
            self.pct.push("boolean")

        elif self.compare_token_value(TokenValueRegex.OPEN_PARENTHESIS):
            self.get_next_token()
            self.process_expression()

            if self.compare_token_value(TokenValueRegex.CLOSE_PARENTHESIS):
                self.get_next_token()
            else:
                raise Exception(self.format_error_message(
                    ') esperado.'))

        elif self.compare_token_value(TokenValueRegex.NOT):
            self.pct.push("boolean")
            self.get_next_token()
            self.process_fator()

        else:
            raise Exception('Fator esperado.')

    def process_sinal(self):
        if self.compare_token_value(TokenValueRegex.SINAL):
            self.get_next_token()
        else:
            raise Exception(self.format_error_message(
                'Sinal esperado'))

    def process_op_relacional(self):
        if self.compare_token_value(TokenValueRegex.OP_RELATIONAL):
            self.get_next_token()
        else:
            raise Exception(self.format_error_message(
                'Operador relacional esperado.'))

    def process_op_aditivo(self):
        if self.compare_token_value(TokenValueRegex.OP_ADD):
            self.get_next_token()
        else:
            raise Exception(self.format_error_message(
                'Operador aditivo esperado.'))

    def process_op_multiplicativo(self):
        if self.compare_token_value(TokenValueRegex.OP_MULTI):
            self.get_next_token()
        else:
            raise Exception(self.format_error_message(
                'Operador multiplicativo esperado.'))

    def process_type(self):
        if self.compare_token_value(TokenValueRegex.VAR_TYPE):
            type = self.current_token['token']
            self.get_next_token()
            return type
        else:
            raise Exception(self.format_error_message(
                'Tipo de variável não permitido.'))

    def verify_arithmetic_expression(self):
        top = self.pct.pop()
        sub_top = self.pct.pop()

        if top == "integer" and sub_top == "integer":
            self.pct.push('integer')

        elif top == "real" and sub_top == "real":
            self.pct.push('real')

        elif top == "integer" and sub_top == "real":
            self.pct.push('real')

        elif top == "real" and sub_top == "integer":
            self.pct.push('real')

        else:
            raise Exception(self.format_error_message(
                "Tipos incompatíveis da operação aritmética."
            ))

    def verify_relational_expression(self):
        top = self.pct.pop()
        sub_top = self.pct.pop()
        allowed_types = ['integer', 'real']

        if top in allowed_types and sub_top in allowed_types:
            self.pct.push('boolean')

        else:
            raise Exception(self.format_error_message(
                "Tipos incompatíveis da operação relacional"
            ))

    def verify_logic_expression(self):
        top = self.pct.pop()
        sub_top = self.pct.pop()

        if top == sub_top:
            self.pct.push('boolean')
        else:
            raise Exception(self.format_error_message(
                "Tipos incompatíveis da operação lógica"
            ))

    def verify_attribution(self):
        self.pct.print()
        top = self.pct.pop()
        new_top = self.pct.peekTop()

        if top == "integer" and new_top == "real":
            self.pct.pop()
        elif self.pct.peekTop() == top:
            self.pct.pop()
        else:
            raise Exception(self.format_error_message(
                "Tipos incompatíveis na atribuição."
            ))

    def process(self, token_table):
        self.stack = list(reversed(token_table))
        self.get_next_token()

        if self.compare_token(TokenType.Keyword, TokenValueRegex.PROGRAM):
            self.add_scope_mark()
            self.get_next_token()

            if self.compare_token_type(TokenType.Identifier):
                self.identifiers_stack.push(self.current_token)
                self.typed_identifiers.push(
                    {"token": self.current_token["token"], "type": "PROGRAM"})
                self.get_next_token()

                if self.compare_token_value(TokenValueRegex.SEMICOLON):
                    self.get_next_token()
                    self.process_variables_declaration()
                    self.process_sub_programs_declararion()
                    self.process_compound_command()

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


def runSyntacticAnalysis(data):
    if "error" in data:
        raise Exception("LexicoError: Ocorreu um erro no analisador lexico.")
    return SyntacticAnalyzer().process(data['symbol_table'])


def runSyntacticAnalysisFromFile(path, relative_path=False):
    data = get_symbol_table(path, relative_path)
    return runSyntacticAnalysis(data)


if __name__ == '__main__':
    # Testes rapidos...
    logging.basicConfig(level=logging.DEBUG)
    logger.debug("Sintatico")

    base_path = pathlib.Path(__file__).parent.resolve()
    file_name = 'Test4.pas'
    if '-name' in sys.argv:
        file_name = sys.argv[sys.argv.index('-name') + 1]
    file_path = path.join(base_path, '../pascal_sources', file_name)

    data = lexico.build_symbol_table(
        file_path, True)

    res = runSyntacticAnalysis(data)

    if res is None:
        logger.debug('Compilado com sucesso')

    else:
        logger.error(json.dumps(res, indent=2))
