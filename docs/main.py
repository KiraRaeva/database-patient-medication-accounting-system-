from services.medical_system import MedicalSystem





def main():

  """Основная функция для демонстрации работы системы"""

  system = MedicalSystem()



  while True:

    print("\n=== Система учёта приёма лекарств ===")

    print("1. Показать всех пациентов")

    print("2. Показать все назначения пациента")

    print("3. Показать приёмы по назначению")

    print("4. Добавить тестовые данные")

    print("5. Выход")



    choice = input("Выберите действие: ")



    if choice == "1":

      users = system.users.get_all_users()

      print("\nСписок пациентов:")

      for user in users:

        print(f"ID: {user[0]}, Имя: {user[1]} {user[2]}, Дата рождения: {user[3]}")



    elif choice == "2":

      user_id = int(input("Введите ID пациента: "))

      system.display_user_prescriptions(user_id)



    elif choice == "3":

      prescription_id = int(input("Введите ID назначения: "))

      system.display_prescription_receptions(prescription_id)



    elif choice == "4":

      system.add_test_data()



    elif choice == "5":

      print("Выход из системы...")

      break



    else:

      print("Неверный выбор!")





if __name__ == "__main__":

  main()