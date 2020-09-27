from os import path
import re
import logging
import json
import pathlib

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


def get_filename_from_path(filepath):
    return filepath.split('/')[-1]


def save_json(filename, data, filename_prefix=""):
    out_dir = path.join('/'.join(path.abspath(__file__).split('/')[:-1]),
                        '..', 'output')
    pathlib.Path(out_dir).mkdir(exist_ok=True)
    logger.debug("Checking output directory")

    filename_without_extension = filename.split('.pas')[0]
    file_path = path.join(out_dir, filename_prefix + '_' +
                          filename_without_extension + '.json')
    logger.debug("Saving JSON output...")
    with open(file_path, 'w') as f:
        json.dump(data, f)
