from telebot import *
from json import load
from telebot.types import *
from stations import MariaConnetion, Users, Stations
from random import choice 

try:
    configures = load(open("configures.json", encoding="utf-8"))
except:
    print("Неправильно составлен configures.json или не верен путь")

database_params = configures["db-conn-params"]
messages = configures["messages"]
menu_options = messages["menu"]
stats = configures["stations"]


maria = MariaConnetion(database_params)
users = Users(maria)
stations = Stations(maria)

try:
    API = open("API.txt", "r").read().split(sep="\n")[0]
except: 
    print("API is empty!")
    print("Stopping server...")
    sys.exit(0)
if API == "":
    print("API is empty!")
    print("Stopping server...")
    sys.exit(0)
# getting API from API file

bot = TeleBot(API)
# master entitie

def finish(chat_id, text):
    bot.send_message(chat_id, text)

def card(chat_id, username):
    bot.send_message(chat_id, username)
    ## sql actions

def choose(message, username):
    current = users.get_curr(username)[0][0]
    user_stats = set([ int(stat) for stat in users.get_user(username)[0][0].split(sep=" ") ])
    print(user_stats)
    # print(current)
    if current != "0":
        bot.send_message(message.chat.id, f"you are on a station {current}. You cant leave! Enter finishcode firstly!")
        bot.register_next_step_handler(message, finishcode, station=current)
    else:
        if user_stats == {0}:
            stat = choice(list(stats.keys()))
            bot.send_message(message.chat.id, messages["random"])
            bot.send_message(message.chat.id, f"Station{stat}\n{stats[stat]['info']}\nEnter station password:")
            bot.register_next_step_handler(message, passcode, station=stat)
        else:
            keyboard = InlineKeyboardMarkup()
            for stat in stats:
                user_stats = [ st for st in users.get_user(username)[0][0].split(sep=' ') ]
                if not (stat in user_stats):
                    # print(stats[stat])
                    button = InlineKeyboardButton(text=str(stat), callback_data=str(stat))
                    keyboard.add(button)
        
            bot.send_message(message.chat.id, "choose station", reply_markup=keyboard)

# command executers

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = InlineKeyboardMarkup()
    for menu_option in menu_options:
        button = InlineKeyboardButton(text=f"{menu_options[menu_option]['text']}", callback_data=f"{menu_options[menu_option]['callback']}")
        keyboard.add(button)

    bot.send_message(message.chat.id, text=messages["start"], reply_markup=keyboard)
    users.add_user(message.chat.username)   

# command handlers

@bot.callback_query_handler(func = lambda call: True)
def callback(call):
    current = users.get_curr(call.message.chat.username)[0][0]
    # if current == "0":
    if True:
        if call.data == "finish":
            finish(call.message.chat.id, messages["finish"])
        elif call.data == "card":
            card(call.message.chat.id, "card for " + str(call.message.chat.username))
        elif call.data == "choose":
            choose(call.message, call.message.chat.username)
        elif call.data in stats.keys():
            if current == "0":
                keyboard = InlineKeyboardMarkup()
                yes = InlineKeyboardButton("Enter passcode", callback_data=f"passcode {call.data}")
                no = InlineKeyboardButton("Cancel", callback_data="choose")

                keyboard.add(yes)
                keyboard.add(no)

                bot.send_message(call.message.chat.id, text=stats[call.data]["info"], reply_markup=keyboard)

            else:
                bot.send_message(call.message.chat.id, text=f"finish station {current} firstly!")
                
        elif call.data.split(sep=" ")[0] == "passcode":
            bot.send_message(call.message.chat.id, text=f"Enter passcode for {call.data.split(sep=' ')[1]}")
            bot.register_next_step_handler(call.message, passcode, station=call.data.split(sep=" ")[1])
    
def passcode(message, station):
    attempt = message.text
    # print(f"attempt {attempt}")
    # print(stations.get_password(station)[0][0])
    if attempt == stations.get_password(station)[0][0]:
        users.set_curr(message.chat.username, station)
        bot.send_message(message.chat.id, text=messages["reg"])
        if stats[station]["files"] != "none":
            # print(stats[station]["files"])
            try:
                doc = open(stats[station]["files"], 'rb').read()
                bot.send_document(message.chat.id, doc, caption="This is a help doc.")
            except:
                print(f"Error! Doc {stats[station]["files"]} not found!")
        bot.register_next_step_handler(message, finishcode, station=station)
    else:
        bot.send_message(message.chat.id, text="Incorrect password. Try again!")
        bot.register_next_step_handler(message, passcode, station=station)


def finishcode(message, station):
    attempt = message.text
    # print(attempt)
    # print(stations.get_finish(station)[0][0])
    if attempt == stations.get_finish(station)[0][0]:
        users.set_curr(message.chat.username, "0")
        users.add_stat(message.chat.username, station)
        bot.send_message(message.chat.id, text=stats[station]["final-message"])
    else:
        bot.send_message(message.chat.id, text="Incorrect finishcode. Try again!")
        bot.register_next_step_handler(message, finishcode, station=station)


# callback handlers

if __name__ == "__main__":
    bot.infinity_polling()