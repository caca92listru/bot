import telebot
from config import keys,TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@ bot.message_handler(commands=['start','help'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду в формате:\n<имя ввалюты>\
<в какую валюту перевести> \
<количество>\n увидить список доступных валют: /values'
    bot.reply_to(message, text)

@ bot.message_handler(commands=['values'])
def values(message:telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text ='\n'.join((text, key))
    bot.reply_to(message, text)

@ bot.message_handler(content_types=['text'])
def convert(message:telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        queue, base, amount =values
        total_base = CryptoConverter.convert(queue, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'ошибка пользователя\n{e}')
    except Exception as e:
       bot.reply_to(message, f'не удалось обработать команду\n{e}')
    else:
        text = f'цена {amount} {queue} в {base} - {total_base * float(amount)}'
        bot.send_message(message.chat.id, text)



bot.polling(none_stop=True)
