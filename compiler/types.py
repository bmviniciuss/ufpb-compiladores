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
    PROCEDURE = r'^(procedure)$'
    VAR = r'^(var|VAR)$'
    COLON = r'^(:)$'
    SEMICOLON = r'^(;)$'
    POINT = r'^(.)$'
    COMMA = r'^(,)$'
    VAR_TYPE = r'^(integer|real|boolean|INTEGER|REAL|BOOLEAN)$'
    BEGIN = r'^(begin|BEGIN)$'
    END = r'^(end|END)$'
    OPEN_PARENTHESIS = r'^(\()$'
    CLOSE_PARENTHESIS = r'^(\))$'
    OP_MULTI = r'^(\*|/|and|AND)$'
    OP_MULTI_SIGNAL = r'^(\*|/)$'
    OP_MULTI_AND = r'^(and|AND)$'
    OP_ADD = r'^(\+|-|or|OR)$'
    OR = r'^(or|OR)$'
    OP_RELATIONAL = r'^(=|<|>|<=|>=|<>)$'
    SINAL = r'^(\+|-)$'
    BOOLEAN = r'^(true|TRUE|false|FALSE)$'
    NOT = r'^(not|NOT)$'
    IF = r'^(if|IF)$'
    ELSE = r'^(else|ELSE)$'
    WHILE = r'^(while|WHILE)$'
    THEN = r'^(then|THEN)$'
    DO = r'^(do|DO)$'
    ASSIGNMENT = r'^(:=)$'
