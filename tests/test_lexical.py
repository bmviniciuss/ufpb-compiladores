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
    expected = [
        {
            "token": "program",
            "type": "Keyword",
            "line": 1
        },
        {
            "token": "Test4",
            "type": "Identifier",
            "line": 1
        },
        {
            "token": ";",
            "type": "Delimiter",
            "line": 1
        },
        {
            "token": "var",
            "type": "Keyword",
            "line": 2
        },
        {
            "token": "A",
            "type": "Identifier",
            "line": 3
        },
        {
            "token": ",",
            "type": "Delimiter",
            "line": 3
        },
        {
            "token": "B",
            "type": "Identifier",
            "line": 3
        },
        {
            "token": ",",
            "type": "Delimiter",
            "line": 3
        },
        {
            "token": "R",
            "type": "Identifier",
            "line": 3
        },
        {
            "token": ",",
            "type": "Delimiter",
            "line": 3
        },
        {
            "token": "I",
            "type": "Identifier",
            "line": 3
        },
        {
            "token": ":",
            "type": "Delimiter",
            "line": 3
        },
        {
            "token": "integer",
            "type": "Keyword",
            "line": 3
        },
        {
            "token": ";",
            "type": "Delimiter",
            "line": 3
        },
        {
            "token": "procedure",
            "type": "Keyword",
            "line": 5
        },
        {
            "token": "teste",
            "type": "Identifier",
            "line": 5
        },
        {
            "token": "(",
            "type": "Delimiter",
            "line": 5
        },
        {
            "token": "A",
            "type": "Identifier",
            "line": 5
        },
        {
            "token": ":",
            "type": "Delimiter",
            "line": 5
        },
        {
            "token": "integer",
            "type": "Keyword",
            "line": 5
        },
        {
            "token": ",",
            "type": "Delimiter",
            "line": 5
        },
        {
            "token": "B",
            "type": "Identifier",
            "line": 5
        },
        {
            "token": ":",
            "type": "Delimiter",
            "line": 5
        },
        {
            "token": "real",
            "type": "Keyword",
            "line": 5
        },
        {
            "token": ")",
            "type": "Delimiter",
            "line": 5
        },
        {
            "token": ";",
            "type": "Delimiter",
            "line": 5
        },
        {
            "token": "var",
            "type": "Keyword",
            "line": 6
        },
        {
            "token": "S",
            "type": "Identifier",
            "line": 7
        },
        {
            "token": ",",
            "type": "Delimiter",
            "line": 7
        },
        {
            "token": "X",
            "type": "Identifier",
            "line": 7
        },
        {
            "token": ":",
            "type": "Delimiter",
            "line": 7
        },
        {
            "token": "real",
            "type": "Keyword",
            "line": 7
        },
        {
            "token": ";",
            "type": "Delimiter",
            "line": 7
        },
        {
            "token": "begin",
            "type": "Keyword",
            "line": 8
        },
        {
            "token": "S",
            "type": "Identifier",
            "line": 9
        },
        {
            "token": ":=",
            "type": "AttributionOperator",
            "line": 9
        },
        {
            "token": "A",
            "type": "Identifier",
            "line": 9
        },
        {
            "token": "+",
            "type": "ArithmeticOperator",
            "line": 9
        },
        {
            "token": "B",
            "type": "Identifier",
            "line": 9
        },
        {
            "token": "*",
            "type": "ArithmeticOperator",
            "line": 9
        },
        {
            "token": "X",
            "type": "Identifier",
            "line": 9
        },
        {
            "token": "end",
            "type": "Keyword",
            "line": 10
        },
        {
            "token": "begin",
            "type": "Keyword",
            "line": 12
        },
        {
            "token": "while",
            "type": "Keyword",
            "line": 13
        },
        {
            "token": "(",
            "type": "Delimiter",
            "line": 13
        },
        {
            "token": "I",
            "type": "Identifier",
            "line": 13
        },
        {
            "token": "<=",
            "type": "ComparisonOperator",
            "line": 13
        },
        {
            "token": "5",
            "type": "Number",
            "line": 13
        },
        {
            "token": ")",
            "type": "Delimiter",
            "line": 13
        },
        {
            "token": "do",
            "type": "Keyword",
            "line": 13
        },
        {
            "token": "begin",
            "type": "Keyword",
            "line": 14
        },
        {
            "token": "A",
            "type": "Identifier",
            "line": 15
        },
        {
            "token": ":=",
            "type": "AttributionOperator",
            "line": 15
        },
        {
            "token": "A",
            "type": "Identifier",
            "line": 15
        },
        {
            "token": "+",
            "type": "ArithmeticOperator",
            "line": 15
        },
        {
            "token": "1",
            "type": "Number",
            "line": 15
        },
        {
            "token": ";",
            "type": "Delimiter",
            "line": 15
        },
        {
            "token": "B",
            "type": "Identifier",
            "line": 16
        },
        {
            "token": ":=",
            "type": "AttributionOperator",
            "line": 16
        },
        {
            "token": "B",
            "type": "Identifier",
            "line": 16
        },
        {
            "token": "-",
            "type": "ArithmeticOperator",
            "line": 16
        },
        {
            "token": "1",
            "type": "Number",
            "line": 16
        },
        {
            "token": ";",
            "type": "Delimiter",
            "line": 16
        },
        {
            "token": "R",
            "type": "Identifier",
            "line": 17
        },
        {
            "token": ":=",
            "type": "AttributionOperator",
            "line": 17
        },
        {
            "token": "A",
            "type": "Identifier",
            "line": 17
        },
        {
            "token": "+",
            "type": "ArithmeticOperator",
            "line": 17
        },
        {
            "token": "B",
            "type": "Identifier",
            "line": 17
        },
        {
            "token": ";",
            "type": "Delimiter",
            "line": 17
        },
        {
            "token": "I",
            "type": "Identifier",
            "line": 18
        },
        {
            "token": ":=",
            "type": "AttributionOperator",
            "line": 18
        },
        {
            "token": "I",
            "type": "Identifier",
            "line": 18
        },
        {
            "token": "+",
            "type": "ArithmeticOperator",
            "line": 18
        },
        {
            "token": "1",
            "type": "Number",
            "line": 18
        },
        {
            "token": "end",
            "type": "Keyword",
            "line": 19
        },
        {
            "token": "end",
            "type": "Keyword",
            "line": 20
        },
        {
            "token": ".",
            "type": "Delimiter",
            "line": 20
        }
    ]

    assert actual == expected


