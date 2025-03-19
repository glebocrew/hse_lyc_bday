from stations import *
from json import load

username = "glebocrew"

conn_params = load(open("configures.json"))
maria = MariaConnetion(conn_params['db-conn-params'])

stations = Stations(maria)

stations.del_stat("1")
stations.del_stat("2")