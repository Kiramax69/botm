import telebot
import requests
from requests.auth import HTTPBasicAuth

# Установите свой токен бота Telegram
TELEGRAM_BOT_TOKEN = '6332761306:AAH08CnPCaNxIMTxqhGYts4ebX_nz1c75nM'

# URL и ключи для FastPanel API
FASTPANEL_API_URL = 'https://cv3909137.vps.regruhosting.ru:8888/vhosts/1/emails/1/boxes'
FASTPANEL_USERNAME = 'fastuser'
FASTPANEL_PASSWORD = 'Aeng7oi7sohv'

# Создание бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Используйте команду /create_email <username> для создания почтового ящика.")

@bot.message_handler(commands=['create_email'])
def create_email(message):
    try:
        username = message.text.split()[1]
    except IndexError:
        bot.reply_to(message, "Пожалуйста, укажите имя пользователя для почтового ящика. Пример: /create_email username")
        return
    
    domain = 'sukaa.ru'  # Ваш домен
    email = f"{username}@{domain}"
    password = 'temporary_password'  # Генерация временного пароля

    # Запрос на создание почтового ящика в FastPanel
    auth = HTTPBasicAuth(FASTPANEL_USERNAME, FASTPANEL_PASSWORD)
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "email": email,
        "password": password
    }
    
    response = requests.post(f'{FASTPANEL_API_URL}/mailboxes', headers=headers, json=payload, auth=auth)
    
    if response.status_code == 201:
        bot.reply_to(message, f'Почтовый ящик {email} успешно создан с паролем {password}.')
    else:
        bot.reply_to(message, f'Ошибка при создании почтового ящика: {response.text}')

bot.polling()
