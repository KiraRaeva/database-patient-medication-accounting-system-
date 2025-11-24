import sqlite3
import os

class AuthService:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_connection(self):
        """Создает соединение с базой данных"""
        try:
            db_dir = os.path.dirname(self.db_path)
            if not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
            return sqlite3.connect(self.db_path)
        except Exception as e:
            print(f"Ошибка подключения к базе: {e}")
            return None

    def medworker_login(self):
        """Авторизация медработника"""
        try:
            medworker_id = input("Введите ID медработника: ")
            password = input("Введите пароль: ")

            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM Medworker WHERE medworker_ID = ? AND password = ?', (medworker_id, password))
            medworker = cursor.fetchone()
            conn.close()

            if medworker:
                print(f"Добро пожаловать, {medworker[1]} {medworker[2]}!")
                return medworker[0]
            else:
                print("Неверный ID или пароль!")
                return None

        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
            return None

    def user_login(self):
        """Авторизация пациента"""
        try:
            user_id = input("Введите ID пациента: ")
            password = input("Введите пароль: ")

            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM User WHERE user_ID = ? AND password = ?', (user_id, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                print(f"Добро пожаловать, {user[1]} {user[2]}!")
                return user[0]
            else:
                print("Неверный ID или пароль!")
                return None

        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
            return None