from typing import List, Optional, Tuple

from docs.database import DatabaseManager





class MedicineModel:

  """Модель для работы с таблицей лекарств"""



  def __init__(self, db_manager: DatabaseManager):

    self.db = db_manager



  def create_medicine(self, nametag: str, dosage: str) -> int:

    """Создание нового лекарства"""

    with self.db.get_connection() as conn:

      cursor = conn.cursor()

      cursor.execute('''

        INSERT INTO Medicine (nametag, dosage)

        VALUES (?, ?)

      ''', (nametag, dosage))

      conn.commit()

      return cursor.lastrowid



  def get_medicine(self, medicine_id: int) -> Optional[Tuple]:

    """Получение лекарства по ID"""

    with self.db.get_connection() as conn:

      cursor = conn.cursor()

      cursor.execute('SELECT * FROM Medicine WHERE medicine_ID = ?', (medicine_id,))

      return cursor.fetchone()



  def get_all_medicines(self) -> List[Tuple]:

    """Получение всех лекарств"""

    with self.db.get_connection() as conn:

      cursor = conn.cursor()

      cursor.execute('SELECT * FROM Medicine')

      return cursor.fetchall()