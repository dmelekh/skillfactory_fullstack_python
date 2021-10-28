import re

import requests
import json
import telebot
from config import TOKEN
from config import API_KEY
from api_exception import APIException

'''
@SomeCurrencyBot
https://free.currencyconverterapi.com/
https://free.currencyconverterapi.com/free-api-key
https://corporatefinanceinstitute.com/resources/knowledge/economics/currency-pair/
all_available_currencies = {'ticker': {'currencyName':'...', 'currencySymbol':'...', 'id':'...'}}
'''

bot = telebot.TeleBot(TOKEN)


def exception_sending(decorated):
    def run_safe(*args, **kwargs):
        try:
            decorated(*args, **kwargs)
        except Exception as e:
            if len(args) > 0 and type(args[0]).__name__ == 'Message':
                bot.send_message(args[0].chat.id, f'{type(e).__name__}: {str(e)}')

    return run_safe


all_available_currencies: dict


def get_all_currencies():
    global all_available_currencies
    response = requests.get(f'https://free.currconv.com/api/v7/currencies?apiKey={API_KEY}')
    all_available_currencies = json.loads(response.content.decode('utf-8'))['results']
    # print(f'all currencies got!\n{all_available_currencies}')


def get_currency_pair(base, quote):
    pair = f'{base}_{quote}'
    response = requests.get(f'https://free.currconv.com/api/v7/convert?apiKey={API_KEY}&q={pair}&compact=y')
    result = json.loads(response.content.decode('utf-8'))[pair]['val']
    return result


def get_price(base, quote, amount):
    return round(float(get_currency_pair(base, quote)) * float(amount), 2)


@bot.message_handler(commands=['start', 'help'])
@exception_sending
def on_start_help(message):
    bot.send_message(message.chat.id,
                     "enter:\n"
                     "<base currency code> <quote currency code> <amount of base currency>\n or\n"
                     "/values - to get available currencies")


@bot.message_handler(commands=['values'])
@exception_sending
def on_values(message):
    global all_available_currencies
    tickers = [ticker for ticker in all_available_currencies]
    tickers.sort()
    answ = '\n'.join([f'{ticker}:  {all_available_currencies[ticker]["currencyName"]}' for ticker in tickers])
    bot.send_message(message.chat.id, answ)


@bot.message_handler(content_types=["text"])
@exception_sending
def on_message(message):
    global all_available_currencies
    regex = '^[a-zA-Z]{3} [a-zA-Z]{3} [\d]+[\.\,]?[\d]*$'
    if not re.match(regex, message.text):
        raise APIException(f'unknown input: {message.text}, try to use /help')
    message_parts = message.text.split()
    if message_parts[0] not in all_available_currencies or message_parts[1] not in all_available_currencies:
        raise APIException(f'unknown input: {message.text}, try to use /help')
    answ = f'{get_price(*message_parts)} {message_parts[1]}'
    bot.send_message(message.chat.id, answ)


if __name__ == '__main__':
    get_all_currencies()
    bot.polling(none_stop=True)
