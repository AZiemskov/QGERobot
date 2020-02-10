"""
dfghjklkjhgfghjk
"""
import telebot
from telebot.types import Message

import config
import get_game_text_from_sqlite3
import inline_keyboard_button

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message: Message):
    """
    :param message:
    :return:
    """
    bot.send_message(
        message.chat.id,
        "Привет первый игрок, {}".format(message.chat.first_name, message.text)
    )


@bot.message_handler(content_types=["text"], func=lambda message: True)
def start_game_text(message: Message):
    """
    :param message:
    :return:
    """
    bot.send_message(
        message.chat.id,
        get_game_text_from_sqlite3.PIZZA["start game"].format(message.chat.first_name, message.text),
        reply_markup=inline_keyboard_button.get_base_inline_keyboard()
    )


if __name__ == "__main__":
    bot.infinity_polling()
