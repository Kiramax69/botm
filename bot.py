import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Данные для входа в FastPanel
FASTPANEL_URL = 'https://cv3909137.vps.regruhosting.ru'
FASTPANEL_USERNAME = 'fastuser'
FASTPANEL_PASSWORD = 'Aeng7oi7sohv'

# Создание бота
bot = telebot.TeleBot(7141698892:AAG_euLwatIth9yFB7QXIkGCJtTac5Boh1k)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Используйте команду /create <username> для создания почтового ящика.")

@bot.message_handler(commands=['create'])
def create_email(message):
    try:
        username = message.text.split()[1]
    except IndexError:
        bot.reply_to(message, "Пожалуйста, укажите имя пользователя для почтового ящика. Пример: /create username")
        return
    
    domain = 'sukaa.ru'  # Ваш домен
    email = f"{username}@{domain}"
    password = 'temporary_password'  # Генерация временного пароля

    # Запуск браузера и выполнение действий
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(FASTPANEL_URL)
    
    # Ввод данных для входа
    driver.find_element(By.NAME, 'username').send_keys(FASTPANEL_USERNAME)
    driver.find_element(By.NAME, 'password').send_keys(FASTPANEL_PASSWORD)
    driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
    
    time.sleep(5)  # Дождаться загрузки панели
    
    # Нажать на кнопку "НОВЫЙ ЯЩИК"
    new_mailbox_button = driver.find_element(By.XPATH, '//button[text()="Новый ящик"]')
    new_mailbox_button.click()
    
    time.sleep(2)  # Дождаться открытия формы
    
    # Заполнение формы для создания нового почтового ящика
    driver.find_element(By.NAME, 'email').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.NAME, 'password_confirm').send_keys(password)
    
    # Нажать на кнопку для сохранения нового почтового ящика
    save_button = driver.find_element(By.XPATH, '//button[text()="Сохранить"]')
    save_button.click()
    
    time.sleep(2)  # Дождаться создания почтового ящика
    
    driver.quit()
    bot.reply_to(message, f'Почтовый ящик {email} успешно создан с паролем {password}.')
    
bot.polling()
