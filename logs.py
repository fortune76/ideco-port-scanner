import logging

logger = logging.getLogger('ideco_port_checker')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s  %(name)s  %(levelname)s  | %(funcName)s | - %(message)s')

ch.setFormatter(formatter)

logger.addHandler(ch)
