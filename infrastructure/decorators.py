import sqlite3


def sqlite_connection_handler(connection_string: str):
    def connection_handler(action):
        def decorated_action(*params):
            conn = sqlite3.connect(connection_string)
            conn.execute("PRAGMA foreign_keys=on;")
            output = action(*params, conn)
            conn.close()
            return output
        return decorated_action
    return connection_handler
