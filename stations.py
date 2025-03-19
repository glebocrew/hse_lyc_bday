from mariadb import *
from json import load

class MariaConnetion:
    def __init__(self, conn_params: dict):
        try:
            self.connection = Connection(**conn_params)
            self.connection.autocommit = True
            self.cursor = Cursor(self.connection)
        except:
            print("MariaConnection Error!")
class Users:
    def __init__(self, mariaconn: MariaConnetion):
        self.maria_connection = mariaconn
        self.queries = {
            "add" : "INSERT INTO users VALUES (?, '0', '0');",
            "get" : "SELECT stations FROM users WHERE username = ?;",
            "new" : "UPDATE users SET stations = (CONCAT(stations, ' ', ?)) WHERE username = ?;",
            "del" : "DELETE FROM users WHERE username = ?"
        }

    def add_user(self, username: str):
        self.maria_connection.cursor.execute(self.queries["add"], [username])

    def get_user(self, username: str):
        self.maria_connection.cursor.execute(self.queries["get"], [username])
        return self.maria_connection.cursor.fetchall()
    
    def add_stat(self, username: str, station: str = "1"):
        self.maria_connection.cursor.execute(self.queries["new"], [station, username])

    def del_user(self, username: str):
        self.maria_connection.cursor.execute(self.queries["del"], [username])

