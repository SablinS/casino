import telebot
from telebot import types
from casino import Casino

casino = Casino()

API_TOKEN = 'YOUR TOKEN HERE'
bot = telebot.TeleBot(API_TOKEN)

user_sessions = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Casino Bot! Type /register to create an account or /login to log in.")

@bot.message_handler(commands=['register'])
def register_user(message):
    user_sessions[message.chat.id] = {'stage': 'register_name'}
    bot.send_message(message.chat.id, "Enter your name:")

@bot.message_handler(func=lambda message: user_sessions.get(message.chat.id, {}).get('stage') == 'register_name')
def get_name(message):
    user_sessions[message.chat.id]['name'] = message.text
    user_sessions[message.chat.id]['stage'] = 'register_age'
    bot.send_message(message.chat.id, "Enter your age:")

@bot.message_handler(func=lambda message: user_sessions.get(message.chat.id, {}).get('stage') == 'register_age')
def get_age(message):
    user_sessions[message.chat.id]['age'] = message.text
    user_sessions[message.chat.id]['stage'] = 'register_gender'
    bot.send_message(message.chat.id, "Enter your gender (M/F):")

@bot.message_handler(func=lambda message: user_sessions.get(message.chat.id, {}).get('stage') == 'register_gender')
def get_gender(message):
    user_sessions[message.chat.id]['gender'] = message.text
    user_sessions[message.chat.id]['stage'] = 'register_login'
    bot.send_message(message.chat.id, "Create a login:")

@bot.message_handler(func=lambda message: user_sessions.get(message.chat.id, {}).get('stage') == 'register_login')
def get_login(message):
    user_sessions[message.chat.id]['login'] = message.text
    user_sessions[message.chat.id]['stage'] = 'register_password'
    bot.send_message(message.chat.id, "Create a password:")

@bot.message_handler(func=lambda message: user_sessions.get(message.chat.id, {}).get('stage') == 'register_password')
def get_password(message):
    user_sessions[message.chat.id]['password'] = message.text
    name = user_sessions[message.chat.id]['name']
    age = user_sessions[message.chat.id]['age']
    gender = user_sessions[message.chat.id]['gender']
    login = user_sessions[message.chat.id]['login']
    password = user_sessions[message.chat.id]['password']
    success, msg = casino.reg(name, age, gender, login, password)
    bot.send_message(message.chat.id, msg)
    if success:
        user_sessions.pop(message.chat.id, None)

@bot.message_handler(commands=['login'])
def login_user(message):
    user_sessions[message.chat.id] = {'stage': 'login_login'}
    bot.send_message(message.chat.id, "Enter your login:")

@bot.message_handler(func=lambda message: user_sessions.get(message.chat.id, {}).get('stage') == 'login_login')
def get_login_for_login(message):
    user_sessions[message.chat.id]['login'] = message.text
    user_sessions[message.chat.id]['stage'] = 'login_password'
    bot.send_message(message.chat.id, "Enter your password:")

@bot.message_handler(func=lambda message: user_sessions.get(message.chat.id, {}).get('stage') == 'login_password')
def get_password_for_login(message):
    login = user_sessions[message.chat.id]['login']
    password = message.text
    success, msg = casino.log_in(login, password)
    bot.send_message(message.chat.id, msg)
    if success:
        bot.send_message(message.chat.id, "Enter your bet:")
        user_sessions[message.chat.id]['stage'] = 'casino_game'
    else:
        user_sessions.pop(message.chat.id, None)

@bot.message_handler(func=lambda message: user_sessions.get(message.chat.id, {}).get('stage') == 'casino_game')
def play_casino_game(message):
    try:
        bet = int(message.text)
        markup = types.ReplyKeyboardMarkup(row_width=3)
        markup.add("<", ">", "=")
        msg = bot.send_message(message.chat.id, "Choose <, >, or =", reply_markup=markup)
        bot.register_next_step_handler(msg, lambda m: evaluate_guess(m, bet))
    except ValueError:
        bot.send_message(message.chat.id, "Please enter a valid bet amount.")

def evaluate_guess(message, bet):
    guess = message.text
    login = user_sessions[message.chat.id]['login']
    result, a, b = casino.play_casino(login, bet, guess)
    if result is True:
        bot.send_message(message.chat.id, f"You won! The numbers were {a} and {b}.")
    elif result is False:
        bot.send_message(message.chat.id, f"You lost. The numbers were {a} and {b}.")
    else:
        bot.send_message(message.chat.id, f"Insufficient balance. Player balance: {a}, Casino balance: {b}.")
    user_sessions.pop(message.chat.id, None)

bot.polling()
