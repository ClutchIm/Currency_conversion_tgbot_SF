import telebot
from config import keys, TOKEN
from extensions import ApiException, CurrencyExchange

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_(message: telebot.types.Message):
    text = (''' Чтобы начать работу введите команду боту в следующем формате: 
    <имя валюты, цену которой вы хотите узнать> / 
    <имя валюты, в которой надо узнать цену первой валюты> / 
    <количество первой валюты>
    Увидеть список всех доступных валют: /values''')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise ApiException('Не верное количество параметров.')

        quote, base, amount = value
        total_base = CurrencyExchange.get_price(quote, base, amount)
    except ApiException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n {e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {round(total_base, 3)}'
        bot.send_message(message.chat.id, text)


bot.polling()
