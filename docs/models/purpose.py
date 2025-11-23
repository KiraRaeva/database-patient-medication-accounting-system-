from database import DatabaseManager





class PurposeOfDrugModel:

  """Модель для работы с таблицей назначений лекарств"""



  def __init__(self, db_manager: DatabaseManager):

    self.db = db_manager



  def create_purpose(self, purpose_id: int, medicine_id: int) -> int:

    """Создание связи назначения и лекарства"""

    with self.db.get_connection() as conn:

      cursor = conn.cursor()

      cursor.execute('''

        INSERT INTO Purpose_of_the_drug (purpose_ID, medicine_ID)

        VALUES (?, ?)

      ''', (purpose_id, medicine_id))

      conn.commit()

      return cursor.lastrowid

