from enum import Enum, auto
import re


class TokenType(str, Enum):
    Keyword = "Keyword"
    Delimiter = "Delimiter"
    AttributionOperator = "AttributionOperator"
    ComparisonOperator = "ComparisonOperator"
    AdditiveOperators = "AdditiveOperators"
    MultiplicativeOperators = "MultiplicativeOperators"
    Identifier = "Identifier"
    Integer = "Integer"
    RealNumber = "RealNumber"
    Unknown = "Unknown"


class TokenValueRegex(str, Enum):
    PROGRAM = r'^(program|PROGRAM)$'
    VAR = r'^(var|VAR)$'
    COLON = r'^(:)$'
    SEMICOLON = r'^(;)$'
    POINT = r'^(.)$'
    COMMA = r'^(,)$'
    IDENTIFIER_TYPE = r'^(integer|real|boolean|INTEGER|REAL|BOOLEAN)$'
    BEGIN = r'^(begin|BEGIN)$'
    END = r'^(end|END)$'
