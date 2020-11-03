from compiler.lexico import TokenReader, get_sym_table
from compiler.sintatico import SyntacticAnalyzer
from os import sysconf_names
from compiler.combinators import Unit, sequence
from compiler.sintatico2 import abre_parentesis, epsilon, choice, expressao_simples, termo, fator


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

    result = parser(sym_table)
    assert result == []


def test_fator():
    src_code = """
    1.3
    10
    true
    false
    not
    """
    sym_table = get_sym_table(src_code)

    parser = sequence(
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

    f = sequence(add, multi)

    xs = [1, 2]
    y = f(xs)

    assert y[0] == 4


def test_compose_associative():
    result = 0

    def f(xs):
        nonlocal result
        result += 1
        return xs[1:]

    def g(xs):
        nonlocal result
        result *= 2
        return xs[1:]

    def h(xs):
        nonlocal result
        result += 3
        return xs[1:]

    k_1 = sequence(sequence(f, g), h)
    k_2 = sequence(f, sequence(g, h))

    result = 0
    x = [0, 0, 0]

    res = k_1(x)  # handled all items
    assert res == []
    assert result == 5  # had the desired effects

    result = 0
    x = [0, 0, 0]

    assert k_2(x) == []  # handled all items
    assert result == 5  # had the desired effects


def test_compose_empty_left():
    # Only way compose(...fs) returns non eof for an empty input is if
    # all links are units
    def f(_): return Unit([])
    def g(_): return Unit([])

    assert sequence(f, g)([]) == []

    def f_2(_): return []
    def g_2(_): return Unit([])
    assert sequence(f_2, g_2)([]) == 'EOF'

    def f_3(_): return []
    def g_3(_): return []
    assert sequence(f_3, g_3)([]) == 'EOF'

    def f_4(_): return Unit([])
    def g_4(_): return []
    assert sequence(f_4, g_4)([]) == 'EOF'


def test_compose_empty_inner_left():
    def f(_): return []
    def g(_): return Unit([])

    assert sequence(f, g)([1]) == []

    def g_2(_): return []

    assert sequence(f, g_2)([1]) == 'EOF'


def test_choice_unit():
    def f(buffer): return buffer[1:]
    def g(buffer): return buffer[1:]

    buffer = [1]
    k = sequence(f, g)
    k_2 = choice(k, epsilon)

    assert k(buffer) == 'EOF'
    assert k_2(buffer).unwrap() == [1]


def test_choice():
    def f(buffer): return buffer[1:]
    def g(buffer): return buffer[1:]

    buffer = [1]
    good_chain = f
    bad_chain = sequence(f, g)

    parser = choice(bad_chain, good_chain)

    assert parser(buffer) == []

    parser = choice(bad_chain)

    assert parser(buffer) == 'EOF'
