import os
import logging

LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def setup_logging(log_level=logging.INFO):
    logging.basicConfig(level=log_level, format=LOGGING_FORMAT)

def get_current_timestamp():
    return str(int(time.time()))

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def setup_logger(logger_name, log_level):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    return logger