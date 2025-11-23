from typing import List, Optional, Tuple

from database import DatabaseManager





class MedicalPrescriptionModel:

  """Модель для работы с таблицей медицинских назначений"""



  def __init__(self, db_manager: DatabaseManager):

    self.db = db_manager



  def create_prescription(self, dosage: str, start_time: str, end_time: str,

              user_id: int, medworker_id: int, medicine_id: int) -> int:

    """Создание нового медицинского назначения"""

    with self.db.get_connection() as conn:

      cursor = conn.cursor()

      cursor.execute('''

        INSERT INTO Medical_prescription (dosage, start_time, end_time, user_ID, medworker_ID, medicine_ID)

        VALUES (?, ?, ?, ?, ?, ?)

      ''', (dosage, start_time, end_time, user_id, medworker_id, medicine_id))

      conn.commit()

      return cursor.lastrowid



  def get_prescription(self, prescription_id: int) -> Optional[Tuple]:

    """Получение назначения по ID"""

    with self.db.get_connection() as conn:

      cursor = conn.cursor()

      cursor.execute('SELECT * FROM Medical_prescription WHERE medical_prescription_ID = ?', (prescription_id,))

      return cursor.fetchone()



  def get_prescriptions_by_user(self, user_id: int) -> List[Tuple]:

    """Получение всех назначений для пользователя"""

    with self.db.get_connection() as conn:

      cursor = conn.cursor()

      cursor.execute('''

        SELECT mp.*, m.nametag, mw.first_name || ' ' || mw.second_name as doctor_name

        FROM Medical_prescription mp

        JOIN Medicine m ON mp.medicine_ID = m.medicine_ID

        JOIN Medworker mw ON mp.medworker_ID = mw.medworker_ID

        WHERE mp.user_ID = ?

      ''', (user_id,))

      return cursor.fetchall()

