import logging
import time

from telegram.ext import Updater, CommandHandler

t = time.localtime()
data = time.asctime(t)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5192637273:AAF9O-Gt_Xrk551BUvbi9nl3WYWQlNbnnnI'


def start(update, context):
        update.message.reply_text(
            "Я бот-Ассистент, Готов помочь по выбору игрушки 😉",)


def help(update, context):
        update.message.reply_text(
            
            "Выберите один из этих комманд"
            "\n 1: /Bestseller"
            "\n 2: /new_toys"
            "\n Я всегда рад вам всегда помочь 🥰")

def bestseller(update, context):
        update.message.reply_text(
            
            "Сейчас самыми популярными является эти игрушки 🤩"
            " "
            "")

def new_toys(update, context):
        update.message.reply_text(
            
            "Cписок новыx игрушок для вас 🤫"
            " "
            "")

def main():
    updater = Updater(TOKEN)


    dp = updater.dispatcher


    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("Bestseller", bestseller))
    dp.add_handler(CommandHandler("new_toys", new_toys))


    


    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()