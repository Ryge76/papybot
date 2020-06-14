import logging

logger = logging.getLogger('components')
logger.setLevel(logging.DEBUG)

log_file = logging.FileHandler('components.log')
log_file.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s:  %(message)s')
log_file.setFormatter(formatter)

logger.addHandler(log_file)
