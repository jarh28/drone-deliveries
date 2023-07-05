from os.path import dirname, join
from uuid import uuid4

DATABASE_FILE_NAME = 'drones.db'
DATABASE_CONNECTION_STRING = join(dirname(__file__), DATABASE_FILE_NAME)
EVENT_LOGS_PERIOD = 60 * 3
EVENT_LOGS_FILE = join(dirname(__file__), 'logs', f'{uuid4()}-battery.log')