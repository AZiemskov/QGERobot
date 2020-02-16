"""
dfghjklkjhgfghjk
"""
import telebot
from telebot.types import Message

import config
import past_to_shelve
from get_game_text_from_sqlite3 import SQLighter

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


@bot.message_handler(commands=['game'])
def game(message):
    # Подключаемся к БД
    db_worker = SQLighter(config.DATABASE_NAME)
    # Формируем разметку
    markup = past_to_shelve.generate_markup(row[4])
    # Отправляем аудиофайл с вариантами ответа
    bot.send_message(message.chat.id, row[3], reply_markup=markup)
    # Включаем "игровой режим"
    past_to_shelve.set_user_game(message.chat.id, row[2])
    # Отсоединяемся от БД
    db_worker.close()


@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    # Если функция возвращает None -> Человек не в игре
    answer = past_to_shelve.get_answer_for_user(message.chat.id)
    # Как Вы помните, answer может быть либо текст, либо None
    # Если None:
    if not answer:
        bot.send_message(message.chat.id, 'Чтобы начать игру, выберите команду /game')
    else:
        # Уберем клавиатуру с вариантами ответа.
        keyboard_hider = past_to_shelve.ReplyKeyboardRemove()
        # Если ответ правильный/неправильный
        if message.text == answer:
            bot.send_message(message.chat.id, 'Верно!', reply_markup=keyboard_hider)
        else:
            bot.send_message(message.chat.id, 'Увы, Вы не угадали. Попробуйте ещё раз!', reply_markup=keyboard_hider)
        # Удаляем юзера из хранилища (игра закончена)
        past_to_shelve.finish_user_game(message.chat.id)


if __name__ == '__main__':
    past_to_shelve.count_rows()
    bot.infinity_polling()
