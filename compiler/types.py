from enum import Enum, auto


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
