
import telebot
import requests
from requests.auth import HTTPBasicAuth

# Установите свой токен бота Telegram
TELEGRAM_BOT_TOKEN = '6332761306:AAH08CnPCaNxIMTxqhGYts4ebX_nz1c75nM'

# URL и ключи для FastPanel API
FASTPANEL_API_URL = 'https://cv3909137.vps.regruhosting.ru:8888/vhosts/1/emails'  # Проверьте корректность URL
FASTPANEL_USERNAME = 'fastuser'
FASTPANEL_PASSWORD = 'Aeng7oi7sohv'
FASTPANEL_API_KEY = 'cd707aa8635689043f7be0a3265f9995d4a7ba49c3b488d45d5ebbc6c266ea0a5c810924aff1ad75f406b1df530f6593'

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
        'Authorization': f'Bearer {FASTPANEL_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(FASTPANEL_API_URL, headers=headers, json=payload, auth=auth)
        
        # Логирование статуса и текста ответа
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 201:
            bot.reply_to(message, f'Почтовый ящик {email} успешно создан с паролем {password}.')
        else:
            bot.reply_to(message, f'Ошибка при создании почтового ящика: {response.text}')
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f'Произошла ошибка при подключении к FastPanel API: {e}')

bot.polling()
