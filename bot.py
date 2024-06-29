
import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    
    driver = None  # Инициализация переменной driver

    try:
        driver = webdriver.Chrome(options=options)
        logger.info("WebDriver initialized successfully")
        
        # Navigate to the website
        logger.info("Navigating to the website")
        driver.get('https://sushivani.ru/menu/setyi/set-king-size')
        logger.info("Successfully navigated to the website")

        # Find the "ЗАКАЗАТЬ" button
        order_button = driver.find_element(By.XPATH, '//button[contains(text(), "ЗАКАЗАТЬ")]')
        
        if order_button:
            bot.reply_to(message, 'Button "ЗАКАЗАТЬ" found!')
            logger.info('Button "ЗАКАЗАТЬ" found!')
        else:
            bot.reply_to(message, 'Button "ЗАКАЗАТЬ" not found!')
            logger.info('Button "ЗАКАЗАТЬ" not found!')

    except Exception as e:
        logger.error(f'An error occurred: {e}')
        bot.reply_to(message, f'An error occurred: {e}')

    finally:
        if driver:
            driver.quit()
            logger.info("WebDriver quit successfully")

# Start polling
bot.polling()
