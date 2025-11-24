import sqlite3
import os


class MedworkerService:
    def __init__(self, db_path, medworker_id):
        self.db_path = db_path
        self.medworker_id = medworker_id

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

    def show_all_patients(self):
        """Показать всех пациентов"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                'SELECT user_ID, first_name, second_name, date_of_birth, contraindications, individual_characteristics FROM User ORDER BY user_ID')
            patients = cursor.fetchall()

            print("\n" + "=" * 70)
            print("СПИСОК ВСЕХ ПАЦИЕНТОВ")
            print("=" * 70)
            for patient in patients:
                print(f"ID: {patient[0]}")
                print(f"ФИО: {patient[1]} {patient[2]}")
                print(f"Дата рождения: {patient[3]}")
                print(f"Противопоказания: {patient[4]}")
                print(f"Симптомы и особенности: {patient[5]}")
                print("-" * 50)

            conn.close()

        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")

    def show_patient_prescriptions(self):
        """Показать назначения пациента"""
        try:
            patient_id = input("Введите ID пациента: ")

            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT mp.medical_prescription_ID, m.nametag, mp.dosage, mp.start_time, mp.end_time
                FROM Medical_prescription mp
                JOIN Medicine m ON mp.medicine_ID = m.medicine_ID
                WHERE mp.user_ID = ?
            ''', (patient_id,))

            prescriptions = cursor.fetchall()

            print(f"\nНазначения для пациента ID {patient_id}:")
            print("=" * 60)
            for prescription in prescriptions:
                print(f"ID назначения: {prescription[0]}")
                print(f"Препарат: {prescription[1]}")
                print(f"Дозировка: {prescription[2]}")
                print(f"Период: с {prescription[3]} по {prescription[4]}")
                print("-" * 40)

            conn.close()

        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")

    def modify_prescription(self):
        """Изменить назначение"""
        try:
            # Показываем список пациентов
            print("\nСписок пациентов:")
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT user_ID, first_name, second_name FROM User ORDER BY user_ID')
            patients = cursor.fetchall()

            for patient in patients:
                print(f"ID: {patient[0]}, ФИО: {patient[1]} {patient[2]}")

            patient_id = input("\nВведите ID пациента: ")

            # Проверяем пациента
            cursor.execute('SELECT first_name, second_name FROM User WHERE user_ID = ?', (patient_id,))
            patient_info = cursor.fetchone()

            if not patient_info:
                print("Пациент не найден!")
                conn.close()
                return

            print(f"\nПациент: {patient_info[0]} {patient_info[1]}")

            # Показываем назначения пациента
            cursor.execute('''
                SELECT mp.medical_prescription_ID, m.nametag, mp.dosage, mp.start_time, mp.end_time
                FROM Medical_prescription mp
                JOIN Medicine m ON mp.medicine_ID = m.medicine_ID
                WHERE mp.user_ID = ?
            ''', (patient_id,))

            prescriptions = cursor.fetchall()

            if not prescriptions:
                print("У пациента нет назначений!")
                conn.close()
                return

            print("\nНазначения пациента:")
            print("=" * 60)
            for prescription in prescriptions:
                print(f"ID назначения: {prescription[0]}")
                print(f"Препарат: {prescription[1]}")
                print(f"Дозировка: {prescription[2]}")
                print(f"Период: с {prescription[3]} по {prescription[4]}")
                print("-" * 40)

            prescription_id = input("\nВведите ID назначения для изменения: ")

            # Получаем информацию о назначении
            cursor.execute('''
                SELECT mp.*, m.nametag 
                FROM Medical_prescription mp 
                JOIN Medicine m ON mp.medicine_ID = m.medicine_ID 
                WHERE mp.medical_prescription_ID = ? AND mp.user_ID = ?
            ''', (prescription_id, patient_id))

            prescription = cursor.fetchone()

            if not prescription:
                print("Назначение не найдено у данного пациента!")
                conn.close()
                return

            print("\nТекущие данные назначения:")
            print(f"ID назначения: {prescription[0]}")
            print(f"Препарат: {prescription[6]} (ID: {prescription[5]})")
            print(f"Дозировка: {prescription[1]}")
            print(f"Начало: {prescription[2]}")
            print(f"Конец: {prescription[3]}")

            # Показываем доступные препараты
            print("\nДоступные препараты:")
            cursor.execute('SELECT medicine_ID, nametag, dosage FROM Medicine')
            medicines = cursor.fetchall()
            for med in medicines:
                print(f"ID: {med[0]}, Название: {med[1]}, Дозировка: {med[2]}")

            print("\nЧто вы хотите изменить?")
            print("1. Препарат")
            print("2. Дозировку")
            print("3. Период приема")
            print("4. Отменить назначение")

            choice = input("Выберите действие: ")

            if choice == '1':
                new_medicine_id = input("Введите новый ID препарата: ")
                cursor.execute('UPDATE Medical_prescription SET medicine_ID = ? WHERE medical_prescription_ID = ?',
                               (new_medicine_id, prescription_id))
                print("Препарат изменен!")
            elif choice == '2':
                new_dosage = input("Введите новую дозировку: ")
                cursor.execute('UPDATE Medical_prescription SET dosage = ? WHERE medical_prescription_ID = ?',
                               (new_dosage, prescription_id))
                print("Дозировка изменена!")
            elif choice == '3':
                new_start = input("Введите новое время начала (ГГГГ-ММ-ДД ЧЧ:ММ:СС): ")
                new_end = input("Введите новое время окончания (ГГГГ-ММ-ДД ЧЧ:ММ:СС): ")
                cursor.execute(
                    'UPDATE Medical_prescription SET start_time = ?, end_time = ? WHERE medical_prescription_ID = ?',
                    (new_start, new_end, prescription_id))
                print("Период приема изменен!")
            elif choice == '4':
                cursor.execute('DELETE FROM Medical_prescription WHERE medical_prescription_ID = ?', (prescription_id,))
                cursor.execute('DELETE FROM Reception WHERE medical_prescription_ID = ?', (prescription_id,))
                print("Назначение отменено!")
            else:
                print("Неверный выбор!")
                conn.close()
                return

            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")

    def add_medical_history(self):
        """Добавить историю болезни"""
        try:
            patient_id = input("Введите ID пациента: ")
            medical_history = input("Введите историю болезни: ")

            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                'UPDATE User SET individual_characteristics = individual_characteristics || ? WHERE user_ID = ?',
                (f"; История болезни: {medical_history}", patient_id))

            conn.commit()
            conn.close()
            print("История болезни добавлена!")

        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")

    def add_individual_characteristics(self):
        """Добавить индивидуальные особенности"""
        try:
            patient_id = input("Введите ID пациента: ")
            characteristics = input("Введите индивидуальные особенности: ")

            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                'UPDATE User SET individual_characteristics = individual_characteristics || ? WHERE user_ID = ?',
                (f"; {characteristics}", patient_id))

            conn.commit()
            conn.close()
            print("Индивидуальные особенности добавлены!")

        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")

    def create_new_prescription(self):
        """Создать новое назначение"""
        try:
            patient_id = input("Введите ID пациента: ")

            print("\nДоступные препараты:")
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT medicine_ID, nametag, dosage FROM Medicine')
            medicines = cursor.fetchall()
            for med in medicines:
                print(f"ID: {med[0]}, {med[1]} - {med[2]}")

            medicine_id = input("Введите ID препарата: ")
            dosage = input("Введите дозировку: ")
            start_time = input("Введите время начала (ГГГГ-ММ-ДД ЧЧ:ММ:СС): ")
            end_time = input("Введите время окончания (ГГГГ-ММ-ДД ЧЧ:ММ:СС): ")

            cursor.execute('''
                INSERT INTO Medical_prescription (dosage, start_time, end_time, user_ID, medworker_ID, medicine_ID)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (dosage, start_time, end_time, patient_id, self.medworker_id, medicine_id))

            conn.commit()
            conn.close()
            print("Новое назначение создано!")

        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")

    def show_medication_status(self):
        """Показать статус приема препаратов"""
        try:
            patient_id = input("Введите ID пациента: ")

            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT mp.medical_prescription_ID, m.nametag, mp.dosage, 
                       r.is_good, r.side_effects, r.taken_time
                FROM Medical_prescription mp
                JOIN Medicine m ON mp.medicine_ID = m.medicine_ID
                LEFT JOIN Reception r ON mp.medical_prescription_ID = r.medical_prescription_ID
                WHERE mp.user_ID = ?
            ''', (patient_id,))

            medications = cursor.fetchall()

            print(f"\nСтатус приема препаратов для пациента ID {patient_id}:")
            print("=" * 80)
            for med in medications:
                status = "ПРИНЯТО" if med[3] is not None and med[3] else "НЕ ПРИНЯТО"
                if med[3] is not None and not med[3]:
                    status = "ПРОПУЩЕНО"

                side_effects = med[4] if med[4] else "Нет побочных эффектов"
                taken_time = med[5] if med[5] else "Не принято"

                print(f"Препарат: {med[1]}")
                print(f"Дозировка: {med[2]}")
                print(f"Статус: {status}")
                print(f"Побочные эффекты: {side_effects}")
                print(f"Время приема: {taken_time}")
                print("-" * 50)

            conn.close()

        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")

    def show_patient_medical_card(self):
        """Просмотр медицинской карты пациента"""
        try:
            patient_id = input("Введите ID пациента: ")

            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                'SELECT user_ID, first_name, second_name, date_of_birth, contraindications, individual_characteristics FROM User WHERE user_ID = ?',
                (patient_id,))
            patient = cursor.fetchone()

            if not patient:
                print("Пациент не найден!")
                conn.close()
                return

            print("\n" + "=" * 70)
            print("МЕДИЦИНСКАЯ КАРТА ПАЦИЕНТА")
            print("=" * 70)
            print(f"ID пациента: {patient[0]}")
            print(f"ФИО: {patient[1]} {patient[2]}")
            print(f"Дата рождения: {patient[3]}")
            print(f"Противопоказания: {patient[4]}")
            print(f"Индивидуальные особенности и симптомы: {patient[5]}")
            print("-" * 70)

            # Текущие назначения
            cursor.execute('''
                SELECT m.nametag, mp.dosage, mp.start_time, mp.end_time
                FROM Medical_prescription mp
                JOIN Medicine m ON mp.medicine_ID = m.medicine_ID
                WHERE mp.user_ID = ? AND datetime('now') BETWEEN mp.start_time AND mp.end_time
            ''', (patient_id,))

            current_prescriptions = cursor.fetchall()

            print("\nТЕКУЩИЕ НАЗНАЧЕНИЯ:")
            if current_prescriptions:
                for prescription in current_prescriptions:
                    print(f"  Препарат: {prescription[0]}")
                    print(f"  Дозировка: {prescription[1]}")
                    print(f"  Период: с {prescription[2]} по {prescription[3]}")
                    print("  " + "-" * 40)
            else:
                print("  Нет текущих назначений")

            # История приема
            cursor.execute('''
                SELECT m.nametag, r.taken_time, r.is_good, r.side_effects
                FROM Reception r
                JOIN Medical_prescription mp ON r.medical_prescription_ID = mp.medical_prescription_ID
                JOIN Medicine m ON mp.medicine_ID = m.medicine_ID
                WHERE mp.user_ID = ?
                ORDER BY r.taken_time DESC
            ''', (patient_id,))

            reception_history = cursor.fetchall()

            print("\nИСТОРИЯ ПРИЕМА ПРЕПАРАТОВ:")
            if reception_history:
                for reception in reception_history:
                    status = "Принято" if reception[2] else "Пропущено"
                    print(f"  Препарат: {reception[0]}")
                    print(f"  Время: {reception[1]}")
                    print(f"  Статус: {status}")
                    print(f"  Побочные эффекты: {reception[3]}")
                    print("  " + "-" * 40)
            else:
                print("  Нет данных о приеме препаратов")

            # Статистика
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_prescriptions,
                    SUM(CASE WHEN r.is_good = 1 THEN 1 ELSE 0 END) as taken_count,
                    SUM(CASE WHEN r.is_good = 0 THEN 1 ELSE 0 END) as missed_count
                FROM Medical_prescription mp
                LEFT JOIN Reception r ON mp.medical_prescription_ID = r.medical_prescription_ID
                WHERE mp.user_ID = ?
            ''', (patient_id,))

            stats = cursor.fetchone()

            print("\nСТАТИСТИКА ПРИЕМА:")
            print(f"  Всего назначений: {stats[0]}")
            print(f"  Принято препаратов: {stats[1]}")
            print(f"  Пропущено препаратов: {stats[2]}")

            if stats[0] > 0:
                compliance_rate = (stats[1] / stats[0]) * 100
                print(f"  Соблюдение режима: {compliance_rate:.1f}%")

            print("=" * 70)
            conn.close()

        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")