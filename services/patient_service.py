import sqlite3
import os


class PatientService:
    def __init__(self, db_path, user_id):
        self.db_path = db_path
        self.user_id = user_id

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

    def mark_wellbeing(self):
        """Отметить самочувствие после препарата"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT mp.medical_prescription_ID, m.nametag
                FROM Medical_prescription mp
                JOIN Medicine m ON mp.medicine_ID = m.medicine_ID
                WHERE mp.user_ID = ?
            ''', (self.user_id,))

            prescriptions = cursor.fetchall()

            print("\nВаши назначения:")
            for pres in prescriptions:
                print(f"ID: {pres[0]}, Препарат: {pres[1]}")

            prescription_id = input("Введите ID назначения: ")
            is_good = input("Хорошее самочувствие? (да/нет): ").lower() == 'да'
            side_effects = input("Опишите побочные эффекты (если есть): ")

            cursor.execute('''
                INSERT INTO Reception (is_good, side_effects, taken_time, medical_prescription_ID)
                VALUES (?, ?, datetime('now'), ?)
            ''', (is_good, side_effects, prescription_id))

            conn.commit()
            conn.close()
            print("Самочувствие отмечено!")

        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")

    def confirm_medication(self):
        """Подтвердить прием препаратов"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT mp.medical_prescription_ID, m.nametag, mp.dosage
                FROM Medical_prescription mp
                JOIN Medicine m ON mp.medicine_ID = m.medicine_ID
                WHERE mp.user_ID = ? AND datetime('now') BETWEEN mp.start_time AND mp.end_time
            ''', (self.user_id,))

            current_meds = cursor.fetchall()

            print("\nТекущие назначения для приема:")
            for med in current_meds:
                print(f"ID: {med[0]}, Препарат: {med[1]}, Дозировка: {med[2]}")

            prescription_id = input("Введите ID назначения для подтверждения: ")
            action = input("Принять препарат или пропустить? (принять/пропустить): ")

            if action == 'принять':
                cursor.execute('''
                    INSERT INTO Reception (is_good, side_effects, taken_time, medical_prescription_ID)
                    VALUES (?, ?, datetime('now'), ?)
                ''', (True, "Принято по расписанию", prescription_id))
                print("Прием препарата подтвержден!")
            elif action == 'пропустить':
                reason = input("Причина пропуска: ")
                cursor.execute('''
                    INSERT INTO Reception (is_good, side_effects, taken_time, medical_prescription_ID)
                    VALUES (?, ?, datetime('now'), ?)
                ''', (False, f"Пропуск: {reason}", prescription_id))
                print("Пропуск препарата отмечен!")

            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")

    def view_prescriptions(self):
        """Посмотреть назначенные препараты"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT m.nametag, mp.dosage, mp.start_time, mp.end_time
                FROM Medical_prescription mp
                JOIN Medicine m ON mp.medicine_ID = m.medicine_ID
                WHERE mp.user_ID = ?
            ''', (self.user_id,))

            prescriptions = cursor.fetchall()

            print("\nВаши назначенные препараты:")
            print("=" * 60)
            for prescription in prescriptions:
                print(f"Препарат: {prescription[0]}")
                print(f"Дозировка: {prescription[1]}")
                print(f"Период приема: с {prescription[2]} по {prescription[3]}")
                print("-" * 40)

            conn.close()

        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")