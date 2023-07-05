import logging
from config import EVENT_LOGS_FILE


class BatteryLogger:
    def __init__(self):
        log_format = '[%(asctime)s][%(levelname)s]: %(message)s'
        logging.basicConfig(filename=EVENT_LOGS_FILE, filemode='w', format=log_format)
        self.__logger = logging.getLogger('server_logger') 
        self.__logger.setLevel(logging.INFO)

    def write(self, message):
        self.__logger.info(message)