import logging
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def runSyntacticAnalysis():
    pass


if __name__ == '__main__':
    logger.debug(1)

    # Testes rapidos...
    logging.basicConfig(level=logging.DEBUG)
    logger.debug("Sintatico")

    res = runSyntacticAnalysis()
    logger.debug(json.dumps(res, indent=2))
