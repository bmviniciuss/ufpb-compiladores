from functools import reduce
from logging import error
from compiler.utils import get_symbol_table
from compiler.types import TokenType, TokenValueRegex
from compiler.lexico import TokenReader, get_sym_table
import logging
import pprint
import re
import coloredlogs


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False

coloredlogs.install(level=logging.INFO, logger=logger)

DONE = -1

INDENT = 0
INDENT_SEQ = '--'

# Gramatica

# Terminais


def compose_one(parser_a, parser_b):
    global INDENT

    idt = INDENT
    INDENT += 1

    name = '%s %s' % (parser_a.__name__,
                      parser_b.__name__)

    def parser_c(buffer):
        logger.info('%s%s' % (idt * INDENT_SEQ, name))

        res_1 = parser_a(buffer)
        logger.info('%s%s' % ((idt + 1) * INDENT_SEQ, parser_a.__name__))

        # Expected eof
        if res_1 == DONE:
            return DONE

        # First errored
        if type(res_1) == str:
            return res_1

        if type(res_1) == tuple:
            res_1 = res_1[0]
        else:
            res_1 = res_1[1:]

        res_2 = parser_b(res_1)
        logger.info('%s%s' % ((idt + 1) * INDENT_SEQ, parser_b.__name__))

        # Expected eof
        if res_2 == DONE:
            return DONE

        # Second errored
        if type(res_2) == str:
            return res_2

        return res_2

    parser_c.__name__ = name

    return parser_c


def compose(*parsers):
    return reduce(lambda curr, acc: compose_one(curr, acc), list(parsers))


def choice(*parsers):
    def choose(buffer):
        seq = map(lambda parser: parser(buffer), parsers)

        for _ in range(len(list(parsers))):
            try:
                res = next(seq)
                if type(res) != str:
                    return res
            except IndexError:
                continue

        return 'Token invalid: \"%s\"' % buffer[0]['token']

    choose.__name__ = ' | '.join([item.__name__ for item in list(parsers)])

    return choose


def head_type(buffer, t):
    if not len(buffer) > 0:
        return False

    return buffer[0]['type'] == t


def head_value(buffer, pattern):
    if not len(buffer) > 0:
        return False

    return re.match(pattern, buffer[0]['token'])


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


def expressao_simples(buffer):
    return choice(
        compose(termo, expressao_simples2),
        compose(sinal, termo, expressao_simples2)
    )(buffer)


def sinal(buffer):
    if head_value(buffer, TokenValueRegex.SINAL):
        return buffer

    return 'Sinal invalido %s' % buffer[0]['token']


def epsilon(buffer):
    return tuple([buffer])


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


def op_aditivo(buffer):
    if head_value(buffer, TokenValueRegex.OP_ADD):
        return buffer

    return 'operador aditivo esperado'


def op_multiplicativo(buffer):
    if head_value(buffer, TokenValueRegex.OP_MULTI):
        return buffer

    return 'Operador operador multiplicativo esperado'


# Utils


def end_of_file(buffer):
    if head_value(buffer, '\.'):
        return DONE

    return '\".\" esperado'


if __name__ == '__main__':
    src_code = """
    - 3 * 5 + 7 - 9"""

    src_code = """
    1 + 1 * 2 + program 
    """

    sym_table = get_sym_table(src_code)
    pprint.pprint(sym_table)

    # Testes rapidos...
    logging.basicConfig(level=logging.INFO)

    parser = expressao_simples

    res = parser(sym_table)

    if type(res) == str:
        logger.error(res)

    if type(res) == tuple:
        res = res[0]

    if type(res) == list and len(res) > 0:
        logger.error('Failed parsing token %s' % res[0]['token'])

    else:
        logger.info('Compiled successfully')
