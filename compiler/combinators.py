from functools import reduce


def empty_left(parser_a, parser_b, buffer):
    try:
        a = parser_a(buffer)
        assert type(a) == Unit
        b = parser_b(buffer)
        assert type(b) == Unit
        return b.unwrap()
    except AssertionError:
        return 'EOF'
    except IndexError:
        return 'EOF'


def empty_inner(parser, buffer):
    try:
        b = parser(buffer)
        assert type(b) == Unit
        return b.unwrap()
    except AssertionError:
        return 'EOF'
    except IndexError:
        return 'EOF'


def sequence_one(parser_a, parser_b):
    name = '%s %s' % (parser_a.__name__,
                      parser_b.__name__)

    def parser_c(buffer):
        # Empty input is only valid if the chain is empty
        if buffer == []:
            return empty_left(parser_a, parser_b, buffer)

        a = parser_a(buffer)

        if type(a) == str:
            return a

        # Handle empty inner left
        if a == []:
            return empty_inner(parser_b, a)

        return parser_b(a)

    # Keep names for logging
    parser_c.__name__ = name

    return parser_c


def sequence(*parsers):
    return reduce(lambda curr, acc: sequence_one(curr, acc), list(parsers))


def choice(*parsers):
    def choose(buffer):
        seq = map(lambda parser: parser(buffer), parsers)

        for i in range(len(list(parsers))):
            try:
                res = next(seq)
                if type(res) == Unit:
                    return res
                if type(res) != str:
                    return res
                if i == len(parsers) - 1:
                    return res
            except IndexError:
                continue
    choose.__name__ = ' | '.join([item.__name__ for item in list(parsers)])

    return choose


class Unit():
    def __init__(self, value):
        self.value = value

    def unwrap(self):
        return self.value
