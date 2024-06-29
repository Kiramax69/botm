
import random
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
import telebot
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name)

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
    
    driver = None  # Инициализация переменной driver

    try:
        driver = webdriver.Chrome(options=options)
        logger.info("WebDriver initialized successfully")
        
        # Navigate to the website
        logger.info("Navigating to the website")
        driver.get('https://sushivani.ru/menu/setyi/set-king-size')
        logger.info("Successfully navigated to the website")

        # Click the "ЗАКАЗАТЬ" button
        order_button = driver.find_element(By.XPATH, '//button[contains(text(), "ЗАКАЗАТЬ")]')
        order_button.click()

        # Click the "Корзина" link
        cart_link = driver.find_element(By.XPATH, '//a[contains(text(), "Корзина")]')
        cart_link.click()

        # Fill in the form with random data
        driver.find_element(By.NAME, 'name').send_keys(fake.name())
        driver.find_element(By.NAME, 'email').send_keys(fake.email())
        driver.find_element(By.NAME, 'phone').send_keys(fake.phone_number())
        driver.find_element(By.NAME, 'persons').send_keys(str(random.randint(1, 10)))
        driver.find_element(By.NAME, 'promo_code').send_keys('')  # leave blank if no promo code

        driver.find_element(By.NAME, 'street').send_keys(fake.street_name())
        driver.find_element(By.NAME, 'house').send_keys(str(random.randint(1, 100)))
        driver.find_element(By.NAME, 'building').send_keys('')  # leave blank if not applicable
        driver.find_element(By.NAME, 'entrance').send_keys(str(random.randint(1, 10)))
        driver.find_element(By.NAME, 'floor').send_keys(str(random.randint(1, 10)))
        driver.find_element(By.NAME, 'apartment').send_keys(str(random.randint(1, 100)))
        driver.find_element(By.NAME, 'order_time').send_keys('')  # leave blank if no specific time
        driver.find_element(By.NAME, 'order_notes').send_keys(fake.text())

        # Select payment method: "Банковская карта"
        card_payment = driver.find_element(By.XPATH, '//input[@value="card"]')
        card_payment.click()

        # Agree to the terms
        agree_terms = driver.find_element(By.XPATH, '//input[@name="agree_terms"]')
        agree_terms.click()

        # Confirm the order
        confirm_button = driver.find_element(By.XPATH, '//button[contains(text(), "ПОДТВЕРДИТЬ ЗАКАЗ")]')
        confirm_button.click()

        bot.reply_to(message, 'Order placed successfully!')

    except Exception as e:
        logger.error(f'An error occurred: {e}')
        bot.reply_to(message, f'An error occurred: {e}')

    finally:
        if driver:
            driver.quit()
            logger.info("WebDriver quit successfully")

# Start polling
bot.polling()
