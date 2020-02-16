"""
Модуль берет текст игры из SQLite3
"""
import sqlite3


class SQLighter:
    """ Класс работает с БД """

    def __init__(self, database):
        """
        Конструктор класса
        :param database:
        """
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """
        Получаем все строки
        :return:
        """
        with self.connection:
            return self.cursor.execute('SELECT * FROM game_text').fetchall()

    def select_single(self, rownum):
        """
        Получаем одну строку с номером rownum
        :param rownum:
        :return:
        """
        with self.connection:
            return self.cursor.execute('SELECT * FROM game_text WHERE id = ?', (rownum,)).fetchall()[0]

    def count_rows(self):
        """
        Считаем количество строк
        :return: Возвращает длину переменной resalt
        """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM game_text').fetchall()
            return len(result)

    def close(self):
        """
        Закрываем текущее соединение с БД
        :return: None
        """
        self.connection.close()
