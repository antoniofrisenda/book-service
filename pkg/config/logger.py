import logging


def setup_logging():

    logging.basicConfig(
        level=logging.DEBUG, 
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.getLogger('pymongo').setLevel(logging.WARNING)