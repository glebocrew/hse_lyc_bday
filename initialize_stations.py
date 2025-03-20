from stations import *
from json import load

conn_params = load(open("configures.json"))
maria = MariaConnetion(conn_params['db-conn-params'])

stations = Stations(maria)

stats = load(open("configures.json"))["stations"]
for stat in stats:
    stations.add_stat(stat, stats[stat]['info'], stats[stat]['password'], stats[stat]['finish'])