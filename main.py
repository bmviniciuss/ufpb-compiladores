import logging
import fire
from compiler import lexico
from compiler.utils import save_json, get_filename_from_path


class Main():
    def lexico(self, file):
        filename = get_filename_from_path(file)
        logger.debug(file)
        logger.debug(filename)
        try:
            symbol_table_data = lexico.build_symbol_table(file, True)
            save_json(filename, symbol_table_data, "lexico")
        except Exception as e:
            print("Unexpected Error:\n", e)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(level=logging.DEBUG)
    logger.info('Init')
    fire.Fire(Main)
