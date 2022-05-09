import logging
import time
from unicodedata import category

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
            
            "Выберите один из этих комманд 👏"
            "\n 1: /Bestseller"
            "\n 2: /new_toys"
            "\n 3: /categorys"
            "\n 4: /toysforboys"
            "\n 5: /toysforgirls"
            "\n 6: /educational"
            "\n 7: /heros"
            "\n Я всегда рад вам помочь 🥰")

def bestseller(update, context):
        update.message.reply_text(
            
            "Сейчас самыми популярными является эти игрушки 🤩"
            "\n 1: China toys мягкая игрушка хаги ваги, высота 40 см"
            "\n 2: Youmu Toys интерактивная игрушка ALF00016"
            "\n 3: Wooden Toys 88 Ксилофон Hand Knocks 88"
            "\n 4: Нестор-История мягкая игрушка Нестор, высота 120 см"
            "\n 5: Игровой коврик Mom_n_me 200x180 см, Облака"
            "\n 6: Huanger Piano HE0639"
            "\n 7: Toys мягкая игрушка Lalafanfan duck 123472KHH"
            )

def new_toys(update, context):
        update.message.reply_text(
            
            "Сейчас самыми популярными является эти игрушки 🤩"
            "\n 1: Budi Basa мягкая игрушка Зайка Ми, высота 34 см"
            "\n 2: Фигурка Funko Maleficent 12"
            "\n 3: Фигурка Funko Harley Quinn 12"
            "\n 4: Mary Poppins Само Совершенство 453185"
            "\n 5: Наша Игрушка Военный наборы оружия"
            "\n 6: Genio Kids игрушка-мялка Ам ням 559079, желтый, розовый,"
            "\n 7: Фигурка MAYA TOYS Orbeez Wow World 3"
            )

def categorys(update, context):
        update.message.reply_text(
            
            "У нас есть несколько котегорий которые может вам понравится😜"
            "\n 1: /new_toys"
            "\n 2: /toysforboys"
            "\n 3: /toysforgirls"
            "\n 4: /educational"
            "\n 5: /heros"
            )

def toysforboys(update, context):
        update.message.reply_text(
            
            "Любимые игрушки для пацанов 😎"
            "\n 1: Майнкруфт"
            "\n 2: Бравл Квас"
            "\n 3: Клэш Роялити"
            "\n 4: Гачи мучи"
            "\n 5: Хитпарат"
            "\n 6: Танк"
            "\n 7: Фортнаит батл пасс"
            )

def toysforgirls(update, context):
        update.message.reply_text(
            
            "Игрушки для девочек 🤮, лучше купи сыну🤧"
            "\n 1: Magic water 101112 Водная раскраска"
            "\n 2: Play Smart Счастливые животные 5097"
            "\n 3: QiYi Toys Кубик Рубика 3х3 Warrior W"
            "\n 4: Zhorya Зайчик 3 в 1 289043865"
            "\n 5: Wooden Toys удочки и спиннинги Магнитная рыбалка"
            "\n 6: ZERDE Пирамидка-сортер Геометрия"
            "\n 7: Wooden Toys 88 Ксилофон Hand Knocks 88"
            )

def educational(update, context):
        update.message.reply_text(
            
            "Игрушки для развития 🤓"
            "\n 1: Magic water 101112 Водная раскраска"
            "\n 2: Play Smart Счастливые животные 5097"
            "\n 3: QiYi Toys Кубик Рубика 3х3 Warrior W"
            "\n 4: Zhorya Зайчик 3 в 1 289043865"
            "\n 5: Wooden Toys удочки и спиннинги Магнитная рыбалка"
            "\n 6: ZERDE Пирамидка-сортер Геометрия"
            "\n 7: Wooden Toys 88 Ксилофон Hand Knocks 88"
            )

def heros(update, context):
        update.message.reply_text(
            
            "Любимые герои здесь 😎"
            "\n 1: Фигурка Funko Batman 25"
            "\n 2: Фигурка Funko Hulk 12"
            "\n 3: Фигурка Funko Stan Lee 12"
            "\n 4: Фигурка Funko Pain 10"
            "\n 5: Фигурка Funko Iron Man 12"
            "\n 6: Фигурка Funko Rat Fink 12"
            "\n 7: Фигурка MAYA TOYS Orbeez Wow World 3"
            )

def main():
    updater = Updater(TOKEN)


    dp = updater.dispatcher


    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("Bestseller", bestseller))
    dp.add_handler(CommandHandler("new_toys", new_toys))
    dp.add_handler(CommandHandler("categorys", categorys))
    dp.add_handler(CommandHandler("toysforboys", toysforboys))
    dp.add_handler(CommandHandler("toysforgirls", toysforgirls))
    dp.add_handler(CommandHandler("educational", educational))
    dp.add_handler(CommandHandler("heros", heros))



    updater.start_polling()

    updater.idle()


if __name__ == '__main__':  
    main()
