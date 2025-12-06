from services.auth_service import AuthService
from services.medworker_service import MedworkerService
from services.patient_service import PatientService
from database.db_init import DatabaseInitializer


class HospitalSystem:
    def __init__(self):
        self.db_path = "database/hospital.db"
        self.current_medworker_id = None
        self.current_user_id = None
        self.auth_service = AuthService(self.db_path)
        self.db_initializer = DatabaseInitializer(self.db_path)

        # Инициализация базы данных
        self.db_initializer.initialize_database()

    def medworker_login(self):
        """Авторизация медработника"""
        self.current_medworker_id = self.auth_service.medworker_login()
        if self.current_medworker_id:
            self.medworker_menu()

    def user_login(self):
        """Авторизация пациента"""
        self.current_user_id = self.auth_service.user_login()
        if self.current_user_id:
            self.user_menu()

    def medworker_menu(self):
        """Меню медработника"""
        medworker_service = MedworkerService(self.db_path, self.current_medworker_id)

        while True:
            print("\n" + "=" * 50)
            print("МЕНЮ МЕДРАБОТНИКА")
            print("=" * 50)
            print("1. Список всех пациентов")
            print("2. Просмотр назначений пациентов")
            print("3. Изменить назначение")
            print("4. Добавить историю болезни пациента")
            print("5. Добавить индивидуальные особенности пациента")
            print("6. Создать новое назначение")
            print("7. Просмотр статуса приема препаратов")
            print("8. Просмотр медицинской карты пациента")
            print("9. Выйти из системы")

            choice = input("Выберите действие: ")

            if choice == '1':
                medworker_service.show_all_patients()
            elif choice == '2':
                medworker_service.show_patient_prescriptions()
            elif choice == '3':
                medworker_service.modify_prescription()
            elif choice == '4':
                medworker_service.add_medical_history()
            elif choice == '5':
                medworker_service.add_individual_characteristics()
            elif choice == '6':
                medworker_service.create_new_prescription()
            elif choice == '7':
                medworker_service.show_medication_status()
            elif choice == '8':
                medworker_service.show_patient_medical_card()
            elif choice == '9':
                self.current_medworker_id = None
                break
            else:
                print("Неверный выбор!")

    def user_menu(self):
        """Меню пациента"""
        patient_service = PatientService(self.db_path, self.current_user_id)

        while True:
            print("\n" + "=" * 50)
            print("МЕНЮ ПАЦИЕНТА")
            print("=" * 50)
            print("1. Отметить самочувствие после препарата")
            print("2. Подтвердить прием препаратов")
            print("3. Посмотреть назначенные препараты")
            print("4. Выйти из системы")

            choice = input("Выберите действие: ")

            if choice == '1':
                patient_service.mark_wellbeing()
            elif choice == '2':
                patient_service.confirm_medication()
            elif choice == '3':
                patient_service.view_prescriptions()
            elif choice == '4':
                self.current_user_id = None
                break
            else:
                print("Неверный выбор!")

    def main_menu(self):
        """Главное меню системы"""
        while True:
            print("\n" + "=" * 40)
            print("СИСТЕМА УЧЁТА ПРИЁМА ЛЕКАРСТВ")
            print("=" * 40)
            print("1. Вход медработника")
            print("2. Вход пациента")
            print("3. Выход")

            choice = input("Выберите действие: ")

            if choice == '1':
                self.medworker_login()
            elif choice == '2':
                self.user_login()
            elif choice == '3':
                print("Выход из системы")
                break
            else:
                print("Неверный выбор!")


if __name__ == "__main__":
    system = HospitalSystem()
    system.main_menu()