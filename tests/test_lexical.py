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


def test_test2_code():
    actual = build_symbol_table('Test2.pas')
    expected = [
        {
            "token": "program",
            "type": TokenType.Keyword,
            "line": 1
        },
        {
            "token": "Test2",
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
            "token": "X",
            "type": TokenType.Identifier,
            "line": 3
        },
        {
            "token": ",",
            "type": TokenType.Delimiter,
            "line": 3
        },
        {
            "token": "A",
            "type": TokenType.Identifier,
            "line": 3
        },
        {
            "token": ",",
            "type": TokenType.Delimiter,
            "line": 3
        },
        {
            "token": "B",
            "type": TokenType.Identifier,
            "line": 3
        },
        {
            "token": ":",
            "type": TokenType.Delimiter,
            "line": 3
        },
        {
            "token": "integer",
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
            "token": "A",
            "type": TokenType.Identifier,
            "line": 5
        },
        {
            "token": ":=",
            "type": TokenType.AttributionOperator,
            "line": 5
        },
        {
            "token": "5",
            "type": TokenType.Number,
            "line": 5
        },
        {
            "token": ";",
            "type": TokenType.Delimiter,
            "line": 5
        },
        {
            "token": "B",
            "type": TokenType.Identifier,
            "line": 6
        },
        {
            "token": ":=",
            "type": TokenType.AttributionOperator,
            "line": 6
        },
        {
            "token": "10",
            "type": TokenType.Number,
            "line": 6
        },
        {
            "token": ";",
            "type": TokenType.Delimiter,
            "line": 6
        },
        {
            "token": "if",
            "type": TokenType.Keyword,
            "line": 7
        },
        {
            "token": "(",
            "type": TokenType.Delimiter,
            "line": 7
        },
        {
            "token": "A",
            "type": TokenType.Identifier,
            "line": 7
        },
        {
            "token": ">",
            "type": TokenType.ComparisonOperator,
            "line": 7
        },
        {
            "token": "B",
            "type": TokenType.Identifier,
            "line": 7
        },
        {
            "token": ")",
            "type": TokenType.Delimiter,
            "line": 7
        },
        {
            "token": "then",
            "type": TokenType.Keyword,
            "line": 7
        },
        {
            "token": "begin",
            "type": TokenType.Keyword,
            "line": 8
        },
        {
            "token": "X",
            "type": TokenType.Identifier,
            "line": 9
        },
        {
            "token": ":=",
            "type": TokenType.AttributionOperator,
            "line": 9
        },
        {
            "token": "A",
            "type": TokenType.Identifier,
            "line": 9
        },
        {
            "token": ";",
            "type": TokenType.Delimiter,
            "line": 9
        },
        {
            "token": "A",
            "type": TokenType.Identifier,
            "line": 10
        },
        {
            "token": ":=",
            "type": TokenType.AttributionOperator,
            "line": 10
        },
        {
            "token": "B",
            "type": TokenType.Identifier,
            "line": 10
        },
        {
            "token": ";",
            "type": TokenType.Delimiter,
            "line": 10
        },
        {
            "token": "B",
            "type": TokenType.Identifier,
            "line": 11
        },
        {
            "token": ":=",
            "type": TokenType.AttributionOperator,
            "line": 11
        },
        {
            "token": "X",
            "type": TokenType.Identifier,
            "line": 11
        },
        {
            "token": "end",
            "type": TokenType.Keyword,
            "line": 12
        },
        {
            "token": "end",
            "type": TokenType.Keyword,
            "line": 13
        },
        {
            "token": ".",
            "type": TokenType.Delimiter,
            "line": 13
        }
    ]

    assert actual == expected


