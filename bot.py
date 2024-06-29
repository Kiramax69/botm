import telebot
from telebot import types
import requests


from telebot import types



bot = telebot.TeleBot('1970145138:AAE0BxCzW-0PbbQKpF8sl0vjMKJbCaewZFs')
GOOGLE_API_KEY = 'AIzaSyBNTHIYzSDu2swXDL6qxHW0X1W-CoGcZyg'
CX = '8061ad7ffd11e4c56'


@bot.message_handler(commands=['start'])

def start(message):

    user = bot.get_me()

    userid = user.id

@bot.message_handler(commands=['delete'])
def delete(message):
    if message.reply_to_message:
        bot.delete_message(message.chat.id, message.reply_to_message.message_id)
    else:
        bot.send_message(message.chat.id, 'Нет сообщения для удаления.')
    

    

@bot.message_handler(commands=['donate'])

def donate(message):

    bot.send_message(message.chat.id, 'Хостинг не бесплатный донатить сюда :D\n\n Payeer: P1018613468', reply_markup=main())

    

@bot.message_handler(content_types=['text'])



def cont(message):



    if message.text == 'Го кс' or message.text == 'Кто кс' or message.text == 'кто кс' or message.text == 'го кс' or message.text == 'Кто кс?' or message.text == 'кто кс?' or message.text == 'kto ks'  or message.text == 'Kto ks' or message.text == 'Rnk rc' or message.text == 'rnk rc' or message.text == '/cs' or message.text == '@all':



        bot.send_message(message.chat.id, f' *Вызвал это меню:* @{message.from_user.username}\n\n @Asia51 @RunDelChaOs @prodcuddly @Shinigamiplay', parse_mode="Markdown")



        bot.send_message(message.chat.id, '@default_g @FreeManBek @Samuel725 @flatox')



        bot.send_message(message.chat.id,  '*Удалены из списка: \n@ Mr_Foxmal \n@ Humon_Sub*', parse_mode="Markdown")

        

    if message.text == 'марти' or message.text == 'Марти':

        

        bot.send_message(message.chat.id, 'У Марти маленький писюн!')

        

    if message.text == 'Тест' or message.text == 'тест':

        

        bot.send_message(message.chat.id, (f'@{message.from_user.username} Нигга'))

        

    if '@Kiramax' in message.text:

        bot.delete_message(message.chat.id, message.message_id)

        bot.send_message(message.chat.id,'Он не хочет что-бы его тегали.')

        

    if '@kiramax' in message.text:

        bot.delete_message(message.chat.id, message.message_id)

        bot.send_message(message.chat.id,'Он не хочет что-бы его тегали.')

@bot.inline_handler(lambda query: len(query.query) > 0)
def inline_query(query):
    try:
        search_query = query.query
        url = f"https://www.googleapis.com/customsearch/v1?q={search_query}&cx={CX}&key={GOOGLE_API_KEY}&searchType=image&num=10"
        response = requests.get(url)
        result = response.json()

        if 'items' in result:
            images = result['items']
            results = []
            for i, image in enumerate(images):
                results.append(types.InlineQueryResultPhoto(
                    id=str(i),
                    photo_url=image['link'],
                    thumb_url=image['link'],
                    caption=f'Image {i+1}'
                ))

            bot.answer_inline_query(query.id, results, cache_time=1)
        else:
            bot.answer_inline_query(query.id, [], switch_pm_text='Картинки не найдены', switch_pm_parameter='no_images')

    except Exception as e:
        print(e)

bot.polling()
