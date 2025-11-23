import sys
import os

# Добавляем корневую директорию проекта в Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from docs.services.medical_system import MedicalSystem

def main():
    """Основная функция системы"""
    system = MedicalSystem()

    while True:
        print("\n=== Система учёта приёма лекарств ===")
        print("1. Вход для пациента")
        print("2. Вход для медработника")
        print("3. Добавить тестовые данные")
        print("4. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            if system.patient_login():
                system.patient_menu()
        elif choice == "2":
            if system.medworker_login():
                system.medworker_menu()
        elif choice == "3":
            system.add_test_data()
        elif choice == "4":
            print("Выход из системы...")
            break
        else:
            print("Неверный выбор!")

if __name__ == "__main__":
    main()