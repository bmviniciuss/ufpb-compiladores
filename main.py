import logging
from compiler import lexico

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # Setup logging
    lexico.build_symbol_table()
    logging.basicConfig(level=logging.DEBUG)
    logger.info('Init')
