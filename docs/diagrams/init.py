import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_name='patient medication accounting system.db'):
        self.conn = sqlite3.connect(db_name)

        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Таблица Пациент
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Пациент (
            Пациент_ID INTEGER PRIMARY KEY AUTOINCREMENT, ФИО TEXT NOT NULL, Дата_рождения DATE NOT NULL,
            Противопоказания TEXT
)
''')

        # Таблица Медработник
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Медработник (
            Медработник_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ФИО TEXT NOT NULL 
)
''')
    # Таблица Лекарственный_препарат
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Лекарственный_препарат (
            Лекарство_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Дозировка TEXT NOT NULL,
            Лекарственная_форма TEXT NOT NULL,
            Название_препарата TEXT NOT NULL
)
''')

    # Таблица Врачебное_назначение
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Врачебное_назначение (
            Назначение_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Начало приема Datetame NOT NULL,
            Конец приема Datetame NOT NULL,
            ID_Пациента INTEGER NOT NULL,
            ID_Медработника INTEGER NOT NULL,
            ID_Лекарство INTEGER NOT NULL,
            FOREIGN KEY (ID_Пациента) REFERENCES Пациент(Пациент_ID),
            FOREIGN KEY(ID_Медработника) REFERENCES Медработник(Медработник_ID),
            FOREIGN KEY(ID_Лекарство) REFERENCES Лекарственный_препарат(Лекарство_ID)
)
''')

        # Таблица Факт_приема_лекарства
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Факт_приема_лекарства (
            Прием_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Статус TEXT NOT NULL CHECK (Статус IN('принято','пропущено')),
            Побочные_эффекты TEXT,
            Врачебное_назначение_ID INTEGER NOT NULL,
            FOREIGN KEY(Врачебное_назначение_ID) REFERENCES Врачебное_назначение(Назначение_ID)
)
''')

        self.conn.commit()

    def close(self):

        self.conn.close()



db = Database()
db.close()


def add_test_data(self):
    """Добавление тестовых данных во все таблицы"""

    patients = [
        ('Мартов Дмитрий Сергеевич', '1996-03-15', 'Аллергия на пенициллин'),
        ('Шарикова Дарья Владимировна', '2000-11-06', 'Беременность'),
        ('Лебедев Леонид Александрович', '1300-11-25', 'Сонная болезнь')
    ]

    self.cursor.executemany('''
    INSERT INTO Пациент (ФИО, Дата_рождения, Противопоказания_и_индивидуальные_особенности)
    VALUES (?, ?, ?)
''', patients)

    medical_workers = [
        ('Смирнова Полина Сергеевна',),
        ('Веселый Павел Николаевич',),
        ('Грустная Елена Дмитриевна',)
    ]

    self.cursor.executemany('''
    INSERT INTO Медработник (ФИО)
    VALUES (?)
''', medical_workers)

    medications = [
        ('500 мг', 'таблетки', 'Парацетамол'),
        ('250 мг', 'капсулы', 'Амоксициллин'),
        ('100 мг', 'сироп', 'Нурофен')
    ]

    self.cursor.executemany('''
    INSERT INTO Лекарственный_препарат (Дозировка, Лекарственная_форма, Название_препарата)
    VALUES (?, ?, ?)
''', medications)


    prescriptions = [
        (1, 1),  # Пациент 1, Медработник 1
        (2, 2),  # Пациент 2, Медработник 2
        (3, 3)  # Пациент 3, Медработник 3
    ]

    self.cursor.executemany('''
    INSERT INTO Врачебное_назначение (ID_Пациента, ID_Медработника)
    VALUES (?, ?)
''', prescriptions)


    medication_intakes = [
        ('принято', 'нет', 1),
        ('пропущено', 'нет', 1),
        ('принято', 'легкая тошнота', 2),
        ('принято', 'нет', 3)
    ]

    self.cursor.executemany('''
    INSERT INTO Факт_приема_лекарства (Статус, Побочные_эффекты, Врачебное_назначение_ID)
    VALUES (?, ?, ?)
''', medication_intakes)

    self.conn.commit()


# класс модели?
class Пациент:
    def __init__(self, пациент_id, фио, дата_рождения, противопоказания):
        self.пациент_id = пациент_id
        self.фио = фио
        self.дата_рождения = дата_рождения
        self.противопоказания = противопоказания

    def __str__(self):
        return f"Пациент {self.фио}"


class Медработник:
    def __init__(self, медработник_id, фио):
        self.медработник_id = медработник_id
        self.фио = фио

    def __str__(self):
        return f"Медработник {self.фио}"


class ЛекарственныйПрепарат:
    def __init__(self, лекарство_id, дозировка, лекарственная_форма, название_препарата):
        self.лекарство_id = лекарство_id
        self.дозировка = дозировка
        self.лекарственная_форма = лекарственная_форма
        self.название_препарата = название_препарата

    def __str__(self):
        return f"{self.название_препарата} ({self.дозировка})"


class ВрачебноеНазначение:
    def __init__(self, назначение_id, id_пациента, id_медработника, id_лекарство):
        self.назначение_id = назначение_id
        self.id_пациента = id_пациента
        self.id_медработника = id_медработника
        self.id_лекарство = id_лекарство

    def __str__(self):
        return f"Назначение #{self.назначение_id}"


class ФактПриемаЛекарства:
    def __init__(self, прием_id, статус, побочные_эффекты, врачебное_назначение_id):
        self.прием_id = прием_id
        self.статус = статус
        self.побочные_эффекты = побочные_эффекты
        self.врачебное_назначение_id = врачебное_назначение_id

    def __str__(self):
        return f"Прием #{self.прием_id} ({self.статус})"

