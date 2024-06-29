import telebot
import requests
import re

bot = telebot.TeleBot('1970145138:AAE0BxCzW-0PbbQKpF8sl0vjMKJbCaewZFs')
GOOGLE_API_KEY = 'AIzaSyBNTHIYzSDu2swXDL6qxHW0X1W-CoGcZyg'
CX = '8061ad7ffd11e4c56'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Бот группы Co-Op CS:GO')

@bot.message_handler(commands=['delete'])
def delete(message):
    if message.reply_to_message:
        bot.delete_message(message.chat.id, message.reply_to_message.message_id)
    else:
        bot.send_message(message.chat.id, 'Нет сообщения для удаления.')

@bot.message_handler(commands=['donate'])
def donate(message):
    bot.send_message(message.chat.id, 'Хостинг не бесплатный донатить сюда :D\n\n Payeer: P1018613468')

@bot.message_handler(content_types=['text'])
def cont(message):
    cs_phrases = [
        'Го кс', 'Кто кс', 'кто кс', 'го кс', 
        'Кто кс?', 'кто кс?', 'kto ks', 'Kto ks', 
        'Rnk rc', 'rnk rc', '/cs'
    ]
    
    all_phrases = ['@all', '@All', '@ALL', '@aLL', 'алл', 'Алл']
    
    if message.text in cs_phrases:
        send_csgo_invite(message)
    elif message.text in all_phrases:
        send_all_invite(message)
    elif re.search(r'(?i)марти', message.text):
        bot.send_message(message.chat.id, 'У Марти маленький писюн!')
    elif re.search(r'(?i)тест', message.text):
        bot.send_message(message.chat.id, f'@{message.from_user.username} Нигга')
    elif re.search(r'@kiramax', message.text, re.IGNORECASE):
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, 'Он не хочет что-бы его тегали.')
    elif re.search(r'(?i)^найди (.+)', message.text):
        search_images(message)
    else:
        pass

def send_csgo_invite(message):
    bot.send_message(message.chat.id, f' *Позвал в коес:* @{message.from_user.username}\n\n @Asia51 @RunDelChaOs @prodcuddly @Shinigamiplay', parse_mode="Markdown")
    bot.send_message(message.chat.id, '@default_g @FreeManBek @Samuel725 @flatox')
    bot.send_message(message.chat.id,  '*Временно не катают: \n@Mr_Foxmal \n@Humon_Sub*', parse_mode="Markdown")

def send_all_invite(message):
    bot.send_message(message.chat.id, f' *Вызвал это меню:* @{message.from_user.username}\n\n @Asia51 @RunDelChaOs @prodcuddly @Shinigamiplay', parse_mode="Markdown")
    bot.send_message(message.chat.id, '@default_g @FreeManBek @Samuel725 @flatox @Mr_Foxmal @Humon_Sub', parse_mode="Markdown")

def search_images(message):
    search_query = re.search(r'(?i)^найди (.+)', message.text).group(1)
    url = f"https://www.googleapis.com/customsearch/v1?q={search_query}&cx={CX}&key={GOOGLE_API_KEY}&searchType=image&num=20"
    response = requests.get(url)
    result = response.json()

    if 'items' in result:
        images = [item['link'] for item in result['items']]
        send_image_options(message, images)
    else:
        bot.send_message(message.chat.id, 'Картинки не найдены.')

def send_image_options(message, images):
    markup = telebot.types.InlineKeyboardMarkup()
    for i, image_url in enumerate(images):
        markup.add(telebot.types.InlineKeyboardButton(text=f'Изображение {i+1}', callback_data=image_url))
    bot.send_message(message.chat.id, 'Выберите изображение для отправки:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data:
        bot.send_photo(call.message.chat.id, call.data)
        bot.answer_callback_query(call.id)

bot.polling()
