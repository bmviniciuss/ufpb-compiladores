from os import sysconf_names
from compiler.sintatico import SyntacticAnalyzer
from compiler.lexico import TokenReader


def test_variable_declaration():
    src_code = """
    program Test;
    var
        X, A, B : integer;
    begin
    end.
    """

    sym_table = TokenReader().process(src_code)['symbol_table']
    SyntacticAnalyzer().process(sym_table)
