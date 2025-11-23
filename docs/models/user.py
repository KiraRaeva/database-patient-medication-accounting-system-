from typing import List, Optional, Tuple
from docs.database import DatabaseManager

class UserModel:
    """Модель для работы с таблицей пользователей"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def create_user(self, first_name: str, second_name: str, date_of_birth: str,
                   login: str, password: str,
                   contraindications: str = "", individual_characteristics: str = "") -> int:
        """Создание нового пользователя"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO User (first_name, second_name, date_of_birth, contraindications, 
                                individual_characteristics, login, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (first_name, second_name, date_of_birth, contraindications,
                  individual_characteristics, login, password))
            conn.commit()
            return cursor.lastrowid

    def authenticate(self, login: str, password: str) -> Optional[Tuple]:
        """Аутентификация пользователя"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM User WHERE login = ? AND password = ?', (login, password))
            return cursor.fetchone()

    def get_user(self, user_id: int) -> Optional[Tuple]:
        """Получение пользователя по ID"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM User WHERE user_ID = ?', (user_id,))
            return cursor.fetchone()

    def get_all_users(self) -> List[Tuple]:
        """Получение всех пользователей"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT user_ID, first_name, second_name, date_of_birth FROM User')
            return cursor.fetchall()

    def update_user(self, user_id: int, **kwargs):
        """Обновление данных пользователя"""
        if not kwargs:
            return

        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values())
        values.append(user_id)

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'UPDATE User SET {set_clause} WHERE user_ID = ?', values)
            conn.commit()

    def update_individual_data(self, user_id: int, individual_characteristics: str):
        """Обновление индивидуальных данных пользователя"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE User SET individual_characteristics = ? WHERE user_ID = ?
            ''', (individual_characteristics, user_id))
            conn.commit()