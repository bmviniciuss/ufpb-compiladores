import logging
import re
from os import path

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_lines(file_name):
    file_path = path.join('/'.join(path.abspath(__file__).split('/')[:-1]), '..',
                          'pascal_sources', file_name)
    if not path.exists(file_path):
        logger.error('Cant find file %s', file_path)
    with open(file_path) as f:
        return f.readlines()


def strip_comments(lines):
    return list([re.sub(r'\{.*\}', '', line) for line in lines])


def get_tokens(line):
    return list([token.strip() for token in line.split()])


def build_symbol_table(path):
    tokens_per_line = map(get_tokens, strip_comments(get_lines(path)))
    return list(tokens_per_line)


if __name__ == '__main__':
    # Testes rapidos...
    logging.basicConfig(level=logging.DEBUG)
    res = build_symbol_table('Test1.pas')
    logger.debug(res)
