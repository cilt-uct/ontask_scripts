import logging
from config.config import *

# create logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s; [%(levelname)s]; %(message)s')

# create file handler
fh = logging.FileHandler(LOG_PATH)
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)

if LOG_IN_CONSOLE:
    # create stream handler (logging in the console)
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
