from typing import List, Optional, Tuple
from docs.database import DatabaseManager

class ReceptionModel:
    """Модель для работы с таблицей приёмов лекарств"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def create_reception(self, is_good: bool, medical_prescription_id: int,
                        status: str = "pending", side_effects: str = "") -> int:
        """Создание записи о приёме лекарства"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Reception (is_good, side_effects, medical_prescription_ID, status)
                VALUES (?, ?, ?, ?)
            ''', (is_good, side_effects, medical_prescription_id, status))
            conn.commit()
            return cursor.lastrowid

    def update_reception_status(self, reception_id: int, status: str, side_effects: str = ""):
        """Обновление статуса приёма лекарства"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Reception SET status = ?, side_effects = ? WHERE reception_ID = ?
            ''', (status, side_effects, reception_id))
            conn.commit()

    def get_reception(self, reception_id: int) -> Optional[Tuple]:
        """Получение записи о приёме по ID"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Reception WHERE reception_ID = ?', (reception_id,))
            return cursor.fetchone()

    def get_receptions_by_prescription(self, prescription_id: int) -> List[Tuple]:
        """Получение всех записей о приёмах для назначения"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Reception WHERE medical_prescription_ID = ?', (prescription_id,))
            return cursor.fetchall()

    def get_receptions_by_user(self, user_id: int) -> List[Tuple]:
        """Получение всех записей о приёмах для пользователя"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT r.*, mp.medical_prescription_ID, m.nametag
                FROM Reception r
                JOIN Medical_prescription mp ON r.medical_prescription_ID = mp.medical_prescription_ID
                JOIN Medicine m ON mp.medicine_ID = m.medicine_ID
                WHERE mp.user_ID = ?
            ''', (user_id,))
            return cursor.fetchall()