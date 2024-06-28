from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

# Установите свой токен бота Telegram
TELEGRAM_BOT_TOKEN = '6332761306:AAH08CnPCaNxIMTxqhGYts4ebX_nz1c75nM'

# URL и ключи для FastPanel API
FASTPANEL_API_URL = 'https://cv3909137.vps.regruhosting.ru:8888/vhosts/1/emails/1/boxes'
FASTPANEL_API_KEY = 'cd707aa8635689043f7be0a3265f9995d4a7ba49c3b488d45d5ebbc6c266ea0a5c810924aff1ad75f406b1df530f6593'

# Команда для создания почтового ящика
def create_email(update: Update, context: CallbackContext) -> None:
    # Получаем имя пользователя из сообщения
    username = context.args[0] if context.args else None
    
    if not username:
        update.message.reply_text('Пожалуйста, укажите имя пользователя для почтового ящика.')
        return
    
    domain = 'sukaa.ru'  # Ваш домен
    email = f"{username}@{domain}"
    password = 'temporary_password'  # Генерация временного пароля

    # Запрос на создание почтового ящика в FastPanel
    headers = {
        'Authorization': f'Bearer {FASTPANEL_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        "email": email,
        "password": password
    }
    
    response = requests.post(f'{FASTPANEL_API_URL}/mailboxes', headers=headers, json=payload)
    
    if response.status_code == 201:
        update.message.reply_text(f'Почтовый ящик {email} успешно создан с паролем {password}.')
    else:
        update.message.reply_text(f'Ошибка при создании почтового ящика: {response.text}')

def main():
    # Настройка бота
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    # Обработчик команды /create_email
    dispatcher.add_handler(CommandHandler('create_email', create_email))

    # Запуск бота
    updater.start_polling()

    updater.idle()

if name == 'main':
    main()
