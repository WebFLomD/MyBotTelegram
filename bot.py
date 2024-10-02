import telebot
from telebot import types
import requests
import config

# Инициализация бота
bot = telebot.TeleBot(config.TOKEN_BOT_TELEGRAM)
print('Бот запущен!')

# Словарь для хранения состояния пользователей
user_states = {}



@bot.message_handler(commands=['start']) # <--- Команда - "start"
def start (message):
    send_start_message(message.chat.id, message.from_user.first_name, message.from_user.id)

def send_start_message(chat_id, first_name, user_id):
    markup = types.InlineKeyboardMarkup()

    btn_weather = types.InlineKeyboardButton('⛅ Погода', callback_data='weather') # <--- Кнопка "Погода"
    btn_contact = types.InlineKeyboardButton('📌 Контакты', callback_data='contact') # <--- Кнопка "Контакты"
    btn_profile = types.InlineKeyboardButton('👤 Профиль', callback_data='profile') # <--- Кнопка "Профиль"

    markup.row(btn_contact, btn_profile)
    markup.row(btn_weather)


    bot.send_message(chat_id, f'Привет, {first_name}! Выберите опцию:', reply_markup=markup)


@bot.message_handler(commands=['code-message']) # <--- Команда - "code-message" для получение json
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

        bot.send_message(callback.message.chat.id,
                         f'Личный кабинет\n\nВаш ID: {user_id}\nВаше имя: {user_first_name}\nВаш телеграмм: {user_username}',
                         reply_markup=markup)

    # Погода
    elif callback.data == 'weather':
        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton('Назад', callback_data='start')
        markup.add(btn_back)

        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        bot.send_message(callback.message.chat.id, 'Чтобы получить данные о погоде, напишите название города.', reply_markup=markup)

        user_states[callback.message.chat.id] = 'weather_city'



    # Возвращается в начало
    elif callback.data == 'start':

        markup = types.InlineKeyboardMarkup()

        btn_weather = types.InlineKeyboardButton('⛅ Погода', callback_data='weather')  # <--- Кнопка "Погода"
        btn_contact = types.InlineKeyboardButton('📌 Контакты', callback_data='contact')  # <--- Кнопка "Контакты"
        btn_profile = types.InlineKeyboardButton('👤 Профиль', callback_data='profile')  # <--- Кнопка "Профиль"

        markup.row(btn_contact, btn_profile)
        markup.row(btn_weather)

        bot.edit_message_text(chat_id=callback.message.chat.id,
                        message_id=callback.message.message_id,
                        text=f'Привет, {callback.from_user.first_name}, ваш ID: {callback.from_user.id}! Выберите опцию:',
                        reply_markup=markup)


@bot.message_handler(func=lambda message: True)

# Получение данные о погоде, которую ввел пользователь ↓
def get_weather(message):
    # Кнопка назад
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton('Назад', callback_data='start')
    markup.add(btn_back)


    city = message.text # <--- Полученный название города от пользователя

    # Если есть такое город, без отпечатков, то проходит дальше ↓
    try:
        url = f'http://api.weatherapi.com/v1/current.json?key={config.WEATHERAPI_KEY}&q={city}' # <--- Название города может на Русском или на Английском
        weather = requests.get(url).json()

        temperature = weather['current']['temp_c'] # <--- Получаем данные - Температура
        wind_speed = weather['current']['wind_kph'] # <--- Получаем данные - Ветер
        cloud_cover = weather['current']['condition']['text'] # <--- Получаем данные - Облачность
        humidity = weather['current']['humidity'] # <--- Получаем данные - Влажность

        # Вывод полученной информации в сообщение ↓
        bot.send_message(message.chat.id, f'Температура: {temperature} °C\n'
                                           f'Ветер: {wind_speed} м/с\n'
                                           f'Облачность: {cloud_cover}\n'
                                           f'Влажность: {humidity}%', reply_markup=markup)


    except KeyError:
        bot.send_message(message.chat.id, f'Не удалось определить название города: {city}', reply_markup=markup)

# Вывод полученной информации ↓
def info(message):
    userId = message.chat.id
    if user_states.get(userId) == 'awaiting_city':
        get_weather(message)
        user_states[userId] = None  # Сбрасываем состояние после получения города
    else:
        if message.text.lower() == 'привет':
            bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
        elif message.text.lower() == 'id':
            bot.reply_to(message, f'Ваш ID: {message.from_user.id}')


bot.polling (non_stop = True)