from compiler.lexico import TokenReader, get_sym_table
from compiler.sintatico import SyntacticAnalyzer
from os import sysconf_names
from compiler.combinators import compose
from compiler.sintatico2 import abre_parentesis, choice, epsilon, expressao_simples, termo, fator


def test_epsilon_choice():
    src_code = """
    12123
    """

    sym_table = get_sym_table(src_code)

    # Epson passes by itself
    parser = epsilon
    assert type(parser(sym_table)) != str

    # Parentesis parser fails by itself
    parser = abre_parentesis
    assert type(parser(sym_table)) == str

    # Choice between both passes
    parser = choice(abre_parentesis, epsilon)
    assert type(parser(sym_table)) != str


def test_choice_recursive_epsilon():
    src_code = """
    12123 .
    """
    sym_table = get_sym_table(src_code)

    # Choice with recursive branch works
    parser = choice(expressao_simples, epsilon)
    assert type(parser(sym_table)) != str


def test_termo():
    src_code = """
    12123
    """
    sym_table = get_sym_table(src_code)

    # Choice with recursive branch works
    parser = termo
    assert type(parser(sym_table)) != str


def test_fator():
    src_code = """
    1.3
    10
    true
    false
    not
    """
    sym_table = get_sym_table(src_code)

    parser = compose(
        fator,
        fator,
        fator,
        fator,
        fator
    )

    result = parser(sym_table)

    assert type(result) != str
    assert len(result) == 0


def test_compose():
    def add(x): return [x[0]+1, x[1]]
    def multi(x): return [x[0]*2]

    f = compose(add, multi)

    xs = [1, 2]
    y = f(xs)

    assert y[0] == 4
