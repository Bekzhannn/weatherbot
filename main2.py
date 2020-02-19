# -*- coding: utf-8 -*-
import telebot
import pyowm
import urllib as urllib2
from googletrans import Translator


token = "690263322:AAH-3v6gvlCpcMFS0FNYtkoCnnVSV3IFWjw"

bot = telebot.TeleBot(token)


greetings = ["Privet", "Hello", "Zdrastvdui","Salamaleikum", ]
how_are_you = ["Otlishno", "Uzhasno", "Horowo", "Super","Poidet",]
bot = telebot.TeleBot("690263322:AAH-3v6gvlCpcMFS0FNYtkoCnnVSV3IsFWjw")

@bot.message_handler(commands=["weather"])
def weather(message):
    city = bot.send_message(message.chat.id, "V kakom gorode Vam pokazat pogodku?")
    bot.register_next_step_handler(city, weath)



@bot.message_handler(commands=["start"])
def handle_start(message):
    user_markup =telebot.types.ReplyKeyboardMarkup()
    user_markup.row('/start','/translate','/weather')
    user_markup.row('audio', 'photo',)
    bot.send_message(message.from_user.id,'Hello',reply_markup=user_markup)

@bot.message_handler(commands=["translate"])
def handle_start(message):
    user_markup =telebot.types.ReplyKeyboardMarkup()
    user_markup.row('/english','/russian','/start')
    bot.send_message(message.from_user.id,'what language do you want to translate ??. , на какой язык вы хотите перевести  ??.. ',reply_markup=user_markup)



@bot.message_handler(commands=["english"])
def handle_english(message):
    word = bot.send_message(message.chat.id, "Введите предложение для перевода")
    bot.register_next_step_handler(word, get_translater)


def get_translater(message):
    translator = Translator()
    translations = translator.translate(message.text, dest='en')  # dest - na kakoi yazyk perevesti nado (ru-russkii)
    output = translations.text
    bot.send_message(message.chat.id, output)

@bot.message_handler(commands=["russian"])
def handle_english(message):
    wor = bot.send_message(message.chat.id, "Введите предложение для перевод")
    bot.register_next_step_handler(wor, get_translate)


def get_translate(message):
    translator = Translator()
    translations = translator.translate(message.text, dest='ru')  # dest - na kakoi yazyk perevesti nado (ru-russkii)
    output = translations.text
    bot.send_message(message.chat.id, output)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text =='photo':
         url='https://goo.gl/58RCFF'
         urllib2.urlretrieve(url, 'url_image.jpg')
         img=open('url_image.jpg', 'rb')
         bot.send_chat_action(message.from_user.id, 'upload_photo')
         bot.send_photo(message.from_user.id, img)
         img.close()
    elif message.text == 'audio':
            audio = open("/Users/admin/Downloads/audio.mp3", 'rb')
            bot.send_chat_action(message.from_user.id, 'upload_audio')
            bot.send_audio(message.from_user.id, audio)
            audio.close()


def weath(message):
    owm = pyowm.OWM("9bada2f6f1939c15ffa6315235371194", language="ru")
    city = message.text
    weather = owm.weather_at_place(city)
    w = weather.get_weather()
    temperature = w.get_temperature("celsius")["temp"]
    wind = w.get_wind()["speed"]
    hum = w.get_humidity()
    desc = w.get_detailed_status()
    bot.send_message(message.chat.id, u' '.join((city,desc)).encode('utf-8') +
                     " Temperature: %d, Humidity: %d, Wind: %d m/s" % (temperature, hum, wind))




import time
if __name__ == "__main__":
    # bot.infinity_polling(True)
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print('Error in main: %s' % e)
            time.sleep(10)



