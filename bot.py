import random
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import telebot

fake = Faker()

# Initialize the Telegram bot
bot = telebot.TeleBot('7141698892:AAG_euLwatIth9yFB7QXIkGCJtTac5Boh1k')

# Function to handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Use /order to place an order.")

# Function to handle the /order command
@bot.message_handler(commands=['order'])
def place_order(message):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no UI)
    driver = webdriver.Chrome(options=options)
        # Navigate to the website
        driver.get('https://sushivani.ru/menu/setyi/set-king-size')

        # Click the "ЗАКАЗАТЬ" button
        order_button = driver.find_element(By.XPATH, '//button[contains(text(), "ЗАКАЗАТЬ")]')
        order_button.click()



bot.polling()
