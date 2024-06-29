import telebot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # Используем имя текущего модуля

# Initialize the Telegram bot
bot = telebot.TeleBot('7141698892:AAGMs0WFMADNOpGapquT42edJrXYbnSDDHc')

# Function to handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Use /order to place an order.")

# Function to handle the /order command
@bot.message_handler(commands=['order'])
def place_order(message):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no UI)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    driver = None  # Инициализация переменной driver

    try:
        service = Service('/path/to/chromedriver')  # Используем Service для указания пути к ChromeDriver
        driver = webdriver.Chrome(service=service, options=options)
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
