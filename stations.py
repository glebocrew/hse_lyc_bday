from mariadb import *
from json import load

class MariaConnetion:
    def __init__(self, conn_params: dict):
        try:
            print("Connecting to Maria DB...")
            self.connection = Connection(**conn_params)
            self.connection.autocommit = True
            self.cursor = Cursor(self.connection)
            print("MariaDB Connection established.")
        except:
            print("MariaDB connection Error!")
class Users:
    def __init__(self, mariaconn: MariaConnetion):
        self.maria_connection = mariaconn
        self.queries = {
            "add" : "INSERT INTO users VALUES (?, '0', '0');",
            "get" : "SELECT stations FROM users WHERE username = ?;",
            "new" : "UPDATE users SET stations = (CONCAT(stations, ' ', ?)) WHERE username = ?;",
            "del" : "DELETE FROM users WHERE username = ?;",
            "cur" : "UPDATE users SET current_station_id = '?' WHERE username='?';",
            "get_stat" : "SELECT current_station_id FROM users WHERE username = ?"
        }
        print("Connected to users!")

    def add_user(self, username: str):
        self.maria_connection.cursor.execute(self.queries["add"], [username])

    def get_user(self, username: str):
        self.maria_connection.cursor.execute(self.queries["get"], [username])
        return self.maria_connection.cursor.fetchall()
    
    def add_stat(self, username: str, station: str):
        self.maria_connection.cursor.execute(self.queries["new"], [station, username])

    def del_user(self, username: str):
        self.maria_connection.cursor.execute(self.queries["del"], [username])

    def set_curr(self, username: str, station: str):
        self.maria_connection.cursor.execute(self.queries["cur"], [station, username])

    def get_curr(self, username: str):
        self.maria_connection.cursor.execute(self.queries["get_stat"], [username])
        return self.maria_connection.cursor.fetchall()
    
class Stations:
    def __init__(self, mariaconn: MariaConnetion):
        self.queries = {
            "add" : "INSERT INTO stations VALUES (?, ?, ?, ?);",
            "del" : "DELETE FROM stations WHERE station_id = ?;",
            "get_all" : "SELECT * FROM stations WHERE station_id = ?;",
            "get_info" : "SELECT info FROM stations WHERE station_id = ?;",
            "get_password" : "SELECT station_password FROM stations WHERE station_id = ?;",
            "get_finish" : "SELECT station_finish FROM stations WHERE station_id = ?;"
        }
        self.maria_connection = mariaconn
        print("Connected to stations!")

    def del_stat(self, station_id: str):
        self.maria_connection.cursor.execute(self.queries["del"], [station_id])

    def get_station(self, station_id: str):
        self.maria_connection.cursor.execute(self.queries["get_all"], [station_id])
        return self.maria_connection.cursor.fetchall()

    def add_stat(self, station_id: str, info: str, station_password: str, staton_finish: str):
        if self.get_station(station_id):
            print(f"Station with station_id = {station_id}")
        else:    
            self.maria_connection.cursor.execute(self.queries["add"], [station_id, info, station_password, staton_finish])

    def get_all(self, station_id: str):
        self.maria_connection.cursor.execute(self.queries["get_all"], [station_id])
        return self.maria_connection.cursor.fetchall()

    def get_info(self, station_id: str):
        self.maria_connection.cursor.execute(self.queries["get_info"], [station_id])
        return self.maria_connection.cursor.fetchall()

    def get_password(self, station_id: str):
        self.maria_connection.cursor.execute(self.queries["get_password"], [station_id])
        return self.maria_connection.cursor.fetchall()


    def get_finish(self, station_id: str):
        self.maria_connection.cursor.execute(self.queries["get_finish"], [station_id])
        return self.maria_connection.cursor.fetchall()