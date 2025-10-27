import sqlite3

db_path = "C:\\Users\\Пользователь\\PycharmProjects\\Project1\\docs\\diagrams\\patient medication accounting system.db"


def add_test_data():
    """Простая функция для добавления тестовых данных"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("🗑️ Очищаем старые данные...")
    # Очищаем таблицы (обратный порядок из-за внешних ключей)
    tables = ['Факт_приема_лекарства', 'Врачебное_назначение', 'Лекарственный_препарат', 'Медработник', 'Пациент']
    for table in tables:
        cursor.execute(f"DELETE FROM {table}")

    print("📝 Добавляем тестовые данные...")

    # 1. Пациенты
    patients = [
        ('Иванов Алексей Петрович', '1985-03-15', 'Аллергия на пенициллин'),
        ('Сидорова Мария Владимировна', '1990-07-22', 'Беременность'),
        ('Петров Дмитрий Сергеевич', '1978-11-30', 'Сахарный диабет')
    ]

    for patient in patients:
        cursor.execute('''
                       INSERT INTO Пациент (ФИО, Дата_рождения, Противопоказания)
                       VALUES (?, ?, ?)
                       ''', patient)
        print(f"   ✅ Добавлен пациент: {patient[0]}")

    # 2. Медработники
    medical_workers = [
        'Смирнова Ольга Владимировна',
        'Козлов Андрей Николаевич',
        'Васильева Елена Дмитриевна'
    ]

    for worker in medical_workers:
        cursor.execute('INSERT INTO Медработник (ФИО) VALUES (?)', (worker,))
        print(f"   ✅ Добавлен медработник: {worker}")

    # 3. Лекарства
    medications = [
        ('500 мг', 'таблетки', 'Парацетамол'),
        ('250 мг', 'капсулы', 'Амоксициллин'),
        ('100 мг/5 мл', 'сироп', 'Нурофен')
    ]

    for med in medications:
        cursor.execute('''
                       INSERT INTO Лекарственный_препарат (Дозировка, Лекарственная_форма, Название_препарата)
                       VALUES (?, ?, ?)
                       ''', med)
        print(f"   ✅ Добавлено лекарство: {med[2]}")

    # 4. Назначения
    prescriptions = [
        (1, 1, 1),  # Пациент 1, Врач 1, Лекарство 1
        (2, 2, 2),  # Пациент 2, Врач 2, Лекарство 2
        (3, 3, 3)  # Пациент 3, Врач 3, Лекарство 3
    ]

    for i, presc in enumerate(prescriptions, 1):
        cursor.execute('''
                       INSERT INTO Врачебное_назначение (ID_Пациента, ID_Медработника, ID_Лекарство)
                       VALUES (?, ?, ?)
                       ''', presc)
        print(f"   ✅ Добавлено назначение #{i}")

    # 5. Факты приема
    intakes = [
        ('принято', 'нет', 1),
        ('пропущено', 'нет', 1),
        ('принято', 'легкая тошнота', 2),
        ('принято', 'нет', 3)
    ]

    for intake in intakes:
        cursor.execute('''
                       INSERT INTO Факт_приема_лекарства (Статус, Побочные_эффекты, Врачебное_назначение_ID)
                       VALUES (?, ?, ?)
                       ''', intake)
        print(f"   ✅ Добавлен факт приема: {intake[0]}")

    conn.commit()
    conn.close()
    print("🎉 Все тестовые данные успешно добавлены!")


def show_all_data():
    """Показывает все данные из всех таблиц"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\n📊 ВСЕ ДАННЫЕ В БАЗЕ:")
    print("=" * 50)

    tables = ['Пациент', 'Медработник', 'Лекарственный_препарат', 'Врачебное_назначение', 'Факт_приема_лекарства']

    for table in tables:
        print(f"\n🎯 ТАБЛИЦА: {table}")
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                print(f"   📍 {row}")
        else:
            print("   (пусто)")

    conn.close()


# ЗАПУСКАЕМ
if __name__ == "__main__":
    add_test_data()
    show_all_data()