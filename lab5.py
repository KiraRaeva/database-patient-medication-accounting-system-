import json
import csv
import xml.etree.ElementTree as ET
import yaml
import os
import sqlite3
from datetime import datetime


class DataFormatter:
    def __init__(self, db_path):
        self.db_path = db_path
        self.ensure_out_directory()

    def ensure_out_directory(self):

        if not os.path.exists('out'):
            os.makedirs('out')

    def get_connection(self):
        """Создает соединение с базой данных"""
        try:
            return sqlite3.connect(self.db_path)
        except Exception as e:
            print(f"Ошибка подключения к базе: {e}")
            return None

    def fetch_patient_data(self):
        """Извлекает данные пациентов с их назначениями"""
        conn = self.get_connection()
        if not conn:
            return []

        cursor = conn.cursor()


        query = """
        SELECT 
            u.user_ID,
            u.first_name,
            u.second_name,
            u.date_of_birth,
            u.contraindications,
            u.individual_characteristics,
            mp.medical_prescription_ID,
            mp.dosage,
            mp.start_time,
            mp.end_time,
            m.medicine_ID,
            m.nametag,
            m.dosage as medicine_dosage
        FROM User u
        LEFT JOIN Medical_prescription mp ON u.user_ID = mp.user_ID
        LEFT JOIN Medicine m ON mp.medicine_ID = m.medicine_ID
        ORDER BY u.user_ID
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        # Группируем данные по пациентам
        patients = {}
        for row in rows:
            user_id = row[0]
            if user_id not in patients:
                patients[user_id] = {
                    'user_ID': user_id,
                    'first_name': row[1],
                    'second_name': row[2],
                    'date_of_birth': row[3],
                    'contraindications': row[4],
                    'individual_characteristics': row[5],
                    'prescriptions': []
                }

            # Добавляем назначение, если оно есть
            if row[6]:  # medical_prescription_ID
                prescription = {
                    'medical_prescription_ID': row[6],
                    'dosage': row[7],
                    'start_time': row[8],
                    'end_time': row[9],
                    'medicine': {
                        'medicine_ID': row[10],
                        'nametag': row[11],
                        'dosage': row[12]
                    }
                }
                patients[user_id]['prescriptions'].append(prescription)

        return list(patients.values())

    def export_to_json(self, data):
        """Экспорт данных в JSON"""
        try:
            with open('out/data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("Данные успешно экспортированы в JSON")
        except Exception as e:
            print(f"Ошибка при экспорте в JSON: {e}")

    def export_to_csv(self, data):
        """Экспорт данных в CSV"""
        try:
            with open('out/data.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)

                # Заголовки
                writer.writerow([
                    'user_ID', 'first_name', 'second_name', 'date_of_birth',
                    'contraindications', 'individual_characteristics',
                    'prescriptions_info'
                ])

                # Данные
                for patient in data:
                    # Формируем информацию о назначениях в одной строке
                    prescriptions_info = ""
                    if patient['prescriptions']:
                        prescriptions_list = []
                        for pres in patient['prescriptions']:
                            pres_str = f"{pres['medicine']['nametag']}: {pres['dosage']} ({pres['start_time']} - {pres['end_time']})"
                            prescriptions_list.append(pres_str)
                        prescriptions_info = "; ".join(prescriptions_list)

                    writer.writerow([
                        patient['user_ID'],
                        patient['first_name'],
                        patient['second_name'],
                        patient['date_of_birth'],
                        patient['contraindications'],
                        patient['individual_characteristics'],
                        prescriptions_info
                    ])

            print(" Данные успешно экспортированы в CSV")
        except Exception as e:
            print(f"Ошибка при экспорте в CSV: {e}")

    def export_to_xml(self, data):
        """Экспорт данных в XML"""
        try:
            root = ET.Element('patients')

            for patient in data:
                patient_elem = ET.SubElement(root, 'patient')

                ET.SubElement(patient_elem, 'user_ID').text = str(patient['user_ID'])
                ET.SubElement(patient_elem, 'first_name').text = patient['first_name']
                ET.SubElement(patient_elem, 'second_name').text = patient['second_name']
                ET.SubElement(patient_elem, 'date_of_birth').text = patient['date_of_birth']
                ET.SubElement(patient_elem, 'contraindications').text = patient['contraindications']
                ET.SubElement(patient_elem, 'individual_characteristics').text = patient['individual_characteristics']

                prescriptions_elem = ET.SubElement(patient_elem, 'prescriptions')
                for prescription in patient['prescriptions']:
                    pres_elem = ET.SubElement(prescriptions_elem, 'prescription')
                    ET.SubElement(pres_elem, 'medical_prescription_ID').text = str(
                        prescription['medical_prescription_ID'])
                    ET.SubElement(pres_elem, 'dosage').text = prescription['dosage']
                    ET.SubElement(pres_elem, 'start_time').text = prescription['start_time']
                    ET.SubElement(pres_elem, 'end_time').text = prescription['end_time']

                    medicine_elem = ET.SubElement(pres_elem, 'medicine')
                    ET.SubElement(medicine_elem, 'medicine_ID').text = str(prescription['medicine']['medicine_ID'])
                    ET.SubElement(medicine_elem, 'nametag').text = prescription['medicine']['nametag']
                    ET.SubElement(medicine_elem, 'dosage').text = prescription['medicine']['dosage']

            tree = ET.ElementTree(root)
            tree.write('out/data.xml', encoding='utf-8', xml_declaration=True)
            print(" Данные успешно экспортированы в XML")
        except Exception as e:
            print(f" Ошибка при экспорте в XML: {e}")

    def export_to_yaml(self, data):
        """Экспорт данных в YAML"""
        try:
            with open('out/data.yaml', 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
            print("✅ Данные успешно экспортированы в YAML")
        except Exception as e:
            print(f" Ошибка при экспорте в YAML: {e}")

    def run_export(self):
        """Основной метод для выполнения экспорта"""
        print(" Начало экспорта данных...")

        # Получаем данные
        data = self.fetch_patient_data()

        if not data:
            print(" Не удалось получить данные из базы")
            return

        print(f"📊 Найдено пациентов: {len(data)}")

        # Экспортируем во все форматы
        self.export_to_json(data)
        self.export_to_csv(data)
        self.export_to_xml(data)
        self.export_to_yaml(data)

        print("Экспорт завершен! Файлы сохранены в папке 'out/'")


def main():
    """Главная функция"""
    db_path = "database/hospital.db"

    # Проверяем существование базы данных
    if not os.path.exists(db_path):
        print(f" База данных не найдена: {db_path}")
        print("Сначала запустите main.py для создания базы данных")
        return

    # Создаем экземпляр класса и запускаем экспорт
    formatter = DataFormatter(db_path)
    formatter.run_export()


if __name__ == "__main__":
    main()