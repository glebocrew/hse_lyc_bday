from stations import *
from json import load

username = "glebocrew"

conn_params = load(open("configures.json"))
maria = MariaConnetion(conn_params['db-conn-params'])
users = Users(maria)
# users.add_stat("test", "9")
print(*users.get_user("test")[0])