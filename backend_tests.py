from stations import *
from json import load

conn_params = load(open("configures.json"))
maria = MariaConnetion(conn_params['db-conn-params'])

stations = Stations(maria)
users = Users(maria)

users.set_curr("glebocrew", '2')
print(users.get_info("glebocrew"))