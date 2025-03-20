from mariadb import *
from json import load


class MariaConnetion:
    """
    A master class for Users and Stations.  
    Establishes connection with Maria DB.  
    """
    def __init__(self, conn_params: dict):
        """
        __init__  (MariaConnection constructor)
        :param conn_params: type: dict, params to connect to mariadb -> [user, password, host, port, db] <-
        """
        try:
            print("Connecting to Maria DB...")
            # log

            self.connection = Connection(**conn_params)
            self.connection.autocommit = True
            self.cursor = Cursor(self.connection)
            # setting connection and cursor initializing

            print("MariaDB Connection established.")
            # log
        except:
            print("MariaDB connection Error!")
            # error


class Users:
    """
    A class, created to manipulate table 'users' in MariaDB
    """
    def __init__(self, mariaconn: MariaConnetion):
        """
        __init__ (Users constructor)  
        :param mariaconn: an existing connection with MariaDB.
        """

        self.maria_connection = mariaconn
        self.queries = {
            "add" : "INSERT INTO users VALUES (?, '0', '0');",
            "find" : "SELECT * FROM users WHERE username = ?",
            "get" : "SELECT stations FROM users WHERE username = ?;",
            "new" : "UPDATE users SET stations = (CONCAT(stations, ' ', ?)) WHERE username = ?;",
            "del" : "DELETE FROM users WHERE username = ?;",
            "cur" : "UPDATE users SET current_station_id = ? WHERE username = ?;",
            "get_stat" : "SELECT current_station_id FROM users WHERE username = ?"
        }
        # queries

        print("Connected to users!")
        # log
    
    def get_info(self, username: str):
        self.maria_connection.cursor.execute(self.queries["find"], [username])
        # print(self.maria_connection.cursor.fetchall())
        return self.maria_connection.cursor.fetchall()

    def get_user(self, username: str):
        """
        Gets username's visited stations.  
        :param username: type: str, gets all stations from table 'users' column 'stations' for username.
        """
        self.maria_connection.cursor.execute(self.queries["get"], [username])
        return self.maria_connection.cursor.fetchall()


    def add_user(self, username: str):
        """
        Add username to table.  
        :param username: type: str, adds user to table 'users' with default params of stations and current stations = 0
        """
        print(self.get_info(username))
        if self.get_info(username) in ["", [],  None]:
            self.maria_connection.cursor.execute(self.queries["add"], [username])

    
    def add_stat(self, username: str, station: str):
        """
        Adds station to username's visited station.  
        :param username: type: str, username that visited a station.  
        :param station: type: str, a station visited by username.  
        """
        self.maria_connection.cursor.execute(self.queries["new"], [station, username])

    def del_user(self, username: str):
        """
        Deletes user and all info about they from table.  
        :param username: type: str, username that must be deleted.
        """
        self.maria_connection.cursor.execute(self.queries["del"], [username])

    def set_curr(self, username: str, station: str):
        """
        Sets current username's station.
        :param username: type: str, username of configuring user.
        :param station: type: str (sorry), current username station.
        """
        self.maria_connection.cursor.execute(self.queries["cur"], [str(station), str(username)])

    def get_curr(self, username: str):
        """
        Gets username's current station.
        :param username: type: str, username whose current station we're getting. 
        """
        self.maria_connection.cursor.execute(self.queries["get_stat"], [username])
        return self.maria_connection.cursor.fetchall()
    
class Stations:
    """
    A class, created to manipulate table 'stations' in MariaDB
    """
    def __init__(self, mariaconn: MariaConnetion):
        """
        __init__ (Users constructor)  
        :param mariaconn: an existing connection with MariaDB.
        """
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
        """
        Deletes stations by it's id.  
        :param station_id: type: str, station's id.  
        """
        self.maria_connection.cursor.execute(self.queries["del"], [station_id])

    def get_all(self, station_id: str):
        """
        Gets all station information.  
        :param station_id: id of interesting station.  
        """
        self.maria_connection.cursor.execute(self.queries["get_all"], [station_id])
        return self.maria_connection.cursor.fetchall()

    def add_stat(self, station_id: str, info: str, station_password: str, staton_finish: str):
        """
        Adds station to table 'stations'.  
        :args: -> [station_id: str, info: str, station_password: str, staton_finish: str] <-
        """
        if not( self.get_info(station_id) in [[], None, ""] ):
            print(f"Station with station_id = {station_id} already exists.")
        else:    
            self.maria_connection.cursor.execute(self.queries["add"], [station_id, info, station_password, staton_finish])

    def get_info(self, station_id: str):
        """
        Gets information field of a station.
        :param station_id: type: str
        """
        self.maria_connection.cursor.execute(self.queries["get_info"], [station_id])
        return self.maria_connection.cursor.fetchall()

    def get_password(self, station_id: str):
        """
        Gets station enter password.
        :param station_id: type: str.
        """
        self.maria_connection.cursor.execute(self.queries["get_password"], [station_id])
        return self.maria_connection.cursor.fetchall()


    def get_finish(self, station_id: str):
        """
        Gets station finish code.
        :param station_id: type: str.
        """
        self.maria_connection.cursor.execute(self.queries["get_finish"], [station_id])
        return self.maria_connection.cursor.fetchall()
    