from os.path import dirname, join

DATABASE_FILE_NAME = 'drones.db'
DATABASE_CONNECTION_STRING = join(dirname(__file__), DATABASE_FILE_NAME)