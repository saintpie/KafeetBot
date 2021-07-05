# импортируем нужные библиотеки
import requests
from datetime import datetime
import telebot
# Импортируем токен, бота
from token_value import token


# Создаём функцию - запрос
def get_data():
    req = requests.get("https://yobit.net/api/3/ticker/btc_usd")
    response = req.json()  # Создаём переменную в которую будем выводить JSON формат
    sell_price = response["btc_usd"]["sell"]  # Создаём переменную, в которую присваеваем нужные компоненты JSON формата
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nSell BTC price: {sell_price}")  # Выводим информацию


# Создаём декоратор функцией, самого бота, принимающию токен
def telegram_bot(token):
    bot = telebot.TeleBot(token)

    # Создём декоратор с функцией приветсвия бота
    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Hello friend! Print: 'price' to find out the BTС cost")

    # Создём декоратор с функцией, которая выводит информацию
    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if message.text.lower() == "price":
            try:  # Создаём блок try, except для выявления ошибок
                req = requests.get("https://yobit.net/api/3/ticker/btc_usd")
                response = req.json()
                sell_price = response["btc_usd"]["sell"]
                bot.send_message(
                    message.chat.id,
                    f"{datetime.now().strftime('Date: %Y-%m-%d %H:%M')}\nBTC price: {sell_price}"
                )
            except Exception as ex:  # Вывод сообщения при каких-либо ошибках
                print(ex)
                bot.send_message(
                    message.chat.id,
                    "Looks like we have some problems. Please try again later"
                )
        else:  # Вывод сообщения при некорректной команде
            bot.send_message(message.chat.id, "Wrong command!")

    bot.polling()


# Создаём условие, затем и происходит сам запуск бота
if __name__ == '__main__':
    # get_data()
    telegram_bot(token)
