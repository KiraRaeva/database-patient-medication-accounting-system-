from datetime import datetime

from database import DatabaseManager

from models import UserModel, MedicineModel, MedworkerModel, MedicalPrescriptionModel, ReceptionModel,PurposeOfDrugModel





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



  def add_test_data(self):

    """Добавление тестовых данных"""

    # Добавляем пациентов

    patient1 = self.users.create_user("Иван", "Петров", "1985-03-15", "Аллергия на пенициллин", "Диабет")

    patient2 = self.users.create_user("Мария", "Сидорова", "1978-07-22", "Нет", "Гипертония")



    # Добавляем медицинских работников

    doctor1 = self.medworkers.create_medworker("Дмитрий", "Иванов")

    doctor2 = self.medworkers.create_medworker("Ольга", "Смирнова")



    # Добавляем лекарства

    medicine1 = self.medicines.create_medicine("Аспирин", "500 мг")

    medicine2 = self.medicines.create_medicine("Амоксициллин", "250 мг")

    medicine3 = self.medicines.create_medicine("Лозартан", "50 мг")



    # Добавляем назначения

    prescription1 = self.prescriptions.create_prescription(

      "1 таблетка 3 раза в день", "2024-01-15", "2024-01-25", patient1, doctor1, medicine1

    )

    prescription2 = self.prescriptions.create_prescription(

      "1 таблетка утром", "2024-01-10", "2024-02-10", patient2, doctor2, medicine3

    )



    # Добавляем записи о приёмах

    self.receptions.create_reception(True, prescription1, "Нет побочных эффектов")

    self.receptions.create_reception(True, prescription1, "Легкое головокружение")

    self.receptions.create_reception(True, prescription2, "Нет побочных эффектов")



    print("Тестовые данные добавлены!")



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



  def display_prescription_receptions(self, prescription_id: int):

    """Отображение приёмов для назначения"""

    receptions = self.receptions.get_receptions_by_prescription(prescription_id)



    if not receptions:

      print(f"Для назначения {prescription_id} нет записей о приёмах")

      return



    print(f"\nПриёмы для назначения {prescription_id}:")

    for rec in receptions:

      status = "Успешно" if rec[1] else "Проблемы"

      print(f" Статус: {status}, Побочные эффекты: {rec[2]}, Время: {rec[4]}")