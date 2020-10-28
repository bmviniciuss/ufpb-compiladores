from compiler.sintatico2 import abre_parentesis, choice, epsilon, expressao_simples, termo
from os import sysconf_names
from compiler.sintatico import SyntacticAnalyzer
from compiler.lexico import TokenReader, get_sym_table


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
