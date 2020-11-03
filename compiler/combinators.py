from functools import reduce


# Monoidical compose
def compose_one(parser_a, parser_b):
    name = '%s %s' % (parser_a.__name__,
                      parser_b.__name__)

    def parser_c(buffer):
        # Handle unit
        arg_1 = buffer
        if type(buffer) == tuple:
            arg_1 = buffer[0]

        res_1 = parser_a(arg_1)
        if type(res_1) == str:
            return res_1

        # Handle unit
        if type(res_1) == tuple:
            res_1 = res_1[0]
        else:
            res_1 = res_1[1:]

        res_2 = parser_b(res_1)
        if type(res_2) == str:
            return res_2

        return res_2

    # Keep names for logging
    parser_c.__name__ = name

    return parser_c


def compose(*parsers):
    return reduce(lambda curr, acc: compose_one(curr, acc), list(parsers))


def choice(*parsers):
    def choose(buffer):
        seq = map(lambda parser: parser(buffer), parsers)

        for _ in range(len(list(parsers))):
            try:
                res = next(seq)
                if type(res) != str:
                    return res
            except IndexError:
                continue

        return 'Token invalid: \"%s\"' % buffer[0]['token']

    choose.__name__ = ' | '.join([item.__name__ for item in list(parsers)])

    return choose
