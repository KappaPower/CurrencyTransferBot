import telebot
from config import keys, TOKEN
from extensions import CurrencyTransfer, ConversionExeption

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/start', '/help', '/values')
    bot.send_message(message.chat.id, 'Выбери, что интересует', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def handle_start_help(message: telebot.types.Message):
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name}.\nВведи данные через пробел, например\nдоллар рубль 12'
                     f'\nКнопка /values для списка доступных валют')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    global keys
    text = "Валюты:"
    for keys in keys.keys():
        text = '\n'.join((text, keys,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    value = message.text.split(' ')
    try:
        if len(value) != 3:
            raise ConversionExeption('Неверное количество параметров')
        quote, base, amount = value
        total_base = CurrencyTransfer.convert(quote, base, amount)

    except ConversionExeption as c:
        bot.reply_to(message, c)

    else:
        bot.reply_to(message, total_base)


bot.polling(none_stop=True)
