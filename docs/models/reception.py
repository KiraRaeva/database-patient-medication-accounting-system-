from typing import List, Optional, Tuple

from database import DatabaseManager





class ReceptionModel:

  """Модель для работы с таблицей приёмов лекарств"""



  def __init__(self, db_manager: DatabaseManager):

    self.db = db_manager



  def create_reception(self, is_good: bool, medical_prescription_id: int,

             side_effects: str = "") -> int:

    """Создание записи о приёме лекарства"""

    with self.db.get_connection() as conn:

      cursor = conn.cursor()

      cursor.execute('''

        INSERT INTO Reception (is_good, side_effects, medical_prescription_ID)

        VALUES (?, ?, ?)

      ''', (is_good, side_effects, medical_prescription_id))

      conn.commit()

      return cursor.lastrowid



  def get_reception(self, reception_id: int) -> Optional[Tuple]:

    """Получение записи о приёме по ID"""

    with self.db.get_connection() as conn:

      cursor = conn.cursor()

      cursor.execute('SELECT * FROM Reception WHERE reception_ID = ?', (reception_id,))

      return cursor.fetchone()



  def get_receptions_by_prescription(self, prescription_id: int) -> List[Tuple]:

    """Получение всех записей о приёмах для назначения"""

    with self.db.get_connection() as conn:

      cursor = conn.cursor()

      cursor.execute('SELECT * FROM Reception WHERE medical_prescription_ID = ?', (prescription_id,))

      return cursor.fetchall()