import telebot
import pyowm

from pyowm import OWM
from pyowm.commons import exceptions
from pyowm.utils.config import get_default_config
from pyowm.utils import timestamps

config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = OWM('e0e46e5fac8a3a3984cb3c2beb748cb3', config_dict)
mgr = owm.weather_manager()

bot = telebot.TeleBot("1486700928:AAG8MdMz8EfMqFSDbQshbHq15Mhdav0wqWY", parse_mode=None)

@bot.message_handler(content_types=['text'])
def send_echo(message):
    try:
        observation = mgr.weather_at_place(message.text)
        w = observation.weather
        temp = w.temperature('celsius')["temp"]

        answer = "В городе " + message.text + " сейчас " + w.detailed_status + "\n"
        answer += "Температура около " + str(temp) + "градусов Цельсия" + "\n\n"

        if temp < -5:
            answer += "Даже для зимы прохладно, одевайся теплее!!!"
        elif temp < 0:
            answer += "Зима на дворе, а ты что хотел? Оденься как обычно!"
        else:
            answer += "Кайф, такая погодка зимой!"

        bot.send_message(message.chat.id, answer + "\n\nНапиши мне в личку)")

    except pyowm.commons.exceptions.NotFoundError:
        bot.send_message(message.chat.id, 'Введите город: ')

bot.polling(none_stop = True)