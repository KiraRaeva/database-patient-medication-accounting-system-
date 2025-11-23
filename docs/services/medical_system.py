import sys
import os
from datetime import datetime

# Добавляем корневую директорию проекта в Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from docs.database import DatabaseManager
from docs.models.user import UserModel
from docs.models.medicine import MedicineModel
from docs.models.medworker import MedworkerModel
from docs.models.prescription import MedicalPrescriptionModel
from docs.models.reception import ReceptionModel
from docs.models.purpose import PurposeOfDrugModel


class MedicalSystem:
    """Основной класс системы учёта приёма лекарств"""

    def __init__(self):
        self.db_manager = DatabaseManager()
        self.users = UserModel(self.db_manager)
        self.medicines = MedicineModel(self.db_manager)
        self.medworkers = MedworkerModel(self.db_manager)
        self.prescriptions = MedicalPrescriptionModel(self.db_manager)
        self.receptions = ReceptionModel(self.db_manager)
        self.purposes = PurposeOfDrugModel(self.db_manager)

        # Текущий авторизованный пользователь
        self.current_user = None
        self.current_medworker = None

    def add_test_data(self):
        """Добавление тестовых данных"""
        try:
            print("Добавление тестовых данных...")

            # Добавляем пациентов с логинами и паролями
            patient1 = self.users.create_user("Иван", "Петров", "1985-03-15",
                                              "ivan", "pass123",
                                              "Аллергия на пенициллин", "Диабет")
            print(f"Добавлен пациент 1: ID {patient1}")

            patient2 = self.users.create_user("Мария", "Сидорова", "1978-07-22",
                                              "maria", "pass123",
                                              "Нет", "Гипертония")
            print(f"Добавлен пациент 2: ID {patient2}")

            # Добавляем медицинских работников с логинами и паролями
            doctor1 = self.medworkers.create_medworker("Дмитрий", "Иванов", "dmitry", "doc123")
            print(f"Добавлен врач 1: ID {doctor1}")

            doctor2 = self.medworkers.create_medworker("Ольга", "Смирнова", "olga", "doc123")
            print(f"Добавлен врач 2: ID {doctor2}")

            # Добавляем лекарства
            medicine1 = self.medicines.create_medicine("Аспирин", "500 мг")
            print(f"Добавлено лекарство 1: ID {medicine1}")

            medicine2 = self.medicines.create_medicine("Амоксициллин", "250 мг")
            print(f"Добавлено лекарство 2: ID {medicine2}")

            medicine3 = self.medicines.create_medicine("Лозартан", "50 мг")
            print(f"Добавлено лекарство 3: ID {medicine3}")

            # Добавляем назначения
            prescription1 = self.prescriptions.create_prescription(
                "1 таблетка 3 раза в день", "2024-01-15", "2024-12-31", patient1, doctor1, medicine1
            )
            print(f"Добавлено назначение 1: ID {prescription1}")

            prescription2 = self.prescriptions.create_prescription(
                "1 таблетка утром", "2024-01-10", "2024-12-31", patient2, doctor2, medicine3
            )
            print(f"Добавлено назначение 2: ID {prescription2}")

            # Добавляем записи о приёмах
            reception1 = self.receptions.create_reception(True, prescription1, "pending", "Нет побочных эффектов")
            print(f"Добавлен приём 1: ID {reception1}")

            reception2 = self.receptions.create_reception(True, prescription1, "pending", "Легкое головокружение")
            print(f"Добавлен приём 2: ID {reception2}")

            reception3 = self.receptions.create_reception(True, prescription2, "pending", "Нет побочных эффектов")
            print(f"Добавлен приём 3: ID {reception3}")

            print("Тестовые данные успешно добавлены!")

        except Exception as e:
            print(f"Ошибка при добавлении тестовых данных: {e}")
            import traceback
            traceback.print_exc()

    def patient_login(self):
        """Авторизация пациента"""
        print("\n=== Авторизация пациента ===")
        login = input("Логин: ")
        password = input("Пароль: ")

        user = self.users.authenticate(login, password)
        if user:
            self.current_user = user
            print(f"Добро пожаловать, {user[1]} {user[2]}!")
            return True
        else:
            print("Неверный логин или пароль!")
            return False

    def medworker_login(self):
        """Авторизация медработника"""
        print("\n=== Авторизация медработника ===")
        login = input("Логин: ")
        password = input("Пароль: ")

        medworker = self.medworkers.authenticate(login, password)
        if medworker:
            self.current_medworker = medworker
            print(f"Добро пожаловать, {medworker[1]} {medworker[2]}!")
            return True
        else:
            print("Неверный логин или пароль!")
            return False

    def patient_menu(self):
        """Меню пациента"""
        while True:
            print(f"\n=== Панель пациента: {self.current_user[1]} {self.current_user[2]} ===")
            print("1. Просмотреть текущие назначения")
            print("2. Заполнить индивидуальные данные")
            print("3. Отметить приём лекарства")
            print("4. Выйти")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.display_user_prescriptions(self.current_user[0])
            elif choice == "2":
                self.update_individual_data()
            elif choice == "3":
                self.mark_medication_taken()
            elif choice == "4":
                self.current_user = None
                print("Выход из системы пациента...")
                break
            else:
                print("Неверный выбор!")

    def medworker_menu(self):
        """Меню медработника"""
        while True:
            print(f"\n=== Панель медработника: {self.current_medworker[1]} {self.current_medworker[2]} ===")
            print("1. Просмотреть текущие назначения")
            print("2. Показать приёмы пациентов")
            print("3. Показать всех пациентов")
            print("4. Добавить пациента")
            print("5. Добавить назначение")
            print("6. Выйти")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.display_all_prescriptions()
            elif choice == "2":
                self.display_all_receptions()
            elif choice == "3":
                self.display_all_patients()
            elif choice == "4":
                self.add_patient()
            elif choice == "5":
                self.add_prescription()
            elif choice == "6":
                self.current_medworker = None
                print("Выход из системы медработника...")
                break
            else:
                print("Неверный выбор!")

    def update_individual_data(self):
        """Обновление индивидуальных данных пациента"""
        print("\n=== Обновление индивидуальных данных ===")
        characteristics = input("Введите индивидуальные характеристики: ")

        self.users.update_individual_data(self.current_user[0], characteristics)
        print("Данные успешно обновлены!")

    def mark_medication_taken(self):
        """Отметка о приёме лекарства"""
        print("\n=== Отметка о приёме лекарства ===")

        # Показать активные назначения
        prescriptions = self.prescriptions.get_prescriptions_by_user(self.current_user[0])
        if not prescriptions:
            print("У вас нет активных назначений")
            return

        print("\nВаши активные назначения:")
        for i, pres in enumerate(prescriptions, 1):
            print(f"{i}. Лекарство: {pres[7]}, Дозировка: {pres[1]}")

        try:
            choice = int(input("Выберите номер назначения: ")) - 1
            if 0 <= choice < len(prescriptions):
                prescription_id = prescriptions[choice][0]

                # Показать приёмы для этого назначения
                receptions = self.receptions.get_receptions_by_prescription(prescription_id)
                if not receptions:
                    print("Для этого назначения нет записей о приёмах")
                    return

                print("\nЗаписи о приёмах:")
                for i, rec in enumerate(receptions, 1):
                    status = "Принято" if rec[5] == "taken" else "Пропущено" if rec[5] == "skipped" else "Ожидает"
                    print(f"{i}. ID: {rec[0]}, Статус: {status}, Время: {rec[6]}")

                rec_choice = int(input("Выберите номер приёма для отметки: ")) - 1
                if 0 <= rec_choice < len(receptions):
                    reception_id = receptions[rec_choice][0]

                    print("\nВыберите действие:")
                    print("1. Отметить как принято")
                    print("2. Отметить как пропущено")

                    action = input("Ваш выбор: ")

                    side_effects = ""
                    if action == "1":
                        status = "taken"
                        side_effects = input("Опишите побочные эффекты (если есть): ")
                    elif action == "2":
                        status = "skipped"
                        side_effects = input("Причина пропуска: ")
                    else:
                        print("Неверный выбор!")
                        return

                    self.receptions.update_reception_status(reception_id, status, side_effects)
                    print("Статус приёма обновлен!")
                else:
                    print("Неверный выбор!")
            else:
                print("Неверный выбор!")
        except ValueError:
            print("Ошибка: введите число!")

    def display_user_prescriptions(self, user_id: int):
        """Отображение назначений пользователя"""
        prescriptions = self.prescriptions.get_prescriptions_by_user(user_id)

        if not prescriptions:
            print(f"У пользователя {user_id} нет назначений")
            return

        print(f"\nНазначения для пользователя {user_id}:")
        for pres in prescriptions:
            status = "Активно" if datetime.now().date() <= datetime.strptime(pres[3],
                                                                             "%Y-%m-%d").date() else "Завершено"
            print(
                f" Лекарство: {pres[7]}, Дозировка: {pres[1]}, Период: {pres[2]} - {pres[3]}, Врач: {pres[8]}, Статус: {status}")

    def display_all_prescriptions(self):
        """Отображение всех назначений"""
        users = self.users.get_all_users()
        for user in users:
            self.display_user_prescriptions(user[0])

    def display_all_receptions(self):
        """Отображение всех приёмов"""
        users = self.users.get_all_users()
        for user in users:
            receptions = self.receptions.get_receptions_by_user(user[0])
            if receptions:
                print(f"\nПриёмы пользователя {user[1]} {user[2]}:")
                for rec in receptions:
                    status = "Принято" if rec[5] == "taken" else "Пропущено" if rec[5] == "skipped" else "Ожидает"
                    print(f" Лекарство: {rec[8]}, Статус: {status}, Побочные эффекты: {rec[2]}, Время: {rec[6]}")

    def display_all_patients(self):
        """Отображение всех пациентов"""
        users = self.users.get_all_users()
        print("\nСписок пациентов:")
        for user in users:
            print(f"ID: {user[0]}, Имя: {user[1]} {user[2]}, Дата рождения: {user[3]}")

    def add_patient(self):
        """Добавление нового пациента"""
        print("\n=== Добавление нового пациента ===")
        first_name = input("Имя: ")
        second_name = input("Фамилия: ")
        date_of_birth = input("Дата рождения (ГГГГ-ММ-ДД): ")
        login = input("Логин: ")
        password = input("Пароль: ")
        contraindications = input("Противопоказания: ")
        individual_characteristics = input("Индивидуальные характеристики: ")

        try:
            user_id = self.users.create_user(first_name, second_name, date_of_birth, login, password,
                                             contraindications, individual_characteristics)
            print(f"Пациент успешно добавлен с ID: {user_id}")
        except Exception as e:
            print(f"Ошибка при добавлении пациента: {e}")

    def add_prescription(self):
        """Добавление нового назначения"""
        print("\n=== Добавление нового назначения ===")

        # Показать пациентов
        users = self.users.get_all_users()
        if not users:
            print("Нет доступных пациентов")
            return

        print("\nСписок пациентов:")
        for user in users:
            print(f"ID: {user[0]}, Имя: {user[1]} {user[2]}")

        # Показать лекарства
        medicines = self.medicines.get_all_medicines()
        if not medicines:
            print("Нет доступных лекарств")
            return

        print("\nСписок лекарств:")
        for med in medicines:
            print(f"ID: {med[0]}, Название: {med[1]}, Дозировка: {med[2]}")

        try:
            user_id = int(input("ID пациента: "))
            medicine_id = int(input("ID лекарства: "))
            dosage = input("Дозировка и инструкция: ")
            start_time = input("Дата начала (ГГГГ-ММ-ДД): ")
            end_time = input("Дата окончания (ГГГГ-ММ-ДД): ")

            prescription_id = self.prescriptions.create_prescription(
                dosage, start_time, end_time, user_id, self.current_medworker[0], medicine_id
            )
            print(f"Назначение успешно добавлено с ID: {prescription_id}")
        except ValueError:
            print("Ошибка: введите числовые ID!")
        except Exception as e:
            print(f"Ошибка при добавлении назначения: {e}")