def test_test5_code():
    actual = build_symbol_table('Test5.pas')
    expected = [
        {
            "token": "program",
            "type": "Keyword",
            "line": 1
        },
        {
            "token": "Test5",
            "type": "Identifier",
            "line": 1
        },
        {
            "token": ";",
            "type": "Delimiter",
            "line": 1
        },
        {
            "token": "var",
            "type": "Keyword",
            "line": 2
        },
        {
            "token": "A",
            "type": "Identifier",
            "line": 3
        },
        {
            "token": ",",
            "type": "Delimiter",
            "line": 3
        },
        {
            "token": "B",
            "type": "Identifier",
            "line": 3
        },
        {
            "token": ",",
            "type": "Delimiter",
            "line": 3
        },
        {
            "token": "R",
            "type": "Identifier",
            "line": 3
        },
        {
            "token": ",",
            "type": "Delimiter",
            "line": 3
        },
        {
            "token": "I",
            "type": "Identifier",
            "line": 3
        },
        {
            "token": ":",
            "type": "Delimiter",
            "line": 3
        },
        {
            "token": "integer",
            "type": "Keyword",
            "line": 3
        },
        {
            "token": ";",
            "type": "Delimiter",
            "line": 3
        },
        {
            "token": "begin",
            "type": "Keyword",
            "line": 4
        },
        {
            "token": "for",
            "type": "Keyword",
            "line": 5
        },
        {
            "token": "I",
            "type": "Identifier",
            "line": 5
        },
        {
            "token": ":=",
            "type": "AttributionOperator",
            "line": 5
        },
        {
            "token": "1",
            "type": "Number",
            "line": 5
        },
        {
            "token": "to",
            "type": "Keyword",
            "line": 5
        },
        {
            "token": "5",
            "type": "Number",
            "line": 5
        },
        {
            "token": "do",
            "type": "Keyword",
            "line": 5
        },
        {
            "token": "begin",
            "type": "Keyword",
            "line": 6
        },
        {
            "token": "A",
            "type": "Identifier",
            "line": 7
        },
        {
            "token": ":=",
            "type": "AttributionOperator",
            "line": 7
        },
        {
            "token": "A",
            "type": "Identifier",
            "line": 7
        },
        {
            "token": "*",
            "type": "ArithmeticOperator",
            "line": 7
        },
        {
            "token": "A",
            "type": "Identifier",
            "line": 7
        },
        {
            "token": ";",
            "type": "Delimiter",
            "line": 7
        },
        {
            "token": "B",
            "type": "Identifier",
            "line": 8
        },
        {
            "token": ":=",
            "type": "AttributionOperator",
            "line": 8
        },
        {
            "token": "B",
            "type": "Identifier",
            "line": 8
        },
        {
            "token": "*",
            "type": "ArithmeticOperator",
            "line": 8
        },
        {
            "token": "A",
            "type": "Identifier",
            "line": 8
        },
        {
            "token": ";",
            "type": "Delimiter",
            "line": 8
        },
        {
            "token": "R",
            "type": "Identifier",
            "line": 9
        },
        {
            "token": ":=",
            "type": "AttributionOperator",
            "line": 9
        },
        {
            "token": "A",
            "type": "Identifier",
            "line": 9
        },
        {
            "token": "+",
            "type": "ArithmeticOperator",
            "line": 9
        },
        {
            "token": "B",
            "type": "Identifier",
            "line": 9
        },
        {
            "token": "end",
            "type": "Keyword",
            "line": 10
        },
        {
            "token": "end",
            "type": "Keyword",
            "line": 11
        },
        {
            "token": ".",
            "type": "Delimiter",
            "line": 11
        }
    ]

    assert actual == expected
