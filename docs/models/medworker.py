from typing import List, Optional, Tuple

from database import DatabaseManager





class MedworkerModel:

  """Модель для работы с таблицей медицинских работников"""



  def __init__(self, db_manager: DatabaseManager):

    self.db = db_manager



  def create_medworker(self, first_name: str, second_name: str) -> int:

    """Создание нового медицинского работника"""

    with self.db.get_connection() as conn:

      cursor = conn.cursor()

      cursor.execute('''

        INSERT INTO Medworker (first_name, second_name)

        VALUES (?, ?)

      ''', (first_name, second_name))

      conn.commit()

      return cursor.lastrowid



  def get_medworker(self, medworker_id: int) -> Optional[Tuple]:

    """Получение медицинского работника по ID"""

    with self.db.get_connection() as conn:

      cursor = conn.cursor()

      cursor.execute('SELECT * FROM Medworker WHERE medworker_ID = ?', (medworker_id,))

      return cursor.fetchone()



  def get_all_medworkers(self) -> List[Tuple]:

    """Получение всех медицинских работников"""

    with self.db.get_connection() as conn:

      cursor = conn.cursor()

      cursor.execute('SELECT * FROM Medworker')

      return cursor.fetchall()

