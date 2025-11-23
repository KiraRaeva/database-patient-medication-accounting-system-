import sqlite3





class DatabaseManager:

  """Класс для управления базой данных"""



  def __init__(self, db_name: str = "medical_system.db"):

    self.db_name = db_name

    self.init_database()



  def get_connection(self):

    """Создание соединения с базой данных"""

    return sqlite3.connect(self.db_name)



  def init_database(self):

    """Инициализация базы данных и создание таблиц"""

    with self.get_connection() as conn:

      cursor = conn.cursor()



      # Создание таблицы Пользователи (Пациенты)

      cursor.execute('''

        CREATE TABLE IF NOT EXISTS User (

          user_ID INTEGER PRIMARY KEY AUTOINCREMENT,

          first_name TEXT NOT NULL,

          second_name TEXT NOT NULL,

          date_of_birth TEXT NOT NULL,

          contraindications TEXT,

          individual_characteristics TEXT

        )

      ''')



      # Создание таблицы Медицинских работников

      cursor.execute('''

        CREATE TABLE IF NOT EXISTS Medworker (

          medworker_ID INTEGER PRIMARY KEY AUTOINCREMENT,

          first_name TEXT NOT NULL,

          second_name TEXT NOT NULL

        )

      ''')



      # Создание таблицы Лекарств

      cursor.execute('''

        CREATE TABLE IF NOT EXISTS Medicine (

          medicine_ID INTEGER PRIMARY KEY AUTOINCREMENT,

          nametag TEXT NOT NULL,

          dosage TEXT NOT NULL

        )

      ''')



      # Создание таблицы Медицинских назначений

      cursor.execute('''

        CREATE TABLE IF NOT EXISTS Medical_prescription (

          medical_prescription_ID INTEGER PRIMARY KEY AUTOINCREMENT,

          dosage TEXT NOT NULL,

          start_time TEXT NOT NULL,

          end_time TEXT NOT NULL,

          user_ID INTEGER NOT NULL,

          medworker_ID INTEGER NOT NULL,

          medicine_ID INTEGER NOT NULL,

          FOREIGN KEY (user_ID) REFERENCES User (user_ID),

          FOREIGN KEY (medworker_ID) REFERENCES Medworker (medworker_ID),

          FOREIGN KEY (medicine_ID) REFERENCES Medicine (medicine_ID)

        )

      ''')



      # Создание таблицы Приёмов лекарств

      cursor.execute('''

        CREATE TABLE IF NOT EXISTS Reception (

          reception_ID INTEGER PRIMARY KEY AUTOINCREMENT,

          is_good BOOLEAN NOT NULL,

          side_effects TEXT,

          medical_prescription_ID INTEGER NOT NULL,

          timestamp TEXT DEFAULT CURRENT_TIMESTAMP,

          FOREIGN KEY (medical_prescription_ID) REFERENCES Medical_prescription (medical_prescription_ID)

        )

      ''')



      # Создание таблицы Назначений лекарств (связующая)

      cursor.execute('''

        CREATE TABLE IF NOT EXISTS Purpose_of_the_drug (

          purpose_of_the_drug_ID INTEGER PRIMARY KEY AUTOINCREMENT,

          purpose_ID INTEGER NOT NULL,

          medicine_ID INTEGER NOT NULL,

          FOREIGN KEY (purpose_ID) REFERENCES Medical_prescription (medical_prescription_ID),

          FOREIGN KEY (medicine_ID) REFERENCES Medicine (medicine_ID)

        )

      ''')



      conn.commit()

