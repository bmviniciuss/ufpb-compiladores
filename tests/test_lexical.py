from compiler.lexico import TokenReader, build_symbol_table, TokenType
import json


def test_basic_attribution():
    actual = TokenReader().process(
        'Area := 3.14 * Raio * Raio;')

    expected = [
        {
            "token": "Area",
            "type": TokenType.Identifier,
            "line": 1
        },
        {
            "token": ":=",
            "type": TokenType.AttributionOperator,
            "line": 1
        },
        {
            "token": "3.14",
            "type": TokenType.Number,
            "line": 1
        },
        {
            "token": "*",
            "type": TokenType.ArithmeticOperator,
            "line": 1
        },
        {
            "token": "Raio",
            "type": TokenType.Identifier,
            "line": 1
        },
        {
            "token": "*",
            "type": TokenType.ArithmeticOperator,
            "line": 1
        },
        {
            "token": "Raio",
            "type": TokenType.Identifier,
            "line": 1
        },
        {
            "token": ";",
            "type": TokenType.Delimiter,
            "line": 1
        }
    ]

    assert actual == expected


def test_multiline_declaration():
    src_code = '''
       var
        Area, Comprimento, Raio : real;
    '''

    actual = TokenReader().process(src_code)
    expected = [
        {
            "token": "var",
            "type": TokenType.Keyword,
            "line": 1
        },
        {
            "token": "Area",
            "type": TokenType.Identifier,
            "line": 2
        },
        {
            "token": ",",
            "type": TokenType.Delimiter,
            "line": 2
        },
        {
            "token": "Comprimento",
            "type": TokenType.Identifier,
            "line": 2
        },
        {
            "token": ",",
            "type": TokenType.Delimiter,
            "line": 2
        },
        {
            "token": "Raio",
            "type": TokenType.Identifier,
            "line": 2
        },
        {
            "token": ":",
            "type": TokenType.Delimiter,
            "line": 2
        },
        {
            "token": "real",
            "type": TokenType.Keyword,
            "line": 2
        },
        {
            "token": ";",
            "type": TokenType.Delimiter,
            "line": 2
        }
    ]

    assert actual == expected


def test_parse_id_with_numbers():
    src_code = 'program Test1;'
    actual = TokenReader().process(src_code)
    expected = [
        {
            "token": "program",
            "type": TokenType.Keyword,
            "line": 1
        },
        {
            "token": "Test1",
            "type": TokenType.Identifier,
            "line": 1
        }, {
            "token": ";",
            "type": TokenType.Delimiter,
            "line": 1
        }]

    assert actual == expected


def test_test1_code():
    actual = build_symbol_table('Test1_sem_erro.pas')

    expected = [
        {
            "token": "program",
            "type": TokenType.Keyword,
            "line": 1
        },
        {
            "token": "Test1",
            "type": TokenType.Identifier,
            "line": 1
        },
        {
            "token": ";",
            "type": TokenType.Delimiter,
            "line": 1
        },
        {
            "token": "var",
            "type": TokenType.Keyword,
            "line": 2
        },
        {
            "token": "Area",
            "type": TokenType.Identifier,
            "line": 3
        },
        {
            "token": ",",
            "type": TokenType.Delimiter,
            "line": 3
        },
        {
            "token": "Comprimento",
            "type": TokenType.Identifier,
            "line": 3
        },
        {
            "token": ",",
            "type": TokenType.Delimiter,
            "line": 3
        },
        {
            "token": "Raio",
            "type": TokenType.Identifier,
            "line": 3
        },
        {
            "token": ":",
            "type": TokenType.Delimiter,
            "line": 3
        },
        {
            "token": "real",
            "type": TokenType.Keyword,
            "line": 3
        },
        {
            "token": ";",
            "type": TokenType.Delimiter,
            "line": 3
        },
        {
            "token": "begin",
            "type": TokenType.Keyword,
            "line": 4
        },
        {
            "token": "Raio",
            "type": TokenType.Identifier,
            "line": 5
        },
        {
            "token": ":=",
            "type": TokenType.AttributionOperator,
            "line": 5
        },
        {
            "token": "4",
            "type": TokenType.Number,
            "line": 5
        },
        {
            "token": ";",
            "type": TokenType.Delimiter,
            "line": 5
        },
        {
            "token": "Area",
            "type": TokenType.Identifier,
            "line": 6
        },
        {
            "token": ":=",
            "type": TokenType.AttributionOperator,
            "line": 6
        },
        {
            "token": "3.14",
            "type": TokenType.Number,
            "line": 6
        },
        {
            "token": "*",
            "type": TokenType.ArithmeticOperator,
            "line": 6
        },
        {
            "token": "Raio",
            "type": TokenType.Identifier,
            "line": 6
        },
        {
            "token": "*",
            "type": TokenType.ArithmeticOperator,
            "line": 6
        },
        {
            "token": "Raio",
            "type": TokenType.Identifier,
            "line": 6
        },
        {
            "token": ";",
            "type": TokenType.Delimiter,
            "line": 6
        },
        {
            "token": "Comprimento",
            "type": TokenType.Identifier,
            "line": 7
        },
        {
            "token": ":=",
            "type": TokenType.AttributionOperator,
            "line": 7
        },
        {
            "token": "2",
            "type": TokenType.Number,
            "line": 7
        },
        {
            "token": "*",
            "type": TokenType.ArithmeticOperator,
            "line": 7
        },
        {
            "token": "3.14",
            "type": TokenType.Number,
            "line": 7
        },
        {
            "token": "*",
            "type": TokenType.ArithmeticOperator,
            "line": 7
        },
        {
            "token": "Raio",
            "type": TokenType.Identifier,
            "line": 7
        },
        {
            "token": "end",
            "type": TokenType.Keyword,
            "line": 8
        },
        {
            "token": ".",
            "type": TokenType.Delimiter,
            "line": 8
        }
    ]

    assert actual == expected
