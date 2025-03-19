from telebot import *
from json import load
from telebot.types import *
from stations import MariaConnetion, Users

try:
    configures = load(open("configures.json", encoding="utf-8"))
except:
    print("Неправильно составлен configures.json или не верен путь")

database_params = configures["db-conn-params"]
messages = configures["messages"]
menu_options = messages["menu"]


API = open("API.txt", "r").read()
# getting API from API file

bot = TeleBot(API)
# master entitie

def finish(chat_id, text):
    bot.send_message(chat_id, text)

def card(chat_id, username):
    bot.send_message(chat_id, username)
    ## sql actions

def choose(chat_id, username):
    if True:
        bot.send_message(chat_id, "choose station")


# command executers

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = InlineKeyboardMarkup()
    for menu_option in menu_options:
        button = InlineKeyboardButton(text=f"{menu_options[menu_option]['text']}", callback_data=f"{menu_options[menu_option]['callback']}")
        keyboard.add(button)
    bot.send_message(message.chat.id, text=messages["start"], reply_markup=keyboard)

# command handlers

@bot.callback_query_handler(func = lambda call: True)
def callback(call):
    if call.data == "finish":
        finish(call.message.chat.id, messages["finish"])
    elif call.data == "card":
        card(call.message.chat.id, call.message.chat.username)
    elif call.data == "choose":
        choose()

# callback handlers

if __name__ == "__main__":
    bot.infinity_polling()