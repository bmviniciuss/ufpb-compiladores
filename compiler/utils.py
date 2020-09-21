from os import path
import logging

logger = logging.getLogger(__name__)


def get_src_code(file_name):
    file_path = path.join('/'.join(path.abspath(__file__).split('/')[:-1]), '..',
                          'pascal_sources', file_name)
    if not path.exists(file_path):
        logger.error('Cant find file %s', file_path)
    with open(file_path) as f:
        return f.read()


def strip_comments(string):
    return re.sub(r'\{.*\}', '', string)
