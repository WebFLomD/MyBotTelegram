import telebot
from telebot import types

import config

# Инициализация бота
bot = telebot.TeleBot(config.TOKEN_BOT_TELEGRAM)


@bot.message_handler(commands=['start']) # <--- Команда - "start"
def start (message):
    send_start_message(message.chat.id, message.from_user.first_name, message.from_user.id)


def send_start_message(chat_id, first_name, user_id):
    markup = types.InlineKeyboardMarkup()

    btn_contact = types.InlineKeyboardButton('📌 Контакты', callback_data='contact') # <--- Кнопка "Контакты"
    btn_profile = types.InlineKeyboardButton('👤 Профиль', callback_data='profile') # <--- Кнопка "Профиль"

    markup.row(btn_contact, btn_profile)
    

    bot.send_message(chat_id, f'Привет, {first_name}, ваш ID: {user_id}! Выберите опцию:', reply_markup=markup)


@bot.message_handler(commands=['code-message']) # <--- Команда - "code-message"
def code_message(message):
    bot.send_message(message.chat.id, message)


@bot.callback_query_handler(func=lambda callback: True)
def handle_callback(callback):
    
    # Контакты
    if callback.data == 'contact':
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id) # <--- Удаляющее сообщение

        markup = types.InlineKeyboardMarkup()
        btn_vk = types.InlineKeyboardButton('VK', url='https://vk.com/zzakharov666')
        btn_git_hub = types.InlineKeyboardButton('GitHub', url='https://github.com/WebFLomD')
        btn_back = types.InlineKeyboardButton('Назад', callback_data='start')

        markup.add(btn_vk, btn_git_hub)
        markup.add(btn_back)

        bot.send_message(callback.message.chat.id, 'Контакты. Выберите опцию:', reply_markup=markup)


    # Профиль пользователя
    elif callback.data == 'profile':
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id) # <--- Удаляющее сообщение

        user_id = callback.message.chat.id
        user_first_name = callback.message.chat.first_name
        user_username = callback.message.chat.username

        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton('Назад', callback_data='start')
        markup.add(btn_back)

        bot.send_message(callback.message.chat.id, f'Личный кабинет\n\nВаш ID: {user_id}\nВаше имя: {user_first_name}\nВаш телеграмм: {user_username}', reply_markup=markup)
    
    # Возвращается в начало
    elif callback.data == 'start':        
        
        markup = types.InlineKeyboardMarkup()
        btn_contact = types.InlineKeyboardButton('Контакты', callback_data='contact') # <--- Кнопка "Контакты"
        btn_profile = types.InlineKeyboardButton('Профиль', callback_data='profile') # <--- Кнопка "Профиль"
        markup.row(btn_contact, btn_profile)

        bot.edit_message_text(chat_id=callback.message.chat.id, 
                        message_id=callback.message.message_id, 
                        text=f'Привет, {callback.from_user.first_name}, ваш ID: {callback.from_user.id}! Выберите опцию:', 
                        reply_markup=markup)
        

@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'Ваш ID: {message.from_user.id}')


bot.polling (non_stop = True)