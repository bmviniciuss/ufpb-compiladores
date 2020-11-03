from compiler.combinators import choice, compose
from functools import reduce
from logging import error
from compiler.utils import get_symbol_table, head_value, head_type
from compiler.types import TokenType, TokenValueRegex
from compiler.lexico import TokenReader, get_sym_table
import logging
import pprint
import re
import coloredlogs


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False

coloredlogs.install(level=logging.DEBUG, logger=logger)


# Gramatica

# Terminais

def fator(buffer):
    if head_type(buffer, TokenType.RealNumber):
        logger.debug('Fator: Numero real')
        return buffer
    if head_type(buffer, TokenType.Integer):
        logger.debug('Fator: Numero inteiro')
        return buffer
    if head_value(buffer, TokenValueRegex.BOOLEAN):
        logger.debug('Fator: Boolean')
        return buffer
    if head_value(buffer, TokenValueRegex.NOT):
        logger.debug('Fator: Negacao')
        return buffer

    return 'Fator invalido'


def abre_parentesis(buffer):
    if head_value(buffer, TokenValueRegex.OPEN_PARENTHESIS):
        logger.debug('Abre parentesis')
        return buffer

    return 'Abre parentesis esperado'


def fecha_parentesis(buffer):
    if head_value(buffer, TokenValueRegex.CLOSE_PARENTHESIS):
        logger.debug('Fecha parentesis')
        return buffer

    return 'Fecha parentesis esperado'


def sinal(buffer):
    if head_value(buffer, TokenValueRegex.SINAL):
        return buffer

    return 'Sinal invalido %s' % buffer[0]['token']


def epsilon(buffer):
    return tuple([buffer])


def op_aditivo(buffer):
    if head_value(buffer, TokenValueRegex.OP_ADD):
        return buffer

    return 'operador aditivo esperado'


def op_multiplicativo(buffer):
    if head_value(buffer, TokenValueRegex.OP_MULTI):
        return buffer

    return 'Operador operador multiplicativo esperado'


def end_of_file(buffer):
    if head_value(buffer, r'\.'):
        return []

    return '\".\" esperado'

# Expressoes


def expressao_simples(buffer):
    return choice(
        compose(termo, expressao_simples2),
        compose(sinal, termo, expressao_simples2)
    )(buffer)


def expressao_simples2(buffer):
    return choice(
        compose(op_aditivo, termo, expressao_simples2),
        epsilon
    )(buffer)


def termo(buffer):
    res = compose(
        fator,
        termo2
    )(buffer)

    return res


def termo2(buffer):
    return choice(
        compose(op_multiplicativo, fator, termo2),
        epsilon
    )(buffer)


if __name__ == '__main__':
    src_code = """
    - 3 * 5 + 7 - 9"""

    src_code = """
    1 + 1 * 2  .
    """

    sym_table = get_sym_table(src_code)
    pprint.pprint(sym_table)

    # Testes rapidos...
    parser = compose(
        expressao_simples,
        end_of_file
    )

    res = parser(sym_table)

    if type(res) == str:
        logger.error(res)

    if type(res) == tuple:
        res = res[0]

    if type(res) == list and len(res) > 0:
        logger.error('Failed parsing token %s' % res[0]['token'])

    else:
        logger.info('Compiled successfully')