def test_test3_code():
    actual = build_symbol_table('Test3.pas')
    expected = [
        {
            "token": "program",
            "type": TokenType.Keyword,
            "line": 1
        },
        {
            "token": "Test3",
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
            "token": "NUMERO",
            "type": TokenType.Identifier,
            "line": 3
        },
        {
            "token": ":",
            "type": TokenType.Delimiter,
            "line": 3
        },
        {
            "token": "integer",
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
            "token": "NUMERO",
            "type": TokenType.Identifier,
            "line": 5
        },
        {
            "token": "=",
            "type": TokenType.ComparisonOperator,
            "line": 5
        },
        {
            "token": "-",
            "type": TokenType.ArithmeticOperator,
            "line": 5
        },
        {
            "token": "3",
            "type": TokenType.Number,
            "line": 5
        },
        {
            "token": "*",
            "type": TokenType.ArithmeticOperator,
            "line": 5
        },
        {
            "token": "5",
            "type": TokenType.Number,
            "line": 5
        },
        {
            "token": "+",
            "type": TokenType.ArithmeticOperator,
            "line": 5
        },
        {
            "token": "7",
            "type": TokenType.Number,
            "line": 5
        },
        {
            "token": "-",
            "type": TokenType.ArithmeticOperator,
            "line": 5
        },
        {
            "token": "9",
            "type": TokenType.Number,
            "line": 5
        },
        {
            "token": ";",
            "type": TokenType.Delimiter,
            "line": 5
        },
        {
            "token": "if",
            "type": TokenType.Keyword,
            "line": 6
        },
        {
            "token": "(",
            "type": TokenType.Delimiter,
            "line": 6
        },
        {
            "token": "NUMERO",
            "type": TokenType.Identifier,
            "line": 6
        },
        {
            "token": ">=",
            "type": TokenType.ComparisonOperator,
            "line": 6
        },
        {
            "token": "20",
            "type": TokenType.Number,
            "line": 6
        },
        {
            "token": ")",
            "type": TokenType.Delimiter,
            "line": 6
        },
        {
            "token": "and",
            "type": TokenType.Identifier,
            "line": 6
        },
        {
            "token": "(",
            "type": TokenType.Delimiter,
            "line": 6
        },
        {
            "token": "NUMERO",
            "type": TokenType.Identifier,
            "line": 6
        },
        {
            "token": "<=",
            "type": TokenType.ComparisonOperator,
            "line": 6
        },
        {
            "token": "90",
            "type": TokenType.Number,
            "line": 6
        },
        {
            "token": ")",
            "type": TokenType.Delimiter,
            "line": 6
        },
        {
            "token": "then",
            "type": TokenType.Keyword,
            "line": 6
        },
        {
            "token": "NUMERO",
            "type": TokenType.Identifier,
            "line": 7
        },
        {
            "token": "=",
            "type": TokenType.ComparisonOperator,
            "line": 7
        },
        {
            "token": "10",
            "type": TokenType.Number,
            "line": 7
        },
        {
            "token": "*",
            "type": TokenType.ArithmeticOperator,
            "line": 7
        },
        {
            "token": "3",
            "type": TokenType.Number,
            "line": 7
        },
        {
            "token": "else",
            "type": TokenType.Keyword,
            "line": 8
        },
        {
            "token": "NUMERO",
            "type": TokenType.Identifier,
            "line": 8
        },
        {
            "token": "=",
            "type": TokenType.ComparisonOperator,
            "line": 8
        },
        {
            "token": "10",
            "type": TokenType.Number,
            "line": 8
        },
        {
            "token": "/",
            "type": TokenType.ArithmeticOperator,
            "line": 8
        },
        {
            "token": "3",
            "type": TokenType.Number,
            "line": 8
        },
        {
            "token": "end",
            "type": TokenType.Keyword,
            "line": 9
        },
        {
            "token": ".",
            "type": TokenType.Delimiter,
            "line": 9
        }
    ]

    assert actual == expected


def test_test4_code():
    actual = build_symbol_table('Test4.pas')
    expected = []

    assert actual == expected


def test_test5_code():
    actual = build_symbol_table('Test5.pas')
    expected = []

    assert actual == expected
