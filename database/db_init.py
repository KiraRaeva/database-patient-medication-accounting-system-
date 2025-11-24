import sqlite3
import os


class DatabaseInitializer:
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

    def create_tables(self):
        """Создает все необходимые таблицы"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS User (
                    user_ID INTEGER PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    second_name TEXT NOT NULL,
                    date_of_birth DATETIME,
                    contraindications TEXT,
                    individual_characteristics TEXT,
                    password TEXT NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Medworker (
                    medworker_ID INTEGER PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    second_name TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Medicine (
                    medicine_ID INTEGER PRIMARY KEY,
                    nametag TEXT NOT NULL,
                    dosage TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Medical_prescription (
                    medical_prescription_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    dosage TEXT,
                    start_time DATETIME,
                    end_time DATETIME,
                    user_ID INTEGER,
                    medworker_ID INTEGER,
                    medicine_ID INTEGER,
                    FOREIGN KEY (user_ID) REFERENCES User(user_ID),
                    FOREIGN KEY (medworker_ID) REFERENCES Medworker(medworker_ID),
                    FOREIGN KEY (medicine_ID) REFERENCES Medicine(medicine_ID)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Reception (
                    reception_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    is_good BOOLEAN,
                    side_effects TEXT,
                    taken_time DATETIME,
                    medical_prescription_ID INTEGER,
                    FOREIGN KEY (medical_prescription_ID) REFERENCES Medical_prescription(medical_prescription_ID)
                )
            ''')

            conn.commit()
            conn.close()
            print("Таблицы базы данных созданы успешно!")

        except sqlite3.Error as e:
            print(f"Ошибка создания таблиц: {e}")

    def create_test_data(self):
        """Создает тестовые данные"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Медработник
            medworker = (111, 'Иван', 'Петров', '111222')
            cursor.execute('SELECT * FROM Medworker WHERE medworker_ID = ?', (medworker[0],))
            if not cursor.fetchone():
                cursor.execute(
                    'INSERT INTO Medworker (medworker_ID, first_name, second_name, password) VALUES (?, ?, ?, ?)',
                    medworker)

            # Пациенты
            users = [
                (1, 'Алексей', 'Смирнов', '1985-05-15', 'Аллергия на пенициллин',
                 'Симптомы: высокая температура 38.5°C, головная боль, боль в горле', '111'),
                (2, 'Мария', 'Иванова', '1990-08-20', 'Беременность',
                 'Симптомы: температура 37.8°C, насморк, кашель, слабость', '222')
            ]

            for user in users:
                cursor.execute('SELECT * FROM User WHERE user_ID = ?', (user[0],))
                if not cursor.fetchone():
                    cursor.execute(
                        'INSERT INTO User (user_ID, first_name, second_name, date_of_birth, contraindications, individual_characteristics, password) VALUES (?, ?, ?, ?, ?, ?, ?)',
                        user)

            # Лекарства
            medicines = [
                (1, 'Парацетамол', '500 мг 3 раза в день после еды'),
                (2, 'Ибупрофен', '400 мг 2 раза в день при температуре выше 38°C'),
                (3, 'ТераФлю', '1 пакетик 2-3 раза в день при симптомах простуды'),
                (4, 'Стрепсилс', '1 пастилка каждые 2-3 часа при боли в горле'),
                (5, 'Називин', '2 капли в каждый носовой ход 3 раза в день'),
                (6, 'Амбробене', '1 таблетка 3 раза в день от кашля'),
                (7, 'Аскорбиновая кислота', '500 мг 1 раз в день для иммунитета'),
                (8, 'Антигриппин', '1 таблетка 2-3 раза в день')
            ]

            for medicine in medicines:
                cursor.execute('SELECT * FROM Medicine WHERE medicine_ID = ?', (medicine[0],))
                if not cursor.fetchone():
                    cursor.execute('INSERT INTO Medicine (medicine_ID, nametag, dosage) VALUES (?, ?, ?)', medicine)

            # Назначения
            prescriptions = [
                (1, '1 таблетка', '2025-01-20 08:00:00', '2025-01-27 20:00:00', 1, 111, 1),
                (2, '1 таблетка', '2025-01-20 12:00:00', '2025-01-25 12:00:00', 1, 111, 2),
                (3, '1 пастилка', '2025-01-20 09:00:00', '2025-01-29 22:00:00', 1, 111, 4),
                (4, '1 таблетка', '2025-01-20 07:00:00', '2025-02-05 07:00:00', 1, 111, 7),
                (5, '1 пакетик', '2025-01-19 09:00:00', '2025-01-26 21:00:00', 2, 111, 3),
                (6, '2 капли', '2025-01-19 08:00:00', '2025-01-29 22:00:00', 2, 111, 5),
                (7, '1 таблетка', '2025-01-19 10:00:00', '2025-01-28 20:00:00', 2, 111, 6),
                (8, '1 таблетка', '2025-01-19 07:00:00', '2025-02-02 07:00:00', 2, 111, 7)
            ]

            for prescription in prescriptions:
                cursor.execute('SELECT * FROM Medical_prescription WHERE medical_prescription_ID = ?',
                               (prescription[0],))
                if not cursor.fetchone():
                    cursor.execute(
                        'INSERT INTO Medical_prescription (medical_prescription_ID, dosage, start_time, end_time, user_ID, medworker_ID, medicine_ID) VALUES (?, ?, ?, ?, ?, ?, ?)',
                        prescription)

            # Записи о приеме
            receptions = [
                (1, True, 'Легкая тошнота после приема', '2025-01-20 08:15:00', 1),
                (2, False, 'Пропуск: забыл принять', '2025-01-20 12:30:00', 2),
                (3, True, 'Принято по расписанию', '2025-01-20 09:10:00', 3),
                (4, True, 'Нет побочных эффектов', '2025-01-20 07:05:00', 4),
                (5, True, 'Сонливость', '2025-01-19 09:20:00', 5),
                (6, False, 'Пропуск: не было дома', '2025-01-19 08:30:00', 6),
                (7, True, 'Легкое головокружение', '2025-01-19 10:15:00', 7),
                (8, True, 'Нет побочных эффектов', '2025-01-19 07:10:00', 8)
            ]

            for reception in receptions:
                cursor.execute('SELECT * FROM Reception WHERE reception_ID = ?', (reception[0],))
                if not cursor.fetchone():
                    cursor.execute(
                        'INSERT INTO Reception (reception_ID, is_good, side_effects, taken_time, medical_prescription_ID) VALUES (?, ?, ?, ?, ?)',
                        reception)

            conn.commit()
            conn.close()
            print("Тестовые данные созданы успешно!")

        except sqlite3.Error as e:
            print(f"Ошибка создания тестовых данных: {e}")

    def initialize_database(self):
        """Инициализирует всю базу данных"""
        self.create_tables()
        self.create_test_data()