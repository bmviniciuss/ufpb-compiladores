from compiler.utils import get_symbol_table
from compiler.types import TokenType
import logging
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PROGRAM_KEYWORD = "program"


class SyntacticAnalyzer():
    def __init__(self):
        self.current_token = ""
        self.stack = []

    def compare_token(self, token_type, token):
        return self.current_token['type'] == token_type \
            and token == self.current_token['token']

    def compare_token_type(self, token_type):
        return self.current_token['type'] == token_type

    def process_compound_command(self):
        pass

    def process_sub_programs_declararion(self):
        pass

    def process_variables_declaration(self):
        pass

    def process(self, token_table):
        self.stack = list(reversed(token_table))
        data = {}

        while len(self.stack) > 0:
            self.current_token = self.stack.pop()
            logger.debug(self.current_token)
            if self.compare_token(TokenType.Keyword, PROGRAM_KEYWORD):
                self.current_token = self.stack.pop()

                if self.compare_token_type(TokenType.Identifier):
                    self.current_token = self.stack.pop()

                    if self.compare_token(TokenType.Delimiter, ';'):
                        self.current_token = self.stack.pop()
                        self.process_variables_declaration()
                        self.process_sub_programs_declararion()
                        self.process_compound_command()

                        if not self.compare_token(TokenType.Delimiter, '.'):
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
