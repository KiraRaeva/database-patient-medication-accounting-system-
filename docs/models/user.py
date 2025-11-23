from typing import List, Optional, Tuple

from database import DatabaseManager





class UserModel:

  """Модель для работы с таблицей пользователей"""



  def __init__(self, db_manager: DatabaseManager):

    self.db = db_manager



  def create_user(self, first_name: str, second_name: str, date_of_birth: str,

          contraindications: str = "", individual_characteristics: str = "") -> int:

    """Создание нового пользователя"""

    with self.db.get_connection() as conn:

      cursor = conn.cursor()

      cursor.execute('''

        INSERT INTO User (first_name, second_name, date_of_birth, contraindications, individual_characteristics)

        VALUES (?, ?, ?, ?, ?)

      ''', (first_name, second_name, date_of_birth, contraindications, individual_characteristics))

      conn.commit()

      return cursor.lastrowid



  def get_user(self, user_id: int) -> Optional[Tuple]:

    """Получение пользователя по ID"""

    with self.db.get_connection() as conn:

      cursor = conn.cursor()

      cursor.execute('SELECT * FROM User WHERE user_ID = ?', (user_id,))

      return cursor.fetchone()



  def get_all_users(self) -> List[Tuple]:

    """Получение всех пользователей"""

    with self.db.get_connection() as conn:

      cursor = conn.cursor()

      cursor.execute('SELECT * FROM User')

      return cursor.fetchall()



  def update_user(self, user_id: int, **kwargs):

    """Обновление данных пользователя"""

    if not kwargs:

      return



    set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])

    values = list(kwargs.values())

    values.append(user_id)



    with self.db.get_connection() as conn:

      cursor = conn.cursor()

      cursor.execute(f'UPDATE User SET {set_clause} WHERE user_ID = ?', values)

      conn.commit()